import unittest
import logging
import sys

import asyncio

import src.app
import src.parse

import random

from bacpypes3.debugging import ModuleLogger
from bacpypes3.settings import settings
from bacpypes3.argparse import create_log_handlers

_debug = 1
_log = ModuleLogger(globals())
_log.setLevel(logging.DEBUG)

_app_config_file = "test/bacpypes3_config.ini"
_sample_xref_file = "test/sample_xrefs"
_test_logger_name = "test_logger"

class TestSetUp((unittest.TestCase)):
    def setUp(self):
        self.app_config = _app_config_file

        # these addresses must be live and on your network
        self.test_file_path = _sample_xref_file
        self.test_keys = []
        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]
        
        # sys.argv = sys.argv[len(sys.argv):] + ['--ini', _app_config_file, '--color', f'--debug={"src.app"}']
        print()
    
    def test_load_args(self):
        # Inject the INI path, then append any actual CLI args
        src.app.load_ini_args(_app_config_file)

class TestAppSetUp((unittest.IsolatedAsyncioTestCase)):
    async def asyncSetUp(self):
        # these addresses must be live and on your network
        self.test_file_path = _sample_xref_file

        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]
        print() 

        # load args from config file
        args = src.app.load_ini_args(_app_config_file, debug_modules=["src.app", __name__, "bacpypes3"], color=True)

        # create the singleton app instance
        await src.app.BACnetClient.create(args)
        self.client = src.app.BACnetClient.get()

        if src.app._debug:
            src.app._log.debug("args: %r", args)
            src.app._log.debug("settings: %r", settings)
            src.app._log.debug("app: %r", self.client)

    async def asyncTearDown(cls):
        if src.app.BACnetClient._instance:
            # Close synchronously since tearDownClass isn't async
            src.app.BACnetClient._instance._app.close()
            src.app.BACnetClient._instance = None
    
    async def test_app_exists(self):
        if self.client:
            print("app exists")
    
class TestReadProperty((unittest.IsolatedAsyncioTestCase)):
    async def asyncSetUp(self):
        # these addresses must be live and on your network
        self.test_file_path = _sample_xref_file

        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]
        print() 

        # load args from config file
        args = src.app.load_ini_args(_app_config_file, debug_modules=["src.app", __name__, "bacpypes3.app.Application"], color=True)

        # create the singleton app instance
        await src.app.BACnetClient.create(args)
        self.client = src.app.BACnetClient.get()

        if src.app._debug:
            src.app._log.debug("args: %r", args)
            src.app._log.debug("settings: %r", settings)
            src.app._log.debug("app: %r", self.client)

    async def asyncTearDown(cls):
        if src.app.BACnetClient._instance:
            # Close synchronously since tearDownClass isn't async
            src.app.BACnetClient._instance._app.close()
            src.app.BACnetClient._instance = None

    async def test_read_property(self):
        
        params = src.parse.ParseBacnetPtKey(self.test_keys[3])
        try:
            present_value = await self.client.read_property(device_addr=params.address, object_id=params.GetObjectId(), property_id=params.property)
            print("present value:", present_value)
        except Exception as e:
            print(f"Error: {e}")
            raise

class TestReadPropertySequential((unittest.IsolatedAsyncioTestCase)):
    async def asyncSetUp(self):
        # these addresses must be live and on your network
        self.test_file_path = _sample_xref_file

        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]
            self.test_keys = self.test_keys + self.test_keys + self.test_keys
        print() 

        # load args from config file
        args = src.app.load_ini_args(_app_config_file, debug_modules=["src.app", __name__], color=True)

        # create the singleton app instance
        await src.app.BACnetClient.create(args)
        self.client = src.app.BACnetClient.get()

        if src.app._debug:
            src.app._log.debug("args: %r", args)
            src.app._log.debug("settings: %r", settings)
            src.app._log.debug("app: %r", self.client)

    async def asyncTearDown(cls):
        if src.app.BACnetClient._instance:
            # Close synchronously since tearDownClass isn't async
            src.app.BACnetClient._instance._app.close()
            src.app.BACnetClient._instance = None

    async def test_read_property(self):
        for k in self.test_keys:
            params = src.parse.ParseBacnetPtKey(k)
            try:
                present_value = await self.client.read_property(device_addr=params.address, object_id=params.GetObjectId(), property_id=params.property)
                print("present value:", present_value)
            except Exception as e:
                print(f"Error: {e}")
                raise

class TestWriteProperty((unittest.IsolatedAsyncioTestCase)):
    async def asyncSetUp(self):
        # these addresses must be live and on your network
        self.test_file_path = _sample_xref_file

        with open(self.test_file_path, 'r') as file:
            self.test_keys = [line.strip() for line in file.readlines()]
        print() 

        # load args from config file
        args = src.app.load_ini_args(_app_config_file, debug_modules=["src.app", __name__, "bacpypes3.app.Application"], color=True)

        # create the singleton app instance
        await src.app.BACnetClient.create(args)
        self.client = src.app.BACnetClient.get()

        if src.app._debug:
            src.app._log.debug("args: %r", args)
            src.app._log.debug("settings: %r", settings)
            src.app._log.debug("app: %r", self.client)

    async def asyncTearDown(cls):
        if src.app.BACnetClient._instance:
            # Close synchronously since tearDownClass isn't async
            src.app.BACnetClient._instance._app.close()
            src.app.BACnetClient._instance = None

    async def test_write_property(self):
        # a temp set point key
        params = src.parse.ParseBacnetPtKey(self.test_keys[2])
        try:
            # check the current value
            setpoint = await self.client.read_property(device_addr=params.address, object_id=params.GetObjectId(), property_id=params.property)
            setpoint = float(setpoint)
            print("value_at_t0:", setpoint)

            # walk up or down
            if random.randint(0, 1):
                setpoint += 1
            else:
                setpoint -= 1

            # try to write new value to the setpoint
            resp = await self.client.write_property(params.address, params.GetObjectId(), params.property, setpoint)
            print(f"write_resp: {repr(resp)}")

            # check the current value
            setpoint = await self.client.read_property(device_addr=params.address, object_id=params.GetObjectId(), property_id=params.property)
            setpoint = float(setpoint)
            print("value_at_t1:", setpoint)

        except Exception as e:
            print(f"Error: {e}")
            raise