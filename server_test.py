import asyncio
import sys

import server
import parse

import json

import random as rand

# assumed to be a RaspberryPi running B
host1 = "192.168.1.177" 
host2 = "192.168.13.142"
host2 = "192.168.1.197" 

device_id_1 = 9
device_id_2 = 123
test_url_1 = "bacnet://{}/{}/analog-input,4/present-value".format(host1, device_id_1)
test_url_2 = "bacnet://{}/{}/analog-input,6/present-value".format(host1, device_id_1)
test_url_3 = "bacnet://{}/{}/analog-value,1/present-value".format(host2, device_id_2)

DEFAULT_PATH = "test_cases.json"

URL_FMT = "bacnet://{}/{}/{}/{}" # .format(IP, DEVICE, OBJECT, PROPERTY)

def LoadTestCases(path:str) -> list[dict]:
    test_cases:dict
    with open(path) as f:
        test_cases = json.load(f)
    return test_cases

def TestCaseToUri(case:dict, object_id:str) -> str:
    uri = URL_FMT.format(case['address'], case['device'], object_id, case['objects'][object_id]['property'])
    return uri

def ReadTest(url:str):
    params = parse.ParseBacnetPtKey(url)
    r = asyncio.run(server.ReadProperty(params.address,
                                        params.GetObjectId(),
                                        params.property))
    print(url, "->", r)

def WriteTest(url:str, value:str="65"):
    params = parse.ParseBacnetPtKey(url)
    r = asyncio.run(server.WriteProperty(params.address,
                                    params.GetObjectId(),
                                    params.property, 
                                    value))
    if r: 
        r = value
    else:
        r = "error"

    print(url, "<-", r)

def ReadMultipleTest(uris:list[str]):
    for s in uris:
        params = parse.ParseBacnetPtKey(s)
        r = asyncio.run(server.ReadProperty(params.address,
                                            params.GetObjectId(),
                                            params.property))
        print(s, "->", r)


def WriteMultipleTest(pairs:list[tuple]):
    for k, v in pairs:
        params = parse.ParseBacnetPtKey(k)
        was = asyncio.run(server.ReadProperty(params.address, params.GetObjectId(), params.property))
        print(k, "->", was)
        ok = asyncio.run(server.WriteProperty(params.address, params.GetObjectId(), params.property, v))
        if ok:
            print(k, "<-", v)
        else:
            print(k, "<-", "error")
        _is = asyncio.run(server.ReadProperty(params.address, params.GetObjectId(), params.property))
        print(k, "->", _is)


def InvalidKeysTest():
    invalid_key_results = {}
    print("X before:", invalid_key_results)
    asyncio.run(DictInvalidKeys(invalid_key_results))
    print("X after:", invalid_key_results)

# check that StashMultiple returns without doing anything if a dict is passed 
# without keys or with the wrong number of args and keys. 
async def DictInvalidKeys(X:dict):
    await server.StashMultiple(
        X=X,
        func=server.StashResult,
        args=['a', 'b', 'c'],
        keys=[] # the default value is also []
    )

    await server.StashMultiple(
        X=X,
        func=server.StashResult,
        args=['a', 'b', 'c'],
        keys=['a']
    )


async def ValidKeys(X:dict):
    args = [('192.168.1.177', 'analog-input,4', 'present-value'),
            ('192.168.1.177', 'analog-input,6', 'present-value'),]
    
    await server.StashMultiple(
        X=X,
        func=server.StashResult,
        args=args,
        keys=[str(i+1) for i in range(len(args))]
    )
    
def valid_keys_test():
    results = {}
    print("X before:", results)
    asyncio.run(ValidKeys(results))
    print("X after: ", results)

async def ValidArgs(X:list[tuple]) -> None:
    args = [('192.168.1.177', 'analog-input,4', 'present-value'),
        ('192.168.1.177', 'analog-input,6', 'present-value'),]
    
    await server.StashMultiple(
        X=X,
        func=server.StashResult,
        args=args
    )

def valid_args_test():
    results = []
    print("X before:", results)
    asyncio.run(ValidArgs(results))
    print("X after: ", results)

# used for testing the other functions
async def GetAsyncValue():
    await asyncio.sleep(0.5)
    return round(rand.randint(0,10))

def dict_stash_test() -> list[any]:
    unordered_results = {}
    asyncio.run(server.StashResult(unordered_results, GetAsyncValue, key="r1"))
    asyncio.run(server.StashResult(unordered_results, GetAsyncValue, key="r2"))
    return unordered_results

def list_stash_test() -> dict[str, any]:
    ordered_results = []
    asyncio.run(server.StashResult(ordered_results, GetAsyncValue))
    asyncio.run(server.StashResult(ordered_results, GetAsyncValue))
    return ordered_results

if __name__ == "__main__":
    C = LoadTestCases(DEFAULT_PATH)    
    uri1 = TestCaseToUri(C[0], "analog-value,1")
    uri2 = TestCaseToUri(C[1], "analog-input,4")
    uri3 = TestCaseToUri(C[1], "analog-input,5")
    uri4 = TestCaseToUri(C[1], "analog-input,6")

    print("== get test ==")
    ReadTest(uri1)

    print("== get multiple ==")
    ReadMultipleTest([uri2, uri3, uri4])

    print("== set test ==")
    WriteTest(uri1, "82.25")
    ReadTest(uri1)

    print("== set multiple ==")
    WriteMultipleTest([(uri1, "82.25"), (uri1, "85.0"), (uri1, "87.5")])