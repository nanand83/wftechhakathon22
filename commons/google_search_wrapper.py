import requests
from googlesearch import search

#Keys
api_key = 'AIzaSyDjOAgYbw_ixUU6fX4l7wwAaO1oYpxydB0'
cx = 'e54032988e341ae22'

#Statics
url = 'https://customsearch.googleapis.com/customsearch/v1'
site_restricted_url = 'https://www.googleapis.com/customsearch/v1/siterestrict'


headers = {
    'Accept' : 'application/json',
}

query_params = {
    'key': api_key,
    'cx': cx,
    'num' : 10
}

'''
Uses Custom Search JSON API and performs Google Search for incoming query and returns top 10 results.
Args:
    query term to search for
Returns:
    List of dict of results
    None if no results found
'''
def do_search_only10(query):
    query_params['q'] = query
    try:
        resp = requests.get(url, headers=headers, params=query_params)
        if resp.ok:
            resp_json = resp.json()
            if 'items' in resp_json:
                return resp_json['items']
        else:
            print ("Failed for query ", query)
    except Exception as ex:
        print ("Something went wrong with search: ", ex)

    return None

'''
Uses Site Restricted Search (SRS) JSON API and performs Google Search for incoming query and returns top 10 results.
Args:
    query term to search for
Returns:
    List of dict of results
    None if no results found
'''
def do_search_only10_srs(query, domain):
    query_params = {
        'siteSearchFilter' : 'i'
    }

    query_params['q'] = query
    query_params['siteSearchFilter'] = 'i'
    query_params['siteSearch'] = domain

    try:
        resp = requests.get(site_restricted_url, headers=headers, params=query_params)
        if resp.ok:
            resp_json = resp.json()
            if 'items' in resp_json:
                return resp_json['items']
        else:
            print ("Failed for query ", query)
    except Exception as ex:
        print ("Something went wrong with search: ", ex)

    return None



def do_search_only10_v2(query,query_params):
    query_params['q'] = query
    try:
        resp = requests.get(url, headers=headers, params=query_params)
        if resp.ok:
            resp_json = resp.json()
            if 'items' in resp_json:
                return resp_json['items']
        else:
            print("Failed for query ", query)
    except Exception as ex:
        print("Something went wrong with search: ", ex)

    return None
'''
Performs traditional requests based search and does not use Custom Search API.
Use this for adhoc search and results.
NOTE: If you hit as batch, this search will fail as Google start blocking us with 429 - Too many requests!!
Args:
    query term to search for
Returns:
    List of dict of results
    None if no results found
'''
def do_adhoc_search(query):
    results = []
    try:
        tmp_results = search(query, tld='com', num=2, stop=10, pause=10.)
        results = [t for t in tmp_results]
    except Exception as ex:
        print ("Something went wrong with search: ", ex)

    return results



if __name__ == "__main__":
    items = do_search_only10("CP&y, Inc. leadership")
    print (items[0])

    #adhoc_items = do_adhoc_search("CP&y, Inc. leadership")
    #print (adhoc_items[0])
    #print (len(adhoc_items))
