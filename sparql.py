from SPARQLWrapper import SPARQLWrapper, JSON

import parse

QUERY_ENDPOINT = "http://localhost:7878/query" 
point_fmt = "bos://{}/bos/dev/{}/pts/{}"
host = "localhost"

def PointUriFmt(pt:str, host:str='localhost') -> str:
    parts = pt.split(".")
    if len(parts) != 2:
        return "error: invalid point id {}".format(pt)
    return point_fmt.format(host, parts[0], parts[1])

def GetUnionedSubClauses(sub_clauses) -> str:
    return "UNION ".join(sub_clauses)

def GetQuery(points) -> str:
    sub_clauses = []
    for p in points:
        point_uri = PointUriFmt(p)
        sub_clauses.append(SUB_CLAUSE_FMT.format(point_uri, XREF_PREDICATE))

    unioned_sub_clauses = GetUnionedSubClauses(sub_clauses=sub_clauses)
    return QUERY_FMT.format(unioned_sub_clauses)

def ExtractTriple(row):
    pass

XREF_PREDICATE = "https://openbos.org/schema/bos#ExternalReference"

# takes two format inputs the point id and the xref predicate
QUERY_FMT = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?sub ?pred ?obj WHERE {{ 
    {}
}} ORDER BY ?sub  
"""

SUB_CLAUSE_FMT = """{{
    ?sub ?pred ?obj .
    <{}> <{}> ?obj .
}}
"""

def RowToTuple(row) -> tuple[str, parse.BACnetPtParams]:
    point_uri = row['sub']['value']
    point = parse.ParseBosPoint(point_uri)
    bacnet_uri = row['obj']['value']
    bacnet_params = parse.ParseBacnetPtKey(bacnet_uri)
    return (point, bacnet_params)


def GetBacnetPtParams(points:str|list[str]) -> list[tuple[str, parse.BACnetPtParams]]:
    """ Accepts either a list of points or a single point str
    """
    if type(points) is str:
        points = [points]

    sparql = SPARQLWrapper(QUERY_ENDPOINT)
    sparql.setReturnFormat(JSON)

    query = GetQuery(points)
    sparql.setQuery(query)

    pairs = []
    try:
        ret = sparql.queryAndConvert()
        for r in ret["results"]["bindings"]:
           pairs.append(RowToTuple(r))
    except Exception as e:
        print(e)
    return pairs


if __name__ == "__main__":
    points = ["2.1", "3.1"]

    # sub_clauses = []
    # for p in points:
    #     point_uri = PointUriFmt(p)
    #     sub_clauses.append(SUB_CLAUSE_FMT.format(point_uri, XREF_PREDICATE))

    # unioned_sub_clauses = GetUnionedSubClauses(sub_clauses=sub_clauses)
    bacnet_pt_params = GetBacnetPtParams(points)
    print(bacnet_pt_params)

