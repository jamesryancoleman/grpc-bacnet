import re

# these are the only two needed
bacnet_re = re.compile(r'^(?P<schema>[a-z]+)://(?P<host>[a-zA-Z0-9.-]+):?(?P<port>[0-9]+)?/(?P<device>[0-9]+)/?(?P<obj_type>[a-zA-Z-_]+)?,?(?P<obj_inst>[0-9]+)?/?(?P<prop>[a-zA-Z0-9-_]+)?/?(?P<index>[0-9]+)?\??(?P<query_params>[^\?]+)?')
params_re = re.compile(r'[a-zA-Z0-9-_]+=?[0-9\.]+?(?=&|\b)')

addr_re = re.compile(r'(?P<host>[a-zA-Z0-9.-]+):?(?P<port>[0-9]+)?')

class BACnetPtParams(object):
    def __init__(self) -> None:
        self.is_valid = False
        self.host = ""              # 192.168.1.99  
        self.port = 47808           # 0xBAC0 (47808) or 0xBAC1 (47809)
        self.address = ""           # "{host+str(port)}"
        self.device_instance = 0    # [1, 4194302]
        self.object_identifier = "" # a 2-tuple e.g, "analog-value,3"
        self.object_type = ""       # device, analog-input, analog-output, etc.
        self.object_instance = 0    # [1, 4194302]
        self.property = ""          # present-value
        self.index = None           # [1, 23]

        # write specific params
        self.value = None
        self.priority = 16

        # for future use
        self.kwargs = {}
        self.flags = []
    
    def __repr__(self):
        return f"BACnetPtParams(host='{self.host}', port={self.port}, device_instance={self.device_instance}, object_identifier='{self.GetObjectId()}, property='{self.property}')"

    def Tidy(self):
        if (self.host != "") and (self.port != 47808):
            self.address = self.host + ":"+ str(self.port)
        elif self.host != "":
            self.address = self.host

        if (self.address != "") and (self.object_type != "") and (self.object_instance != 0) and (self.property != ""):
            self.object_identifier = self.GetObjectId()
            self.is_valid = True
        else:
            self.is_valid = False

    def GetObjectId(self) -> str:
        return self.object_type + "," + str(self.object_instance)

    def SetAddress(self, address:str, default_port:int=47808) -> bool:
        self.address = address
        socket = ParseAddress(address)
        self.host = socket["host"]
        if socket["port"]:
            self.port = socket["port"]
        else:
            self.port = default_port

    def GetUri(self) -> str:
        # make sure that address and object id are valid
        if not self.is_valid:
            self.Tidy()
        return "bacnet://{}/{}/{}/{}".format(self.address,
                                      self.device_instance,
                                      self.object_identifier,
                                      self.property,
                                      )


def ParseBacnetPtKey(uri:str) -> BACnetPtParams:
    """ParseBacnetPtKey takes a uri key of the format 
    `bacnet://<host>[:port]/<dev>/<object_type>,<object_inst>/<property>[/<index>]`
    and returns a populated BACnetPtParams object.
    """
    params = BACnetPtParams()
    matches = bacnet_re.match(uri)
    groups = matches.groupdict()

    params.host = groups['host']
    if groups['port'] is not None:
        params.port = groups['port']
    params.device_instance = groups['device']
    params.object_type = groups['obj_type']
    params.object_instance = groups['obj_inst']
    params.property = groups['prop']
    
    params.Tidy() # ensure address includes port and object id is stored

    return params


def ParseAddress(addr:str) -> dict:
    matches = bacnet_re.match(addr)
    return matches.groupdict()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        pass
    else:
        bacnet_uris = [
        "bacnet://192.168.1.23:47808/123/analog-value,19/present-value",
        "bacnet://node6/123/analog-input,19/present-value"]

        for uri in bacnet_uris:
            params = ParseBacnetPtKey(uri)
            print(params.__dict__)