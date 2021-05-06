import requests,json

url = "https://dm-us.informaticacloud.com/ma/api/v2/user/login"
payload = "{\"@type\":\"login\",\"username\": \"{usr}\",\"password\": \"{pwd}\"}" # replace {usr} with your user id and {pwd} with your users password
headers = {
  'Content-Type': 'application/json',
    'Accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)
#print(response.text.encode('utf8'))
t = json.loads(response.text)
SessionId = t['icSessionId']
serverUrl = t['serverUrl']
uuid = t['uuid']
orgUuid = t['orgUuid']
