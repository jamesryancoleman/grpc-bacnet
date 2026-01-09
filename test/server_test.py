import unittest
import asyncio
import grpc

from bacpypes3.settings import settings

import src.common_pb2_grpc as common_pb2_grpc
import src.common_pb2 as common_pb2
import src.server
import src.app

import random

_sample_xref_file = "test/sample_xrefs"

class TestServerRead((unittest.IsolatedAsyncioTestCase)):
    async def asyncSetUp(self):
        # these addresses must be live and on your network
        self.test_file_path = _sample_xref_file
        self.test_keys = []
        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]

        if src.app._debug:
            src.app._log.debug("keys: %r", self.test_keys)
        print()

    async def asyncTearDown(self):
        if src.app.BACnetClient._instance:
            # Close synchronously since tearDownClass isn't async
            src.app.BACnetClient._instance._app.close()
            src.app.BACnetClient._instance = None

    async def test_main(self):

        # start the servers
        _main_task = asyncio.create_task(src.server.main(early_stop=3))
        await asyncio.sleep(1) # wait for servers to spin up

        # issue a client call
        async with grpc.aio.insecure_channel(f"0.0.0.0:{src.server.
        SERVER_PORT}") as channel:
            stub = common_pb2_grpc.DeviceControlStub(channel)
            req = common_pb2.GetRequest(Keys=self.test_keys)
            resp:common_pb2.GetResponse = await stub.Get(req)
            for pair in resp.Pairs:
                print(f"key='{pair.Key}', value={float(pair.Value):.3f}, time={pair.time.ToDatetime()}")

        await _main_task
    
class TestServerWrite((unittest.IsolatedAsyncioTestCase)):
    async def asyncSetUp(self):
        # these addresses must be live and on your network
        self.test_file_path = _sample_xref_file
        self.test_keys = []
        self.key:str
        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]
            # use only a known setpoint
            self.key = self.test_keys[2]

        if src.app._debug:
            src.app._log.debug("key: %r", self.key)
        print()

    async def asyncTearDown(self):
        if src.app.BACnetClient._instance:
            # Close synchronously since tearDownClass isn't async
            src.app.BACnetClient._instance._app.close()
            src.app.BACnetClient._instance = None

    async def test_main(self):
        # start the servers
        _main_task = asyncio.create_task(src.server.main(early_stop=3))
        await asyncio.sleep(1) # wait for servers to spin up

        async with grpc.aio.insecure_channel(f"0.0.0.0:{src.server.
        SERVER_PORT}") as channel:
            stub = common_pb2_grpc.DeviceControlStub(channel)

            # issue a client read
            req = common_pb2.GetRequest(Keys=[self.key])
            resp:common_pb2.GetResponse = await stub.Get(req)
            value:str|int
            for pair in resp.Pairs:
                value = pair.Value
                value = float(value)
                print(f"key='{pair.Key}', value={float(value):.3f}, time={pair.time.ToDatetime()}")

            # random value on value
            if random.randint(0,1):
                value += 1
            else:
                value -= 1
            print(f"writing new value of {value} to {self.key}")

            # issue a client write
            req = common_pb2.SetRequest(
                Pairs=[
                    common_pb2.SetPair(
                        Key=self.key,
                        Value=str(value)
                    )
                ], 
            )
            resp:common_pb2.SetResponse = await stub.Set(req)
            if src.app._debug:
                src.app._log.debug("set_resp: %r", resp)

            # check value one more time
            req = common_pb2.GetRequest(Keys=[self.key])
            resp:common_pb2.GetResponse = await stub.Get(req)
            value:str|int
            for pair in resp.Pairs:
                value = pair.Value
                value = float(value)
                print(f"key='{pair.Key}', value={float(value):.3f}, time={pair.time.ToDatetime()}")

        await _main_task