from uspto.peds.client import UsptoPatentExaminationDataSystemClient 
client = UsptoPatentExaminationDataSystemClient()

#https://docs.ip-tools.org/uspto-opendata-python/peds.html
# https://m.blog.naver.com/sejeonpat/221476219847
expression = 'firstNamedApplicant:(nasa)'
filter = 'appFilingDate:[2000-01-01T00:00:00Z TO 2015-12-31T23:59:59Z]'
result = client.search(expression, filter=filter, sort='applId asc')

# result = client.download_document(type='patent', number='US20170293197A1', format='json')

for i in result["docs"][0]:
    print(i)

result["docs"][0]["appType"]

keys = ["applId", "patentTitle", "appFilingDate", "applicants", "firstNamedApplicant", "appType", "appClsSubClsFacet"]
result2 = {key: result["docs"][0][key] for key in keys}
result2

import pandas as pd

df = pd.read_csv("D:/Analysis/2021_Similarity/data/patent/patent.tsv", sep='\t') #https://patentsview.org/download/data-download-tables
df.head()

app = pd.read_csv("D:/Analysis/2021_Similarity/data/patent/application.tsv", sep='\t')
app.head()

import requests

response = requests.get("https://api.patentsview.org/patents/query?q={"_and":[{"inventor_last_name":"Whitney"},{"patent_date":"1981-10-06"}]}")
