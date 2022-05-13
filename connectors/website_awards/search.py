from commons.google_search_wrapper import do_search_only10
from commons import utils
from models import AwardsModel
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

awards_model = AwardsModel()

def extractWeblinks(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}/'.format(uri=parsed_uri)
    print(domain)
    reqs = requests.get(url, headers=utils.get_headers())
    print(reqs)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        if link.get('href') is not None:
            if "award" in  link.get('href').lower() or  "certification"  in  link.get('href').lower():
                if link.get('href') not in urls:
                    urls.append(link.get('href'))
            #if "about" in link.get('href').lower() or  "story" in link.get('href').lower():
            #    if link.get('href') not in urls:
            #        urls.append(link.get('href'))
    return urls

def extract_entities(companywithaddress):
    items = do_search_only10(companywithaddress+' website')
    weblinks = extractWeblinks(items[0]['link'])
    for link in weblinks:
        print (link)
        extractedText = utils.extract_text_from_url(link);
        entities = awards_model.predict_single(extractedText)

extract_entities('EXECUTEAM CORPORATION')
