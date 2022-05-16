from connectors.cage.cage_report_connector import CageReportConnector
from commons.company_profile import CompanyProfile
from commons.teammember import TeamMember
import pandas as pd
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sys

def get_team_members(lst):
    tms = [{'name': x, 'gender': '', 'ethnicity': ''} for x in lst]
    return tms

def convert_to_dto(duns_num, incoming_dict):
    if not incoming_dict:
        incoming_dict = dict()

    c = CompanyProfile({
            'dunsNum' : duns_num,
            'name' : incoming_dict.get('Name of Firm', None),
            'website' : incoming_dict.get('E-Commerce Website', None),
            'address' : incoming_dict.get('Address, line 1', None),
            'team' :  get_team_members(incoming_dict.get('names', [])),
            'certifications' : incoming_dict.get('Ownership and Self-Certifications', '').split(', '),
            'status' : incoming_dict.get('Status', None),
            'lastUpdated' : incoming_dict.get('This profile was last updated', None)
        })
    return c

def extract_company_profile_single(d):
    c = CageReportConnector()
    try:
        tmp_dict = c.scrape(d)
        return convert_to_dto(d, tmp_dict)
        ##time.sleep(1)
    except Exception as ex:
        print (ex)
        print ("Ignoring for: ", d)
        

    return None


def extract_company_profile(duns_numbers):
    company_profiles = []
    c = CageReportConnector()
    for d in duns_numbers:
        try:
            tmp_dict = c.scrape(d)
            if tmp_dict:
                company_profiles.append(convert_to_dto(d, tmp_dict))
            ##time.sleep(1)
            print ("Done ", str(d))
        except Exception as ex:
            print (ex)
            print ("Ignoring for ",str(d))
        

    return company_profiles

if __name__=="__main__":
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    orig_df = pd.read_excel('data/Original_Data.xlsx')
    df = orig_df[start-1:end-1].copy()
    df['dunsNum'] = df['dunsNum'].apply(str)

    company_profiles = extract_company_profile(df['dunsNum'].values)
    cage_df = pd.DataFrame(columns=CompanyProfile.__annotations__.keys())
    for c in company_profiles:
        if c is not None:
            cage_df = cage_df.append(c.__dict__, ignore_index=True)

    cage_df.to_csv('data/cage_report_company_profile_{0}_{1}.csv'.format(start,end), mode='a',index=False)
