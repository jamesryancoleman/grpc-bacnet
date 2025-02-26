import sys

import grpc
import comms_pb2
import comms_pb2_grpc

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

# def Get(keys:str, addr=devCtrlAddr) -> str:
#     header = comms_pb2.Header(Src=devCtrlAddr, Dst=addr)


#     with grpc.insecure_channel(addr) as channel:
#         stub = comms_pb2_grpc.GetSetRunStub(channel)
#         result:comms_pb2.GetResponse
#         result = stub.Get(comms_pb2.GetRequest(
#             Header=header,
#             Keys=key,
#         ))
#         return result.Value
def Get(keys:list[str], addr=devCtrlAddr) -> list[comms_pb2.GetResponse]:
    header = comms_pb2.Header(Src=devCtrlAddr, Dst=addr)
    if isinstance(keys, str):
        keys = [keys]

    result:comms_pb2.GetResponse
    with grpc.insecure_channel(addr) as channel:
        print("opened channel with addr:", addr)
        stub = comms_pb2_grpc.GetSetRunStub(channel)
        result = stub.Get(comms_pb2.GetRequest(
            Header=header,
            Keys=keys
        ))
    
    return result.Pairs


def Set(keys:str, values:str, addr=devCtrlAddr) -> bool:
    header = comms_pb2.Header(Src=devCtrlAddr)
    if isinstance(keys, str):
        keys = [keys]
    if isinstance(values, str):
        values = [values]
    
    if len(keys) != len(values):
        print("error: Set must receive equal numbers of keys and values ({} != {})".format(
            len(keys), len(values)))
        return False
    pairs:list[comms_pb2.SetPair] = [comms_pb2.SetPair(k, values[i]) for i, k in enumerate(keys)]
    
    result:comms_pb2.SetResponse
    with grpc.insecure_channel(addr) as channel:
        stub = comms_pb2_grpc.GetSetRunStub(channel)

        result = stub.Set(comms_pb2.SetRequest(
            Header=header,
            Key=keys,
            Value=pairs, 
        ))
    return result.Ok



