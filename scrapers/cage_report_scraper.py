from base_scraper import BaseScraper


class CageReportScraper(BaseScraper):
    base_url = 'https://cage.report/DUNS'

    def __init__(self):
        super().__init__(self.base_url)

    def get_final_url(self, params):
        return self.base_url + '/' + params

    def process_soup(self):
        keys = self.get_divs_with_class('profilehead')
        values = self.get_divs_with_class('profileinfo')
        return dict(zip(keys, values))


if __name__ == "__main__":
    c = CageReportScraper()
    print (c.scrape('806933284'))
