import time
import datetime
import urllib.request
import ssl
import json
import pandas as pd
from pandas.io.json import json_normalize

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

max_tries = 10 #define max number of tries in case of errors
pages_per_request = 100 #number of datasets returned per request --> CKAN max=1000

#input file
urls = pd.read_csv(r'C:\temp\catsidentified_noduplication.csv', delimiter=';', encoding='latin-1')

#output files
file_results = open(r'C:\temp\results_CKAN.csv',encoding='utf-8',mode='w') 
file_results.write('DATETIME;ID;DATASET_ID;DATASET_LASTMODIFIED;PRIVATE\n')
file_errors = open(r'C:\temp\errors_CKAN.csv',encoding='utf-8',mode='w') 
file_errors.write('ID;SOURCE;URL;COUNTRY;PRODUCT;ERROR_MESSAGE\n')

print('records: ' + str(len(urls)))
print('start: ' + str(datetime.datetime.now()))

for x, row_url in urls.iterrows():
    if row_url['PRODUCT'] == 'CKAN':
        #set default values to iterate pages
        next_record_to_request = 0 #DOT NOT change. Start with 0 zero
        has_more_pages = True #DOT NOT change
        tries = 1 #DOT NOT change
        dataset_info = pd.DataFrame #variable to controll offset bug (see bermuda.io). DOT NOT change

        dataset_count = 1
        
        while has_more_pages:
            try:
                url = row_url['URL'] + '/api/action/package_search?rows=' + str(pages_per_request) + '&start=' + str(next_record_to_request)
                print(str(x+1) + ' ' + url, end=' ')

                req = urllib.request.Request(
                    url, 
                    data=None, 
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                    }
                )
                resp = urllib.request.urlopen(req, timeout=60, context=ctx)
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
                tries = 1 #DOT NOT change
                
                #condition to verify difference in dictionaries. See http://data.london.gov.uk for an example
                if 'result' in response_dict['result']:
                    dataset_info_current = json_normalize(response_dict['result']['result'])
                else:
                    dataset_info_current = json_normalize(response_dict['result']['results'])
                
                #condition to controll offset bug (see bermuda.io)
                if dataset_info_current.equals(dataset_info) == True:
                    has_more_pages = False
                else:
                    dataset_info = dataset_info_current

                    if dataset_info.empty:
                        has_more_pages = False
                    else:
                        for y, row_dataset in dataset_info.iterrows():
                            file_results.write(str(datetime.datetime.now()) + ';' + str(row_url['ID']) + ';' +  str(row_dataset['id']) + ';' + str(row_dataset['metadata_modified']) + ';' + (str(row_dataset['private']) if 'private' in row_dataset else '*') + '\n')
                            dataset_count = dataset_count + 1
                        
                        if dataset_count >= int(response_dict['result']['count']):
                            has_more_pages = False
                        else:
                            next_record_to_request = next_record_to_request + pages_per_request

                        #show progress bar
                        print(str(dataset_count - 1) + '/' + str(response_dict['result']['count']))

file_results.close()
file_errors.close()
print('end: ' + str(datetime.datetime.now()))
