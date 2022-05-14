from connectors.cage.cage_report_connector import CageReportConnector
from commons.company_profile import CompanyProfile
import pandas as pd
import time

def convert_to_dto(duns_num, incoming_dict):
    c = CompanyProfile({
            'dunsNum' : duns_num,
            'name' : incoming_dict.get('Name of Firm', None),
            'website' : incoming_dict.get('E-Commerce Website', None),
            'address' : incoming_dict.get('Address, line 1', None),
            'team' : incoming_dict.get('names', []),
            'certifications' : incoming_dict.get('Ownership and Self-Certifications', '').split(', '),
            'status' : incoming_dict.get('Status', None),
            'lastUpdated' : incoming_dict.get('This profile was last updated', None)
        })
    return c


def extract_company_profile(duns_numbers):
    company_profiles = []
    c = CageReportConnector()
    for d in duns_numbers:
        tmp_dict = c.scrape(d)
        if tmp_dict:
            company_profiles.append(convert_to_dto(d, tmp_dict))
        
        ##time.sleep(1)

    return company_profiles


df = pd.read_excel('data/Original_Data.xlsx')
df['dunsNum'] = df['dunsNum'].apply(str)
company_profiles = extract_company_profile(df['dunsNum'].values)
cage_df = pd.DataFrame(columns=CompanyProfile.__annotations__.keys())
for c in company_profiles:
    cage_df = cage_df.append(c.__dict__, ignore_index=True)

cage_df.to_csv('data/cage_report_company_profile.csv', mode='a',index=False)
