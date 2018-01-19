import datetime
import time
import urllib.request
import ssl
import json
import pandas as pd
from pandas.io.json import json_normalize

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

max_tries = 10 #define max number of tries in case of errors
pages_per_request = 1000 #number of datasets returned per request

#input file
urls = pd.read_csv(r'C:\temp\catsidentified_noduplication.csv', delimiter=';', encoding='latin-1' )

#output files
file_results = open(r'C:\temp\results_SOCRATA.csv',encoding='utf-8',mode='w') 
file_results.write('DATETIME;ID;DATASET_ID;DATASET_LASTMODIFIED\n')
file_errors = open(r'C:\temp\errors_SOCRATA.csv',encoding='utf-8',mode='w') 
file_errors.write('ID;SOURCE;URL;COUNTRY;PRODUCT;ERROR_MESSAGE\n')

print('records: ' + str(len(urls)))
print('start: ' + str(datetime.datetime.now()))

for x, row_url in urls.iterrows():
    if row_url['PRODUCT'] == 'SOCRATA':
        #set default values to iterate pages
        has_more_pages = True #DOT NOT change
        last_dataset_id = ''
        
        tries = 1 #DOT NOT change
        
        while has_more_pages:
            try:
                url = row_url['URL']
                domain = url[url.find('//') + 2:]
                
                url = row_url['URL'] + '/api/catalog/v1?only=dataset&domains=' + domain + '&search_context=' + domain + '&limit=' + str(pages_per_request) + '&scroll_id=' + last_dataset_id
                print(str(x+1) + ' ' + url)

                req = urllib.request.Request(
                    url, 
                    data=None, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    }
                )
                resp = urllib.request.urlopen(req, timeout=20, context=ctx)
                response_dict = json.loads(resp.read())

            except Exception as e: #raises HTTP, URL and refused connection errors
                print('ERRO: ' + url + ' ' + str(e))
                if tries <= max_tries:
                    wait_time = tries * 10
                    tries = tries + 1

                    print('RETRY IN ' + str(wait_time) + 'sec ' + url)
                    
                    time.sleep(wait_time)
                else:
                    print('ABORTING: ' + url)
                    #record a log of erros
                    file_errors.write(str(row_url['ID']) + ';' + str(row_url['SOURCE']) + ';' + str(row_url['URL']) + ';' + str(row_url['COUNTRY']) + ';' + str(row_url['PRODUCT']) + ';' + str(e) + '\n')
                    break
                    
            else:
                dataset_info = json_normalize(response_dict['results'])

                if dataset_info.empty:
                    has_more_pages = False
                else:
                    for y, row_dataset in dataset_info.iterrows():
                        file_results.write(str(datetime.datetime.now()) + ';' + str(row_url['ID']) + ';' +  str(row_dataset['resource.id']) + ';' +  str(row_dataset['resource.updatedAt']) + '\n')
                        last_dataset_id = str(row_dataset['resource.id'])
                        
                    if dataset_info.shape[0] < pages_per_request:
                        has_more_pages = False

file_results.close()
file_errors.close()
print('end: ' + str(datetime.datetime.now()))
