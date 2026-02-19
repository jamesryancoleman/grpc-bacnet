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
from bacpypes3.primitivedata import Atomic, ObjectIdentifier, Real
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
import src.parse as parse
import src.common_pb2 as common_pb2
import src.common_pb2_grpc as common_pb2_grpc

from typing import Callable, Any

import src.app as app
# import app

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

# the gRPC server implementation
class BACnetRPCServer(common_pb2_grpc.DeviceControlServicer):
    async def Get(self, request:common_pb2.GetRequest, context):
        if _debug:
            _log.debug("get_request received")
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
            # print(f'the type of {k} is {type(v)} ({v})')
            # if isinstance(v, int):
            #     _dtype = common_pb2.INT64
            if isinstance(v, Real):
                _dtype = common_pb2.DOUBLE
            else:
                 _dtype = common_pb2.STRING

            pairs.append(common_pb2.GetPair(
                Key=k,
                Value=str(v),
                time=dt.datetime.now(_local_tz),
                Dtype=_dtype
            ))
        return common_pb2.GetResponse(
            Header=header,
            Pairs=pairs,
        )
    
    async def Set(self, request:common_pb2.SetRequest, context) -> common_pb2.SetResponse:
        if _debug:
            _log.debug("set_request received")
        header = common_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)

        bacnet_client = app.BACnetClient.get()
        results:list[common_pb2.SetPair] = []
        for pair in request.Pairs:
            params = parse.ParseBacnetPtKey(pair.Key)
            resp = await bacnet_client.write_property(
                params.address,
                params.GetObjectId(),
                params.property,
                pair.Value,
            )
            if resp is None:
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

