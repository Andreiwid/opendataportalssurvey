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
pages_per_request = 1000 #number of datasets returned per request

#input file
urls = pd.read_csv(r'C:\temp\catsidentified_noduplication.csv', delimiter=';', encoding='latin-1' )

#output files
file_results = open(r'C:\temp\results_ARCGIS.csv',encoding='utf-8',mode='w') 
file_results.write('DATETIME;ID;DATASET_ID;DATASET_LASTMODIFIED\n')
file_errors = open(r'C:\temp\errors_ARCGIS.csv',encoding='utf-8',mode='w') 
file_errors.write('ID;SOURCE;URL;COUNTRY;PRODUCT;ERROR_MESSAGE\n')
file_unavailable = open(r'C:\temp\unavailable_ARCGIS.csv',encoding='utf-8',mode='w') 
file_unavailable.write('URL\n')

print('records: ' + str(len(urls)))
print('start: ' + str(datetime.datetime.now()))

for x, row_url in urls.iterrows():
    if row_url['PRODUCT'] == 'ARCGIS':
        #set default values to iterate pages
        next_page_to_request = 1 #DOT NOT change
        has_more_pages = True #DOT NOT change
        tries = 1 #DOT NOT change
    
        #verify if site still available when it is redirected to hub.arcgis.com
        url = str(row_url['URL'])

        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        resp = urllib.request.urlopen(req, timeout=20, context=ctx)
    
        if resp.geturl().find('hub.arcgis.com') > -1:
            print(str(x+1) + ' UNAVAILABLE ' + url)
            file_unavailable.write(url + '\n')
            continue

        while has_more_pages:
            try:
                url = row_url['URL'] + '/data.json?page=' + str(next_page_to_request) + '&per_page=' + str(pages_per_request)
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
                dataset_info = json_normalize(response_dict['dataset'])
                tries = 1 #DOT NOT change

                if dataset_info.empty:
                    has_more_pages = False
                else:
                    for y, row_dataset in dataset_info.iterrows():
                        dataset_id = str(row_dataset['identifier'])
                        dataset_id = dataset_id[dataset_id.find('dataset') + 9:]

                        file_results.write(str(datetime.datetime.now()) + ';' + str(row_url['ID']) + ';' +  dataset_id + ';' +  str(row_dataset['modified']) + '\n')

                    if dataset_info.shape[0] < pages_per_request:
                        has_more_pages = False
                    else:
                        next_page_to_request = next_page_to_request + 1
                

file_results.close()
file_errors.close()
file_unavailable.close()
print('end: ' + str(datetime.datetime.now()))
