import unittest
import asyncio
import grpc

from bacpypes3.settings import settings

import src.common_pb2_grpc as common_pb2_grpc
import src.common_pb2 as common_pb2
import src.server
import src.app

_sample_xref_file = "test/sample_xrefs"

class TestServer((unittest.IsolatedAsyncioTestCase)):
    async def asyncSetUp(self):
        # these addresses must be live and on your network
        self.test_file_path = _sample_xref_file
        self.test_keys = []
        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]

        if src.app._debug:
            src.app._log.debug("keys: %r", self.test_keys)
        print()

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
    
    # async def asyncSetUp(self):
    #     pass