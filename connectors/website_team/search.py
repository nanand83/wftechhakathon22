from commons.google_search_wrapper import do_search_only10
from models.models import EthnicityOTSModel
from commons import utils
import spacy
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def extract_web_links_from_url(url):
    parsed_uri = urlparse(url)
    domainname = parsed_uri.netloc.split(".")[-2:]
    domain = 'http://'+".".join(domainname)
    reqs = requests.get(url, headers=utils.get_headers())
    #print(reqs)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        if link.get('href') is not None:
            if "director" in  link.get('href').lower() or  "team"  in  link.get('href').lower():
                if link.get('href') not in urls:
                    weblink = link.get('href');
                    if domain not in link.get('href'):
                        weblink = domain+link.get('href')
                    urls.append(weblink)
            #if "about" in link.get('href').lower() or  "story" in link.get('href').lower():
            #    if link.get('href') not in urls:
            #        urls.append(link.get('href'))
    return urls


def extract(company_name):
    entities_detected=[]
    names_detected=[]
    results = do_search_only10(company_name + ' website')

    if results:
        for link in extract_web_links_from_url(results[0]['link']):
            extractedText = utils.extract_text_from_url(link);
            print(extractedText)
            nlp_updated = spacy.load('en_core_web_sm')
            doc = nlp_updated(extractedText)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            for ent in doc.ents:
               if 'PERSON' in ent.label_:
                   names_detected.append(ent.text)
            print (names_detected)
            result = EthnicityOTSModel().predict_batch_by_lastname(names_detected)
            print(result)

    return None


extract('Ologie, LLC')

