import requests

#Keys
api_key = 'AIzaSyDjOAgYbw_ixUU6fX4l7wwAaO1oYpxydB0'
cx = 'e54032988e341ae22'

#Statics
url = 'https://customsearch.googleapis.com/customsearch/v1'

headers = {
    'Accept' : 'application/json'
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


if __name__ == "__main__":
    items = do_search_only10("CP&y, Inc. leadership")
    print (len(items))
