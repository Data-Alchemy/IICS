###########################################################
######################Parms for Job########################

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

org     = ''
user    = ''
pwd     = ''

###########################################################
###########################################################

class IICS_Resource_Manager():
    def __init__(self, org, user, pwd):
        self.org            = org
        self.user           = user
        self.pwd            = pwd



    def auth(self) -> dict:
        try:
            self.url            = f"https://{self.org}.informaticacloud.com/ma/api/v2/user/login"
            self.payload        = json.dumps({"@type": "login", "username": f"{self.user}", "password": f"{self.pwd}"})
            self.headers        = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            self.response       = requests.request("POST", self.url, headers=self.headers, data=self.payload)
            self.json_resp      = self.response.json()
            self.SessionId      = self.json_resp['icSessionId']
            self.serverUrl      = self.json_resp['serverUrl']
            self.uuid           = self.json_resp['uuid']
            self.orgUuid        = self.json_resp['orgUuid']
            self.domain         = re.search("\//(.*?)\.", self.serverUrl).group(1) + "-ing." + self.org
            self.run_domain = re.search("\//(.*?)\.", self.serverUrl).group(1) +"."+ self.org
        except Exception as e:
            print(e)
        return {"token": self.SessionId, "URL": self.serverUrl, "orgid": self.orgUuid,"domain":self.domain,"run_domain":self.run_domain}


    def GetInstallToken(self):
        self.runurl = f"{self.auth()['URL']}/api/v2/agent/installerInfo/linux64"
        self.runpayload = {'application': ''}
        self.runheaders = {
            "accept": "application/json",
            "content-type": "application/json",
            "icSessionId": f"{self.auth()['token']}"
        }
        self.response = requests.request("GET", url=self.runurl, headers=self.runheaders, data=self.runpayload)
        self.json_resp = self.response.json()
        self.InstallToken = self.json_resp['installToken']
        p = pth.Path('./tokens')
        p.mkdir(exist_ok=True)
        self.output_token = open(p / '.install_token.netrc', 'w')
        print(self.InstallToken,file=self.output_token)
        return self.InstallToken



print(IICS_Resource_Manager(org='dm-na',user='',pwd="").GetInstallToken())
