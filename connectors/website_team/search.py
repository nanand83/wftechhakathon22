import json
import pandas as pd
from commons.google_search_wrapper import do_search_only10
from connectors.website_team.extract_weblinks_on_website import extractWeblinks
from connectors.website_team.extract import extractData
import spacy
from ethnicolr import pred_wiki_ln, pred_wiki_name

def callGoogleSearch(companywithaddress):
    items = do_search_only10(companywithaddress+' website')
    print(items)
    return items[0]['link']

def callGetWebLinks(baseweblink):
    urls = extractWeblinks(baseweblink)
    print(urls)
    return urls

entities_detected=[]
names_detected=[]
def extractWeblink(weblinks):
    for link in weblinks:
        extractedText = extractData(link);
        print(extractedText)
        nlp_updated = spacy.load('en_core_web_sm')
        doc = nlp_updated(extractedText)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        for ent in doc.ents:
           if 'PERSON' in ent.label_:
               names_detected.append({'name': ent.text})

        df = pd.DataFrame(names_detected)
        result = pred_wiki_ln(df,'name')
        print(result)
extractWeblink(callGetWebLinks(callGoogleSearch('Jenzabar, Inc.')))