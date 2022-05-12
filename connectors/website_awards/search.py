from commons.google_search_wrapper import do_search_only10
from connectors.website_awards.extract_weblinks_on_website import  extractWeblinks
from connectors.website_awards.extract import extractData
def callGoogleSearch(companywithaddress):
    items = do_search_only10(companywithaddress+' website awards')
    print(items)
    return items[0]['link']

def callGetWebLinks(baseweblink):
    urls = extractWeblinks(baseweblink)
    print(urls)
    return urls

def extractWeblink(weblinks):
    for link in weblinks:
        extractData(link);

extractWeblink(callGetWebLinks(callGoogleSearch('EXECUTEAM CORPORATION')))