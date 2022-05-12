from bs4 import BeautifulSoup
import requests

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape(self, params, headers=None):
        url = self.get_final_url(params)
        self.soup = self.get_soup_for_url(url, headers)
        return self.process_soup()

    def get_final_url(self, params):
        raise Exception("Unimplemented in Base class!")

    def process_soup(self):
        raise Exception("Unimplemented in Base class!")

    def get_soup_for_url(self, url, headers=None):
        resp = requests.get(url, headers=headers, verify=False)
        if resp.ok:
            return BeautifulSoup(resp.text, 'html.parser')
        else:
            print (resp.text)
            print ("No soup for you: ", url)

        return None


    def get_divs_with_class(self, css_class, trim=True):
        divs = self.soup.find_all('div', css_class)
        if trim:
            return [s.text.replace(':','').strip() for s in divs]
        else:
            return divs
