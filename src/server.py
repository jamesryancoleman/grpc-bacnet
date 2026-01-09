"""
A gRPC server to handle BACnet work.

Based on read-property.py
"""

import asyncio
import re

from bacpypes3.debugging import ModuleLogger
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application
from bacpypes3.settings import settings

from bacpypes3.pdu import Address
from bacpypes3.primitivedata import Atomic, ObjectIdentifier
from bacpypes3.constructeddata import Sequence,AnyAtomic, Array, List
from bacpypes3.apdu import ErrorRejectAbortNack
from bacpypes3.json.util import (
    atomic_encode,
    sequence_to_json,
    extendedlist_to_json_list,
)

from concurrent import futures
from zoneinfo import ZoneInfo
import datetime as dt
import logging
import sys

from argparse import Namespace

import grpc
from src import parse
from src import common_pb2
from src import common_pb2_grpc

from typing import Callable, Any

import src.app as app

_local_tz = ZoneInfo("America/New_York")
_app_config_file = "test/bacpypes3_config.ini"

# some debugging
_debug = 0
_log = ModuleLogger(globals())
_log.setLevel(logging.DEBUG)
# _log.setLevel(logging.INFO)

# 'property[index]' matching
property_index_re = re.compile(r"^([0-9A-Za-z-]+)(?:\[([0-9]+)\])?$")

# globals
INSTANCE_SERVER = 999
INSTANCE_LOW = 0
INSTANCE_HIGH = 4194302 # 4194303

# MUST CHANGE THIS
SERVER_ADDRESS:str  # e.g., 192.168.1.1
MASK:str = "24"

SERVER_PORT:str = "50062"     # e.g., 50062

async def ReadProperty(device_addr:str, object_id:str, property_id:str) -> str:         
    try:
        client = app.BACnetClient.get()
        response = await client.read_property(device_addr, object_id, property_id)
        if _debug:
                _log.debug("    - response: %r", response)
        print("present value:", response)
    except Exception as e:
        print(f"Error: {e}")
        raise
    if response is not None:
        return(str(response)) # str | None
    else:
        return(None)


async def WriteProperty(device_address:str, object_identifier:str, property_id:str,  
                        value:str=None, priority=None, array_index=None):
    """ Should the default priority be 16? (or maybe that's 15?)
    """
    app = None # clear the app out
    try:
        if _debug:
            _log.debug("args: %r", args)
        if app is None:
            # build an application
            app = Application.from_args(args)

            # parse = SimpleArgumentParser()
            # parse.expand_args(args) # this should set debugging to True and add color

        # interpret the address
        device_address = Address(device_address)
        if _debug:
            _log.debug("device_address: %r", device_address)

        # interpret the object indentifier
        object_identifier = ObjectIdentifier(object_identifier)
        if _debug:
            _log.debug("object_identifier: %r", object_identifier)

        # split the property identifier and its index
        property_index_match = property_index_re.match(property_id)
        if not property_index_match:
            raise ValueError("property specification incorrect")
        property_identifier, property_array_index = property_index_match.groups()
        if property_identifier.isdigit():
            property_identifier = int(property_identifier)
        if property_array_index is not None:
            property_array_index = int(property_array_index)

        # check if caller wants a specific priority
        if priority:
            if (priority < 1) or (priority > 16):
                raise ValueError(f"set error: priority {priority}")
        if _debug:
            _log.debug("priority: %r", priority)

        try:
            response = await app.write_property(
                device_address,
                object_identifier,
                property_id,
                value,
                array_index,
                priority,
            )
            if _debug:
                _log.debug("response: %r", response)
            # print(response)
            if response is None:
                return True
        except ErrorRejectAbortNack as err:
            if _debug:
                _log.debug("    - exception: %r", err)
            response = err
            return False
    finally:
        if app:
            app.close()


# the gRPC server implementation
class BACnetRPCServer(common_pb2_grpc.DeviceControlServicer):
    async def Get(self, request:common_pb2.GetRequest, context):
        if _debug:
            _log.debug("get_request:\n%r", request)
        # print("received Get request:\n", request, sep="")
        header = common_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)
        bacnet_client = app.BACnetClient.get()
        results = {}
        for key in request.Keys:
            params = parse.ParseBacnetPtKey(key)
            if params.is_valid:
                try:
                    resp = await bacnet_client.read_property(
                        device_addr=params.address,
                        object_id=params.GetObjectId(),
                        property_id=params.property,
                    )
                    if resp is not None:
                        results[key] = resp
                except Exception as e:
                    _log.error(f"Error getting key '{key}': {e}")
                    continue
        
        # copy results to the response format
        pairs:list[common_pb2.GetPair] = []
        for k, v in results.items():
            pairs.append(common_pb2.GetPair(
                Key=k,
                Value=str(v),
                time=dt.datetime.now(_local_tz),
                # TODO Dtype=[something] ,
            ))
        return common_pb2.GetResponse(
            Header=header,
            Pairs=pairs,
        )
    
    def Set(self, request:common_pb2.SetRequest, context) -> common_pb2.SetResponse:
        print("set request received: ", request)
        header = common_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

        results:list[common_pb2.SetPair] = []
        for pair in request.Pairs:
            params = parse.ParseBacnetPtKey(pair.Key)
            ok = asyncio.run(WriteProperty(params.address,
                                                params.GetObjectId(),
                                                params.property,
                                                pair.Value))
            if ok:
                pair.Ok = True
            results.append(pair)
            print("{} <- {} (ok={})".format(pair.Key, pair.Value, pair.Ok)) 

        return common_pb2.SetResponse(
            Header=header,
            Pairs=results,
        )   
                                  

# need to use specified port in the oxigraph instance
async def initGRPC(port:str=SERVER_PORT) -> grpc.aio.Server:
    # GRPC set up
    server = grpc.aio.server()
    common_pb2_grpc.add_DeviceControlServicer_to_server(BACnetRPCServer(), server)
    server.add_insecure_port("0.0.0.0:" + port)
    _log.info("gRPC server started. Listening on port: %s", port)
    await server.start()
    if app._debug:
        app._log.debug("grpc: %r", server)
    return server

async def startBACnetApp():
    # load args from config file
    args = app.load_ini_args(_app_config_file, debug_modules=["src.app", __name__], color=True)
    await app.BACnetClient.create(args)

    # create the singleton app instance
    bacnet_client = app.BACnetClient.get()

    if app._debug:
        app._log.debug("args: %r", args)
        app._log.debug("settings: %r", settings)
        app._log.debug("app: %r", bacnet_client)

async def main(early_stop:int=0):
    await startBACnetApp()
    grpc_server = await initGRPC()

    async def server_graceful_shutdown():
        if app._debug:
            app._log.info("Starting graceful shutdown")
        await grpc_server.stop(3)
    
    if early_stop:
        await asyncio.sleep(early_stop)
    else:
        await grpc_server.wait_for_termination()
    await server_graceful_shutdown()

    if app._debug:
        app._log.info("async main() finished")


if __name__ == "__main__":
    asyncio.run(main())

