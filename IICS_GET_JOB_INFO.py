import requests,json, pandas as pd, time,datetime,sys
from IICS_AUTH import SessionId
pd.set_option("expand_frame_repr", False)
job_detail_url = "https://na1-ing.dm-us.informaticacloud.com/mijobmonitor/api/v1/MIJobs?$count=true&$orderby=deployTime%20desc&$skip=0&$top=1000"
payload= {}
headers = {
  "task_id":"60lwBL46tpoiZiD1HbYW2n",
  "authority": "na1-ing.dm-us.informaticacloud.com",
  "sec-ch-ua": "'Google Chrome';v='87', ' Not;A Brand';v='99', 'Chromium';v='87'",
  "accept": "application/json, text/plain",
  "sec-ch-ua-mobile": "?0",
  'content-type': 'application/json',
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
  "origin": "https://na1.dm-us.informaticacloud.com",
  "sec-fetch-site": "same-site",
  "sec-fetch-mode": "cors",
  "sec-fetch-dest": "empty",
  "referer": "https://na1.dm-us.informaticacloud.com/cloudUI/products/monitor/main/ingestion-dashboard",
  "accept-language": "en-US,en;q=0.9",
  "xsrf_token": "PBA",
  "cookie": "USER_SESSION=" + SessionId + ";" + "XSRF_TOKEN=PBA"
}
job_detail_response = requests.request("GET", job_detail_url, headers=headers, data=payload)
job_details= json.loads(job_detail_response.content)
df = pd.read_json(json.dumps(job_details['value'])).sort_values(by=['runId'])
job_info = df
print(job_info)
