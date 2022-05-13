from commons.google_search_wrapper import do_search_only10
from connectors.website_awards.extract_weblinks_on_website import  extractWeblinks
from connectors.website_awards.extract import extractData
import spacy
def callGoogleSearch(companywithaddress):
    items = do_search_only10(companywithaddress+' website')
    print(items)
    return items[0]['link']

def callGetWebLinks(baseweblink):
    urls = extractWeblinks(baseweblink)
    print(urls)
    return urls

entities_detected=[]

def extractWeblink(weblinks):
    for link in weblinks:
        extractedText = extractData(link);
        nlp_updated = spacy.load('../../commons/output/awards')
        doc = nlp_updated(extractedText)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

extractWeblink(callGetWebLinks(callGoogleSearch('Essex Group Management Corp.')))