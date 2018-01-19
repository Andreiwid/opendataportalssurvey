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
pages_per_request = 100 #number of datasets returned per request. OPENDATASOFT max 100

#input file
urls = pd.read_csv(r'C:\temp\catsidentified_noduplication.csv', delimiter=';', encoding='latin-1' )

#output files
file_results = open(r'C:\temp\results_ODSOFT.csv',encoding='utf-8',mode='w') 
file_results.write('DATETIME;ID;DATASET_ID;DATASET_LASTMODIFIED\n')
file_errors = open(r'C:\temp\errors_ODSOFT.csv',encoding='utf-8',mode='w') 
file_errors.write('ID;SOURCE;URL;COUNTRY;PRODUCT;ERROR_MESSAGE\n')

print('records: ' + str(len(urls)))
print('start: ' + str(datetime.datetime.now()))

for x, row_url in urls.iterrows():
    if row_url['PRODUCT'] == 'OPENDATASOFT':
        #set default values to iterate pages
        next_record_to_request = 0 #DOT NOT change. Start with 0 zero
        has_more_pages = True #DOT NOT change
        tries = 1 #DOT NOT change
        
        while has_more_pages:
            try:
                url = row_url['URL'] + '/api/v2/catalog/datasets?rows=' + str(pages_per_request) + '&start=' + str(next_record_to_request) + '&pretty=false&include_app_metas=false'
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
                tries = 1 #DOT NOT change
                dataset_info = json_normalize(response_dict['datasets'])

                if dataset_info.empty:
                    has_more_pages = False
                else:
                    for y, row_dataset in dataset_info.iterrows():
                        file_results.write(str(datetime.datetime.now()) + ';' + str(row_url['ID']) + ';' +  str(row_dataset['dataset.dataset_id']) + ';' +  str(row_dataset['dataset.metas.default.modified']) + '\n')

                    if dataset_info.shape[0] < pages_per_request:
                        has_more_pages = False
                    else:
                        next_record_to_request = next_record_to_request + pages_per_request

file_results.close()
file_errors.close()
print('end: ' + str(datetime.datetime.now()))
