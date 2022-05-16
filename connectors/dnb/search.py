from commons.google_search_wrapper import do_search_only10
from commons import utils
from models import AwardsModel
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from ethinicity_classification import identifyEthinicity
from gender_classification import getGender
import time
import json
import random

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('user-agent={0}'.format(random.choice(utils.user_agent_list)))
#chrome_options.add_argument('user-agent={0}'.format('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'))
chrome_options.add_argument('user-agent={0}'.format('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'))
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

awards_model = AwardsModel()

def extractWeblinks(url):
    #parsed_uri = urlparse(url)
    #domain = '{uri.netloc}/'.format(uri=parsed_uri)
    #print(domain)
    reqs = requests.get(url, headers=utils.get_headers())
    #print(reqs)
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

api_key = 'AIzaSyDjOAgYbw_ixUU6fX4l7wwAaO1oYpxydB0'
cx = 'e54032988e341ae22'
def extract_entities(companywithaddress):
    query_params = {
        'key': api_key,
        'cx': cx,
        'num': 10,
        'siteSearch' : 'https://www.dnb.com/',
        'siteSearchFilter' : 'i'
    }

    items = do_search_only10(companywithaddress ,query_params)
    #weblinks = extractWeblinks(items[0]['link'])
    #for link in weblinks:
    #    print (link)
    extractedText = extract_html(items[0]['link']);
    entities = awards_model.predict_single(extractedText)


def extract_html(url):
    time.sleep(2)
    driver =webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    search_url = url
    driver.get(search_url)
    output_list = []

    tries = 0
    max_tries = 6
    while (driver.title.lower() == "access denied" and tries < max_tries):
        driver.get(search_url)
        tries += 1
        time.sleep(2)
    
    print ("Page Title:", driver.title.lower())
    if driver.title.lower() == "access denied":
        print ("Unable to extract for ", url)
        driver.quit()
        return output_list


    #print (driver.find_element_by_xpath("/html").text)
    links = driver.find_element(by=By.CLASS_NAME, value='contacts-body')
    #links = driver.find_element(by=By.XPATH, value="//div[contains(@class, 'contacts-body')]")
    ul_list = links.find_element(by=By.TAG_NAME, value='ul')
    list_of_contacts = links.text.splitlines()
    mappeddata = list(zip(list_of_contacts[::2], list_of_contacts[1::2]))
    for data in mappeddata:
        output_list.append({
            'name' : data[0],
            'gender': getGender(data[0]),
            'ethnicity': identifyEthinicity(data[0])
        })
    driver.quit()
    #print ("Output list is ", output_list)
    return output_list


if __name__ == "__main__":
    extract_html('https://www.dnb.com/business-directory/company-profiles.skillnet_solutions_inc.70f4f1134a7ed06c700c4d197b4a0eaf.html')
    #extract_entities('Premier Oil & Gas Inc')
    #driver.get('https://google.com')
    #print (driver.title)
