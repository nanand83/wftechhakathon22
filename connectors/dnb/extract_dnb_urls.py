from commons.google_search_wrapper import do_search_only10,do_search_only10_srs
import pandas as pd
import time


orig_df = pd.read_excel('../../data/Original_Data.xlsx')
df = orig_df[0:6000].copy()


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


df['DNB_LINK'] = df['dunsName'].apply(get_dnb_url)
df[['dunsNum','dunsName','DNB_LINK']].to_csv('./dnb_links_6k.csv',index=False)

#print (get_dnb_url('Russell Transport, Inc.'))
