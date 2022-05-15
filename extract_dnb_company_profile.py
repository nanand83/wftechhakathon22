from connectors.dnb.search import extract_html
from commons.company_profile import CompanyProfile
from commons.teammember import TeamMember
import pandas as pd
import time
from commons.google_search_wrapper import do_search_only10,do_search_only10_srs
import sys

def convert_to_dto(each_row, url, incoming_list):
    if len(incoming_list) > 0:
        c = CompanyProfile({
                'dunsNum' : each_row['dunsNum'],
                'name' : each_row['dunsName'],
                'website' : url,
                'address' : None,
                'team' : [TeamMember(x) for x in incoming_list],
                'certifications' : list(),
                'status' : None,
                'lastUpdated' : None
            })
    return c


def get_dnb_url(company_name):
    time.sleep(1)
    #results = do_search_only10_srs(company_name, 'https://www.dnb.com/')
    results = do_search_only10(company_name + ' DNB Business Directory')
    
    if results and results[0]['link'].startswith('https://www.dnb.com'):
        print (results[0]['link'])
        return results[0]['link']
    else:
        print ("Nothing found for ", company_name)
        return None

#print (get_dnb_url('Russell Transport, Inc.'))

def extract_company_profile(df):
    company_profiles = []
    for idx, each_row in df.iterrows():
        dnb_url = get_dnb_url(each_row['dunsName'])
        if dnb_url and dnb_url != 'https://www.dnb.com':
            dnb_data = extract_html(dnb_url)
            company_profiles.append(convert_to_dto(each_row, dnb_url, dnb_data))
        
        ##time.sleep(1)
        print ("-------------------Done extracting for ", each_row['dunsName'])

    return company_profiles


if __name__ == "__main__":
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    orig_df = pd.read_excel('data/Original_Data.xlsx')
    df = orig_df[start-1:end-1].copy()
    df['dunsNum'] = df['dunsNum'].apply(str)

    company_profiles = extract_company_profile(df)
    dnb_df = pd.DataFrame(columns=CompanyProfile.__annotations__.keys())
    for c in company_profiles:
        dnb_df = dnb_df.append(c.__dict__, ignore_index=True)

    dnb_df.to_csv('data/dnb_report_company_profile_{0}_{1}.csv'.format(start, end), index=False)
