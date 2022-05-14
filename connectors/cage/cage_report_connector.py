from base_connector import BaseConnector


class CageReportConnector(BaseConnector):
    base_url = 'https://cage.report/DUNS'

    def __init__(self):
        super().__init__(self.base_url)

    def get_final_url(self, params):
        return self.base_url + '/' + params

    def process_soup(self):
        keys = self.get_divs_with_class('profilehead')
        values = self.get_divs_with_class('profileinfo')
        tmp_map = dict(zip(keys, values))

        ##Names
        names_content = self.get_divs_with_class('indent_same_as_profilehead')
        if names_content:
            tmp_map['names'] = names_content[1].split('\\n')

        return tmp_map


if __name__ == "__main__":
    c = CageReportConnector()
    print (c.scrape('45097789'))
