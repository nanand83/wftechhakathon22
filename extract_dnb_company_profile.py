from connectors.dnb.search import extract_html
from commons.company_profile import CompanyProfile
from commons.teammember import TeamMember
import pandas as pd
import time
from commons.google_search_wrapper import do_search_only10,do_search_only10_srs
import sys

def convert_to_dto(each_row, url, incoming_data):
    #print (type(incoming_data), incoming_data)
    c = CompanyProfile({
            'dunsNum' : each_row['dunsNum'],
            'name' : each_row['dunsName'],
            'website' : url,
            'address' : '',
            'team' : incoming_data,
            'certifications' : [],
            'status' : '',
            'lastUpdated' : '' 
        })
    return c


def get_dnb_url(company_name):
    #time.sleep(1)
    #results = do_search_only10_srs(company_name, 'https://www.dnb.com/')
    results = do_search_only10(company_name + ' DNB Business Directory')
    
    if results and results[0]['link'].startswith('https://www.dnb.com'):
        #print (results[0]['link'])
        return results[0]['link']
    else:
        print ("Nothing found for ", company_name)
        return None

#print (get_dnb_url('Russell Transport, Inc.'))

def extract_company_profile_row(each_row):
    try:
        dnb_url = get_dnb_url(each_row['dunsName'])
        if dnb_url and dnb_url != 'https://www.dnb.com/':
            dnb_data = extract_html(dnb_url)
            #print (dnb_data)
            print ("-------------------Done DNB extracting for ", each_row['dunsName'])
            return convert_to_dto(each_row, dnb_url, dnb_data)
        ##time.sleep(1)
    except:
        print ("Ignoring") 

    return None


def extract_company_profile(df):
    company_profiles = []
    for idx, each_row in df.iterrows():
        try:
            dnb_url = get_dnb_url(each_row['dunsName'])
            if dnb_url and dnb_url != 'https://www.dnb.com/':
                dnb_data = extract_html(dnb_url)
                company_profiles.append(convert_to_dto(each_row, dnb_url, dnb_data))
            
            ##time.sleep(1)
            print ("-------------------Done extracting for ", each_row['dunsName'])
        except Exception as ex:
            print (ex)
            print ("Ignoring for idx:", str(idx))

    return company_profiles


if __name__ == "__main__":
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    orig_df = pd.read_excel('data/Original_Data.xlsx')
    df = orig_df[start-1:end-1].copy()
    df['dunsNum'] = df['dunsNum'].apply(str)

    #company_profiles = extract_company_profile(df)
    dnb_df = pd.DataFrame(columns=CompanyProfile.__annotations__.keys())

    for idx, each_row in df.iterrows():
        company_profile = extract_company_profile_row(each_row)
        if company_profile is not None:
            dnb_df = dnb_df.append(company_profile.__dict__, ignore_index=True)

    dnb_df.to_csv('data/dnb_report_company_profile_{0}_{1}.csv'.format(start, end), index=False)
