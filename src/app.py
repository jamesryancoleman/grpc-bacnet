import asyncio
import logging
import sys
import re

from bacpypes3.primitivedata import ObjectIdentifier
from bacpypes3.constructeddata import AnyAtomic
from bacpypes3.apdu import ErrorRejectAbortNack
from bacpypes3.debugging import bacpypes_debugging, ModuleLogger, LoggingFormatter
from bacpypes3.settings import settings
from bacpypes3.app import Application
from bacpypes3.pdu import Address
from bacpypes3.vendor import VendorInfo, get_vendor_info

from bacpypes3.argparse import INIArgumentParser, create_log_handlers
import argparse

# Register vendor 15 (used by BACpypes for testing)
VendorInfo(vendor_identifier=15)

import src.parse

# some debugging
_debug = 1
_log = ModuleLogger(globals())
_log.setLevel(logging.DEBUG)

# 'property[index]' matching
property_index_re = re.compile(r"^([0-9A-Za-z-]+)(?:\[([0-9]+)\])?$")

def load_ini_args(path:str, debug_modules:list[str]=None, color:bool=False) -> argparse.Namespace:
    # turn on logging and colors
    create_log_handlers(debug_modules, use_color=True)
    
    sys.argv = ['app', '--ini', path]
    INIArgumentParser().parse_args()
    
    ini = settings['ini']['BACpypes']
    args = argparse.Namespace(
        name=ini['objectname'],
        instance=int(ini['objectidentifier']),
        address=ini['address'],
        vendoridentifier=int(ini['vendoridentifier']),
        network=0,
        foreign=None,
        ttl=30,
        bbmd=None,
        loggers=False,
        debug=debug_modules,
        color=color,
        route_aware=None,
    )
    return args

class BACnetClient:
    _instance: 'BACnetClient' = None
    
    def __init__(self, app: Application):
        self._app = app
        self._semaphore = asyncio.Semaphore(8)  # tune based on your network
    
    @classmethod
    async def create(cls, args) -> 'BACnetClient':
        """Factory method - call once at startup."""
        print()
        app = Application.from_args(args)
        if _debug:
            _log.debug("app: %r", app)
        cls._instance = cls(app)
        await asyncio.sleep(0.5)  # Let the network stack settle
        return cls._instance
    
    @classmethod
    def get(cls) -> 'BACnetClient':
        """Get the singleton instance."""
        if cls._instance is None:
            raise RuntimeError("BACnetClient not initialized - call create() first")
        return cls._instance
    
    async def read_property(self, device_addr: str, object_id: str, property_id: str) -> str:
        async with self._semaphore:
            device_address = Address(device_addr)
            object_identifier = ObjectIdentifier(object_id)
            
            property_index_match = property_index_re.match(property_id)
            if not property_index_match:
                raise ValueError("property specification incorrect")
            
            property_identifier, property_array_index = property_index_match.groups()
            if property_identifier.isdigit():
                property_identifier = int(property_identifier)
            if property_array_index is not None:
                property_array_index = int(property_array_index)

            try:
                response = await self._app.read_property(
                    device_address,
                    object_identifier,
                    property_identifier,
                    property_array_index,
                )
            except ErrorRejectAbortNack as err:
                if _debug:
                    _log.debug("    - exception: %r", err)
                return str(err)

            if isinstance(response, AnyAtomic):
                response = response.get_value()
            
            return response
    
    async def write_property(
            self, device_addr:str,
            object_id:str, 
            property_id:str,
            value,
            priority=None,
            array_index=None):
        async with self._semaphore:
            device_addr = Address(device_addr)
            object_id = ObjectIdentifier(object_id)

            # split the property identifier and its index
            property_index_match = property_index_re.match(property_id)
            if not property_index_match:
                raise ValueError("property specification incorrect")
            property_id, property_array_index = property_index_match.groups()
            if property_id.isdigit():
                property_id = int(property_id)
            if property_array_index is not None:
                property_array_index = int(property_array_index)

            # check if caller wants a specific priority
            if priority:
                if (priority < 1) or (priority > 16):
                    raise ValueError(f"set error: priority {priority}")
        if _debug:
            _log.debug("priority: %r", priority)
            try:
                resp = await self._app.write_property(
                    device_addr,
                    object_id,
                    property_id,
                    value,
                    array_index,
                    priority,
                )
                if _debug:
                    _log.debug("write_resp: %r", resp)
            except ErrorRejectAbortNack as err:
                if _debug:
                    _log.debug("    - exception: %r", err)
                return str(err)
    
    async def close(self):
        """Call only at shutdown."""
        self._app.close()