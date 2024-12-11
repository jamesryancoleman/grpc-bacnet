import re

addr_re = re.compile(r'[0-9A-Za-z.]+(?!://)(?=[/:\b])?') # finds the host and port so use [0]
port_re = re.compile(r'(?<=:)[0-9]+(?=/)?')

# bacnet_re = re.compile(r"^bacnet(?=://)")
device_re = re.compile(r'(?<=bacnet://)[0-9A-Za-z.]+(?!://)(?=/:)?') # finds the host and port so use [0]
obj_id_re = re.compile(r'[a-zA-Z-_]+,[0-9]+?')
property_re = re.compile(r'(?<=[0-9]/)[a-zA-Z0-9-_]+(?=[\?/]|$)')
index_re = re.compile(r'(?<=/)[0-9](?=[\?/]|$)')
query_re = re.compile(r'(?<=[&\?])[A-Za-z0-9\_\-\.\=]+')

# these are the only two needed
bacnet_re = re.compile(r'^(?P<schema>[a-z]+)://(?P<host>[a-zA-Z0-9.-]+):?(?P<port>[0-9]+)?/(?P<device>[0-9]+)/?(?P<obj_type>[a-zA-Z-_]+)?,?(?P<obj_inst>[0-9]+)?/?(?P<prop>[a-zA-Z0-9-_]+)?/?(?P<index>[0-9]+)?\??(?P<query_params>[^\?]+)?')
params_re = re.compile(r'[a-zA-Z0-9-_]+=?[0-9\.]+?(?=&|\b)')

class BACnetPtParams():
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

# Depricated no not use
def ParseBACnetUri(uri:str) -> BACnetPtParams:
    """ParseBACnetUrl takes a url string and returns a dict with the keys:
    "valid" (bool), "host" (string), port (int), path (list)."""
    params = BACnetPtParams()

    if len(bacnet_re.findall(uri)) == 0:
        # user id not provide schema
        return None
    
    # get the host address
    _dev = device_re.findall(uri)
    if len(_dev) > 0:
        params.host = _dev[0]

    # look for a port
    _port = port_re.findall(uri)
    if len(_port) > 0:
        params.port = int(_port[0])

    # grab the object identifier
    _obj_id = obj_id_re.findall(uri)
    if len(_obj_id) > 0:
        params.object_identifier = _obj_id[0]

        # split up the object type and the object instance
        id_parts = _obj_id[0].split(",")
        params.object_type = id_parts[0]
        params.object_instance = id_parts[1]

    # grab the property
    _property = property_re.findall(uri)
    if len(_property) > 0:
        params.property =  _property[0]

    # grab the index, if provided
    _index = index_re.findall(uri)
    if len(_index) > 0:
        try:
            params.index = int(_index[0])
        except ValueError:
            # let params.index remain None
            pass

    # parse the query params
    args = query_re.findall(uri)
    for a in args:
        parts = a.split("=")
        if len(parts) > 1:
            # we have a kwarg
            if parts[0]=="value":
                params.value=parts[1]
            elif parts[0]=="priority":
                params.priority=int(parts[1])
            else:
                # we have a kwargs
                params.kwargs[parts[0]] = parts[1]
        else:
            # we have a flag
            params.flags.append(a)

    # format the address
    params.Tidy()
    
    return params


def ParseAddress(address:str) -> dict:
    socket = {
        "host": None,
        "port": None,
        }

    host = addr_re.findall(address)
    if len(address) > 0:
        socket["host"] = host[0]
    else:
        socket["host"] = None

    port = port_re.findall(address)
    if len(port) > 0:
        socket["port"] = port[0]
    else:
        socket["port"] = None

    return socket


bos_point_re = re.compile(r'(?P<schema>[a-z]+)://(?P<host>[a-zA-Z0-9.-]+):?(?P<port>[0-9]+)?/bos/dev/(?P<device>[0-9]+)/pts/(?P<point>[0-9]+)')

def ParseBosPoint(uri:str) -> str:
    bpm = bos_point_re.match(uri)
    g = bpm.groupdict()

    return g['device'] + "." + g['point']


if __name__ == "__main__":
    import sys


    # uri_tests = [
    #     # just a device
    #     "bacnet://123/device,321",
    #     # complete point
    #     "bacnet://123:47809/analog-value,1/present-value",
    #     # point with index
    #     "bacnet://123/analog-value,1/present-value/3",
    #     # point with value and priority
    #     "bacnet://123/analog-value,1/present-value?value=100.0&priority=9",
    #     # point with index and value
    #     "bacnet://123/analog-value,1/present-value?value=100.0&priority=9",
    #     # point with index, value, and priorty
    #     "bacnet://123:47808/analog-value,1/present-value/3?value=100.0&priority=9",
    # ]

    # socket_tests = [
    #     "192.168.1.123",            # 47808 is implied
    #     "192.168.1.321:47809",      # 47809 is explicit
    #     "node6:47808",              # 47808 is explicit
    #     "node6/path/to/resource",   # root path is explicity
    #     "192.168.1.23:47809/resouce?flag",      # port and root path is explicit
    # ]

    combined_uri_tests = [
        # a write point
        "bacnet://192.168.1.23:47808/123/analog-value,19/present-value/4?value=69.0&priority=9",
        # a read request
        "bacnet://node6/123/analog-value,19/present-value"
    ]

    res = ParseBosPoint("bos://localhost/bos/dev/2/pts/15")
    print(res)


    # # compile the regexps
    # for i, t in enumerate(combined_uri_tests):
    #     km = key_re.match(t)
    #     groups = km.groupdict()
    #     print(i+1, groups)

    #     p_dict = {}
    #     if "query_params" in groups:
    #         query_str = groups["query_params"]
    #         if query_str != "":
    #             # TODO debug why this breaks when there are no query params
    #             params = params_re.findall(query_str)
    #             for p in params:
    #                 if "=" in p:
    #                     # key value pair
    #                     parts = p.split("=")
    #                     p_dict[parts[0]] = parts[1]
    #                 else:
    #                     # flag
    #                     p_dict[parts[0]] = True
    #         print("write params:", p_dict)
    #     else:
    #         print("read-only")


