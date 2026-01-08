"""
A gRPC server to handle BACnet work.

Based on read-property.py
"""

import asyncio
import re

from bacpypes3.debugging import ModuleLogger
from bacpypes3.argparse import SimpleArgumentParser
from bacpypes3.app import Application

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
import parse

import grpc
import common_pb2
import common_pb2_grpc

from typing import Callable, Any

_local_tz = ZoneInfo("America/New_York")

# some debugging
_debug = 0
_log = ModuleLogger(globals())
_log.setLevel(logging.DEBUG)
# _log.setLevel(logging.INFO)

# 'property[index]' matching
property_index_re = re.compile(r"^([0-9A-Za-z-]+)(?:\[([0-9]+)\])?$")

# globals
# app: Application = None

INSTANCE_SERVER = 999
INSTANCE_LOW = 0
INSTANCE_HIGH = 4194302 # 4194303

# MUST CHANGE THIS
SERVER_ADDRESS:str  # e.g., 192.168.1.1
MASK:str = "24"

SERVER_PORT:str = "50062"     # e.g., 50062

args = Namespace(
    # loggers=False,
    # debug= "__main__",
    route_aware=None,
    name='BACpi',
    instance=INSTANCE_SERVER,
    network=0,
    # address="192.168.1.127/24", # set this to the machines IP.
    vendoridentifier=999,
    foreign=None,
    ttl=30,
    bbmd=None,
)

async def StashMultiple(X:dict[str,Any]|list[str], 
                      func:Callable,
                      args:list[tuple[tuple, dict]],
                      keys:list[str]=[]) -> None:
    """ For each tuple in args StashMultiple takes creates an asyncio Task for
    func and passes the tuple as the positional arguments. 

    The 0th position of the tuple is args and the 1st position is kwargs.
    i.e., func with be called with [func](*args, **kwargs)
    """

    async with asyncio.TaskGroup() as tg:
        if type(X) is dict:
            # valid input for args
            if len(args) != len(keys):
                print('number of args and keys must match if type(X) is dict.\nlen(args)->{} != len(keys)->{}'.format(len(args), len(keys)))
                return 
            for k, A in zip(keys,args):
                print(k, A)
                tg.create_task(StashResult(X, func, *A, key=k))
        elif type(X) is list:
            # assume args will be valid
            for A in args:
                tg.create_task(StashResult(X, func, *A))
    return 
    

# utility function for stashing the results of multiple calls to a function in an iterable.
async def StashResult(X:dict[str,any]|list[str], 
                      func:Callable,
                      *args,
                      **kwargs) -> None:
    key = None
    if 'key' in kwargs:
        key = kwargs.get('key')
    
    if type(X) is dict and key is not None:
        X[key] = await func(*args)
    elif type(X) is list:
        X.append(await func(*args))


async def ReadProperty(device_addr:str, object_id:str, property_id:str) -> str:
    app = None # clear the app out
    try:
        if app is None:
            # build an application
            app = Application.from_args(args)
        if _debug:
            _log.debug("app: %r", app) 
        
        if _debug:
            _log.debug("debug: %r", _debug) 
        
        # interpret the address
        device_address = Address(device_addr)
        if _debug:
            _log.debug("device_address: %r", device_address)
        
        # interpret the object identifier
        object_identifier = ObjectIdentifier(object_id)
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


        try:
            # print("Trying to get response:")
            # print(device_address,object_identifier, property_identifier, property_array_index)
            response = await app.read_property(
                device_address,
                object_identifier,
                property_identifier,
                property_array_index,
            )
            if _debug:
                _log.debug("    - response: %r", response)
        except ErrorRejectAbortNack as err:
            if _debug:
                _log.debug("    - exception: %r", err)
            response = err

        if isinstance(response, AnyAtomic):
            if _debug:
                _log.debug("    - schedule objects")
            response = response.get_value()
        # print(str(response))
    
    finally:
        # pass # leave app running
        if app:
            app.close()
    
    return(str(response)) # str | None


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
    def Get(self, request:common_pb2.GetRequest, context):
        # print("globals:")
        # for k, v in globals().items():
        #     print(k,": ", v, sep="")
        if _debug:
            _log.debug("get_request:\n%r", request)
        # print("received Get request:\n", request, sep="")
        header = common_pb2.Header(Src=request.Header.Dst, Dst=request.Header.Src)
        
        # fetch the (id, BacnetPtParams) tuples from the sysmod service
        pairs = []
        for key in request.Keys:
            params = parse.ParseBacnetPtKey(key)
            if params.is_valid:
                pairs.append((key, params))

        # format the args that will be passed to each coroutine
        args = []
        for p in pairs:
            args.append((p[1].address, p[1].object_identifier, p[1].property))

        # create a dict to store the results (unordered)
        unordered_results = {}
        asyncio.run(StashMultiple(
            X=unordered_results,
            func=ReadProperty,
            args=args,
            keys=request.Keys # the result dict keys are the point ids
        ))
        
        # copy results to the response format
        results:list[common_pb2.GetPair] = []
        
        for k, v in unordered_results.items():
            results.append(common_pb2.GetPair(
                Key=k,
                Value=str(v),
                time=dt.datetime.now(_local_tz),
                # TODO Dtype=[something] ,
            ))
        return common_pb2.GetResponse(
            Header=header,
            Pairs=results,
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
async def serve(port:str=SERVER_PORT) -> None:
    # parse reused app arguments
    global args
    # _log

    parser = SimpleArgumentParser()
    args = parser.parse_args()
    args.address = '192.168.13.127/24'
    # print(vars(_log))
    # _log.basicConfig(level=logging.INFO)
    # Remove all existing handlers
#     for handler in logging.root.handlers[:]:
#         logging.root.removeHandler(handler)

#     # Set up your logging configuration
#     logging.basicConfig(
#         level=logging.INFO,
#         # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

    # GRPC set up
    server = grpc.aio.server()
    common_pb2_grpc.add_DeviceControlServicer_to_server(BACnetRPCServer(), server)
    result = server.add_insecure_port("0.0.0.0:" + port)
    # print(result)
    _log.info("gRPC server started. Listening on port: %s", port)
    await server.start()

    async def server_graceful_shutdown():
        _log.info("Starting graceful shutdown")
        await server.stop(3)
    
    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()

# Coroutines to be invoked when the event loop is shutting down.
_cleanup_coroutines = []

if __name__ == "__main__":
    # if len(sys.argv) > 2:
    # print(sys.argv)
    # SERVER_ADDRESS = "{}/{}".format(sys.argv[1], MASK)
    # SERVER_PORT = SER

    # args = Namespace(
    #     # loggers=False,
    #     debug=0,
    #     color=True,
    #     route_aware=None,
    #     name='BACpi',
    #     instance=INSTANCE_SERVER,
    #     network=0,
    #     # address="", # set this to the machines IP. default is "" (empty str)
    #     vendoridentifier=999,
    #     foreign=None,
    #     ttl=30,
    #     bbmd=None,
    # )

    # logging.basicConfig(level=logging.INFO)
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()

    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
    # else:
    #     print("bacnet server requires 2 args: LISTEN_ADDR PORT")
    #     if len(sys.argv) == 2:
    #         SERVER_ADDRESS = "{}/{}".format(sys.argv[1], MASK)
    #         print("\t1 arg received LISTEN_ADDR={}".format(SERVER_ADDRESS))
    #     sys.exit(1)
