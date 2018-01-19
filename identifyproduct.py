#identify product/platform by API signature
import datetime
import urllib.request
import ssl
import json
import pandas as pd

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = pd.read_csv(r'C:\temp\catsall.csv', delimiter=';', encoding='latin-1' )
print(len(urls))
print('start: ' + str(datetime.datetime.now()))

for index, row in urls.iterrows():
    #configure products signature
    ckan_sig = '/api/action/site_read'
    socrata_sig = '/api/catalog/v1'
    arcgis_sig = '/api/v2'
    odsoft_sig = '/api/v2'
    catalog = 'none'
    
    ckan_error = False
    socrata_error = False
    arcgis_error = False
    odsoft_error = False

    #get redirected domain to verify duplicated URLs
    
    url_id = str(row['ID'])
    url = str(row['URL'])

    try:
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        resp = urllib.request.urlopen(req, timeout=20, context=ctx)
    except:
        print(url_id + ';' + url + ';;ERROR')
        continue
    else:
        domain = resp.geturl()
    
        #CKAN
        try:
            req = urllib.request.Request(
                url + ckan_sig, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            resp = urllib.request.urlopen(req, timeout=20, context=ctx)
        except Exception as e: #raises HTTP, URL and refused connection errors
            ckan_error = True
        else:
            try:
                response_dict = json.loads(resp.read())
            except ValueError: #raises JSON format error of a non-expected result (API not found)
                pass
            else:
                if 'success' in response_dict or 'help' in response_dict or 'result' in response_dict:
                    catalog = 'CKAN'

        #SOCRATA
        try:
            req = urllib.request.Request(
                url + socrata_sig, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            resp = urllib.request.urlopen(req, timeout=20, context=ctx)
        except: #raises HTTP, URL and refused connection errors
            socrata_error = True
        else:
            try:
                response_dict = json.loads(resp.read())
            except ValueError: #raises JSON format error of a non-expected result (API not found)
                pass
            else:
                if 'results' in response_dict:
                    catalog = 'SOCRATA'

        #ARCGIS
        try:
            req = urllib.request.Request(
                url + arcgis_sig, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            resp = urllib.request.urlopen(req, timeout=20, context=ctx)
        except: #raises HTTP, URL and refused connection errors
            arcgis_error = True
        else:
            try:
                response_dict = json.loads(resp.read())
            except ValueError: #raises JSON format error of a non-expected result (API not found)
                pass
            else:
                if 'datasets' in response_dict and domain.find('hub.arcgis.com') == -1:
                    catalog = 'ARCGIS'

        #OPENDATASOFT
        try:
            req = urllib.request.Request(
                url + odsoft_sig, 
                data=None,  
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            resp = urllib.request.urlopen(req, timeout=20, context=ctx)
        except: #raises HTTP, URL and refused connection errors
            odsoft_error = True
        else:
            try:
                response_dict = json.loads(resp.read())
            except ValueError: #raises JSON format error of a non-expected result (API not found)
                pass
            else:
                if 'links' in response_dict:
                    catalog = 'OPENDATASOFT'

        if ckan_error and socrata_error and arcgis_error and odsoft_error:
            print(url_id + ';' + url + ';' + domain + ';none')
        else:
            print(url_id + ';' + url + ';' + domain + ';' + catalog)

print('end: ' + str(datetime.datetime.now()))
