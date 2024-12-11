import asyncio

import server
import parse

import random as rand

host1 = "192.168.1.177"
host2 = "192.168.1.197"
host3 = "192.168.13.142"

device_id_1 = 9
device_id_2 = 123
test_url_1 = "bacnet://{}/{}/analog-input,4/present-value".format(host1, device_id_1)
test_url_2 = "bacnet://{}/{}/analog-input,6/present-value".format(host1, device_id_1)
test_url_3 = "bacnet://{}/{}/analog-value,1/present-value".format(host2, device_id_2)
test_url_4 = "bacnet://{}/{}/analog-value,1/present-value".format(host3, device_id_2)

# test_urls = [test_url_1, test_url_2]
# test_point_ids = ["2.1", "2.2"]

# assert len(test_urls) == len(test_point_ids)


def read_test(url:str=test_url_3):
    params = parse.ParseBacnetPtKey(url)
    print("getting:", params.address, params.GetObjectId(), params.property)

    r = asyncio.run(server.ReadProperty(params.address,
                                        params.GetObjectId(),
                                        params.property))
    print(r)

def write_test(url:str=test_url_3, value:str="65"):
    params = parse.ParseBacnetPtKey(url)
    print("setting:", params.address, params.GetObjectId(), params.property, value)

    r = asyncio.run(server.WriteProperty(params.address,
                                    params.GetObjectId(),
                                    params.property, 
                                    value))
    print(r)

def sequential_read_test():
    # parse a url
    params = parse.ParseBacnetPtKey(test_url_1)
    print("getting:", params.address, params.GetObjectId(), params.property)

    r1 = asyncio.run(server.ReadProperty(params.address,
                                          params.GetObjectId(),
                                          params.property))
    print(r1)
    
    params = parse.ParseBacnetPtKey(test_url_2)
    print("getting:", params.address, params.GetObjectId(), params.property)

    r2 = asyncio.run(server.ReadProperty(params.address,
                                          params.GetObjectId(),
                                          params.property))
    print(r2)


def sequential_write_test() -> str:
    # parse the url 
    params = parse.ParseBacnetPtKey(test_url_3)

    print("getting:", params.address, params.GetObjectId(), params.property)
    r1 = asyncio.run(server.ReadProperty(params.address,
                                          params.GetObjectId(),
                                          params.property))
    print(test_url_3, "->", r1)
    
    value = 69
    print("setting:", params.address, params.GetObjectId(), params.property)
    r2 = asyncio.run(server.WriteProperty(params.address,
                                          params.GetObjectId(),
                                          params.property,
                                          value))
    print(test_url_3, "<-", r2)
    
    print("getting:", params.address, params.GetObjectId(), params.property)
    r3 = asyncio.run(server.ReadProperty(params.address,
                                          params.GetObjectId(),
                                          params.property))
    print(test_url_3, "->", r3)


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

def invalid_keys_test():
    invalid_key_results = {}
    print("X before:", invalid_key_results)
    asyncio.run(DictInvalidKeys(invalid_key_results))
    print("X after:", invalid_key_results)

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

def parse_and_get_test():
    # capture the resolved bacnet configuration
    bacnet_configs = []
    for uri in test_urls:
        config = parse.ParseBacnetPtKey(uri)
        if config.is_valid:
            bacnet_configs.append(config)

    # create a tuple of the information needed to read a bacnet property
    args = []
    for c in bacnet_configs:
        args.append((c.address, c.object_identifier, c.property))
    
    # you can request it in an ordered list, or
    ordered_results = []
    print("ordered_results before:", ordered_results)
    asyncio.run(server.StashMultiple(
        X=ordered_results,
        func=server.ReadProperty,
        args=args,
    ))
    print("ordered_results after:", ordered_results)
    print()

    # you can request it be stored in a dict
    unordered_results = {}
    print("unordered_results before:", unordered_results)
    asyncio.run(server.StashMultiple(
        X=unordered_results,
        func=server.ReadProperty,
        args=args,
        keys=test_point_ids
    ))
    print("unordered_results after:")
    [print(k,"->", v) for k, v in unordered_results.items()]
    

if __name__ == "__main__":
    read_test(test_url_4)

    write_test(test_url_4, 80)

    read_test(test_url_4)
    # sequential_read_test()
    # result = asyncio.run(GetAsyncValue())
    # print("single result:", result)

    # ordered_results = list_stash_test()
    # print("ordered results:", ordered_results)
    
    # unordered_results = dict_stash_test()
    # print("unordered results:", unordered_results)

    # invalid_keys_test()
    # # should get two lines or errors saying len(keys) != len(args)

    # valid_keys_test()
    # valid_args_test()
    # parse_and_get_test()
    
    # sequential_write_test()