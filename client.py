import sys

import grpc
import device_pb2
import device_pb2_grpc

# device_address = "192.168.1.174"
# description = "Smart Air Quality Monitor"

"""Usage:
    client sends a bos point uri that identifies the point to access.

        e.g., <bos://localhost/dev/3/pts/6>

    devCtrl will query the sysmod and replace it with a uri that looks like:

        <bacnet://192.168.13.133:47808/analog-input/6/present-value>
"""

serverAddr = "localhost:50062"
devCtrlAddr = "localhost:2822"

def Get(key:str, addr=devCtrlAddr) -> str:
    header = device_pb2.Header(Src=devCtrlAddr, Dst=addr)

    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)
        result:device_pb2.GetResponse
        result = stub.Get(device_pb2.GetRequest(
            Header=header,
            Key=key,
        ))
        return result.Value
    


def Set(key:str, value:str, addr=devCtrlAddr) -> bool:
    header = device_pb2.Header(Src=devCtrlAddr)
    
    result:device_pb2.SetResponse

    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)

        result = stub.Set(device_pb2.SetRequest(
            Header=header,
            Key=key,
            Value=value, 
        ))
    return result.Ok


def GetMultiple(keys:list[str], addr=devCtrlAddr) -> list[device_pb2.GetResponse]:
    header = device_pb2.Header(Src=devCtrlAddr, Dst=addr)

    with grpc.insecure_channel(addr) as channel:
        stub = device_pb2_grpc.GetSetRunStub(channel)
        result:device_pb2.GetMultipleResponse
        result = stub.GetMultiple(device_pb2.GetMultipleRequest(
            Header=header,
            Keys=keys
        ))
    
    return result.Responses



# if __name__=="__main__":
#     # key1 = "2.1"
#     # get_test(key1)

#     # key2 = "2.2"
#     # get_multiple_test([key1,key2])

#     key3 = ""
    