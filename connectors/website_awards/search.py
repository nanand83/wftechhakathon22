from commons.google_search_wrapper import do_search_only10
from commons.utils import *
import spacy

def callGoogleSearch(companywithaddress):
    items = do_search_only10(companywithaddress+' website')
    print(items)
    return items[0]['link']

entities_detected=[]

def predict_entities(weblinks):
    for link in weblinks:
        extractedText = extractData(link);
        nlp_updated = spacy.load('../../commons/output/awards')
        doc = nlp_updated(extractedText)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

predict_entities(extract_web_links_from_url(callGoogleSearch('EXECUTEAM CORPORATION')))
