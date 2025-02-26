import client as c

def driver_get_test(key:str):
    values = c.Get(key, addr="localhost:50062")
    print(values)
    # print("{} -> '{}'".format(key, values[key]))

def set_test(key:str, value:str):
    ok = c.Set(key, value)
    print("{} <- '{}' ({})".format(key, value, ok))

def get_multiple_test(keys:list[str]):
    res = c.GetMultiple(keys)
    for r in res:
        print("{} -> '{}'".format(r.Key, r.Value))

if __name__=="__main__":
    c.devCtrlAddr = "localhost:2822"

    # key1 = "bos://localhost/dev/3/pts/4" # temp
    # key2 = "bos://localhost/dev/3/pts/5" # humid
    # key3 = "bos://localhost/dev/3/pts/6" # co2
    # key4 = "bos://localhost/dev/4/pts/1" # temp
    xref1 = "bacnet://192.168.13.147/40100/analog-input,3/present-value"
    xref2 = "bacnet://192.168.13.147/40100/analog-input,12/present-value"

    driver_get_test(xref1)
    driver_get_test(xref2)

    # get_multiple_test([key2, key3])

    # get_test(key4)
    # set_test(key4, str(82))
    # get_test(key4)


