import requests,json, pandas as pd, time,datetime,sys,xmltodict,re
from IICS_AUTH_PRE import SessionId,serverUrl


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

listofdfs = []
project ='DnA - Crawl Phase'
  #'DnA (Walk)/'
#### get list of folder paths to
url = f"{serverUrl}/public/core/v3/objects?q=location=='{project}'"
print(url)

payload ='{}'
#payload ='{"objects":[{"id":"9brn4KVQLCdhNUCxoTQPec"}]}'
#payload = '{"objects":[{"path": "Data Science/AMP OFFERS","type": "Folder"}]}'
#and updateTime<2018-03-27T12:00.00Z
headers = {
  'content-type': 'application/json',
  "Accept": "application/json",
  "INFA-SESSION-ID":SessionId
}
response = requests.request("GET", url, headers=headers, data=payload)
#job_details= json.loads(response.content)
#print(json.dumps(response.json(),indent= 4))
dumps = json.dumps(response.json())
loads = json.loads(dumps)
listofpathids =[i['id'] for i in loads['objects']]
listofpaths =[i['path'] for i in loads['objects']]
#print(listofpathids)
#print(listofpaths)
  ### get job ids ###
for path in listofpaths:
  try:
    url = f"{serverUrl}/public/core/v3/objects?q=location=='{path}'"
    #print(url)
    headers = {
      'content-type': 'application/json',
      "Accept": "application/json",
      "INFA-SESSION-ID": SessionId
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    dumps = json.dumps(response.json())
    loads = json.loads(dumps)
    listofjobids = [{'id':i['id'],'type':i['type'], 'path':i['path'],'update_date':i['updateTime']} for i in loads['objects']]
    listofdfs.append(pd.DataFrame.from_dict(listofjobids))
    #print(loads)
  except: next
df = pd.concat(listofdfs)

#filter1 = df['path'].str.contains('P1Tables-DailyLoad' ,regex = False)
#filter2 = df['type'] =='TASKFLOW'#!= 'Folder'& df['type'] !=
#df = df[filter1 & filter2]
altfilt = df['type'].isin(['TASKFLOW','DSS','MI_TASK'])
altfilt2 =  df['id'] != '50t0yP91ugschMvTU3hvUZ'
df = df[altfilt & altfilt2]
df['project']= df['path'].apply(lambda x: x[:re.search("\/",x).span()[0]])
df['path']= df['path'].apply(lambda x: x[re.search("\/",x).span()[1]:])
df['jobname']= df['path'].apply(lambda x: x[re.search("\/",x).span()[1]:])
df['path']= df['path'].apply(lambda x: x[:re.search("\/",x).span()[1]])
#apply(lambda x: x[:column_name_length] if len(x) > column_name_length else x)
print(df)
#print(1)
for row in df.itertuples():
  print(row[5],row[1],row[2])

