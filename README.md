# Repository of the paper "Investigating open data portals automatically: a methodology and some illustrations"
This is the official repository of the paper entitled _"Investigating open data portals automatically: a methodology and some illustrations"_. If you are interested in understanding what this repository contains, we suggest you first read the paper at _unpublished yet - wait link_.
Here you can find all algorithms and data produced during the paper development, thus readers can check our experiments and reproduce results. Authors expect this paper and all its underlying artifacts help to grow Open Data Community and improve the use of Open Data worldwide.
To run all the experiments, we relied on Python and Microsoft SQL Server database. Python codes and SQL scripts are fully specified in this repository. We also made available CSVs files containing the database dump of the MS-SQL Server. 
Below are some explanation about all files:
## catsall.csv
This is the source of all 4,019 URLs gathered from 7 different repositories prior to the identification of products/platforms. Refer to Section 4.2 of the paper. We have made a lot of adjustments to right identify the location at country level of data portals according to ISO3166 (see support file **iso3166.csv**).
## catsidentified_withduplication.csv
This is the same content of **catsall.csv** plus the identified product/platform obtained after running **identifyproduct.py**. 
## catsidentified_noduplication.csv
The same as **catsidentified_withduplication.csv** but with no duplication of URLs. We have made manual checking to avoid duplication and URL variations that pointed to the same data portal. We ended up 3,152 unique URLs of data portals.
## iso3166.csv
Support file used to adjust the location of data portals URLs. We got base data by copying and pasting the table content from Wikipedia article https://en.wikipedia.org/wiki/ISO_3166-1.
## datasets.zip
A compressed version of datasets.csv (GitHub doesn’t allow files larger than 100MB).  Contains all the datasets extracted from identified CKAN, Socrata, ArcGIS and OpenDataSoft platforms. 
## identifyproduct.py
Python code to identify what product/platform of a given data portal. The code reads a CSV file with URLs of data portals and logs the results in the console. This code is discussed in the 4.3 of the paper.
## CKAN_extractdatasets.py
## SOCRATA_extractdatasets.py
## ARCGIS_extractdatasets.py 
## ODSOFT_extractdatasets.py
Python codes to extract datasets specifically from different products/platforms. Each product/platform is specified at the beginning of .py file name. The code essentially reads a CSV file with URLs of data portals and logs the results in different CSV files, depending on the type of product/platform.
## table1.sql
## table6.sql
## table7.sql
## table8.sql
## table10.sql
SQL scripts used to extract data from database. We also used a lot of Excel to better formats tables and specify percentage numbers.
