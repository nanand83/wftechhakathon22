from commons.google_search_wrapper import do_search_only10
from connectors.website_awards.extract_weblinks_on_website import  extractWeblinks
def callGoogleSearch(companywithaddress):
    items = do_search_only10(companywithaddress)
    print(items)
    return items[0]['link']

def callGetWebLinks(baseweblink):
    extractWeblinks(baseweblink)

#callGetWebLinks(callGoogleSearch('CP&y, Inc. Dallas 1820 REGAL ROW STE 200 DALLAS TX 75235 website_awards'))
callGetWebLinks(callGoogleSearch('EXECUTEAM CORPORATION'))
#callGetWebLinks(callGoogleSearch('Magnolia River Services, Inc.	Morgan	408 BANK ST NE	DECATUR	AL	35601'))