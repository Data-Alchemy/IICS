import requests, json, pandas as pd, datetime as dt, sys, urllib,asyncio
from concurrent.futures import ThreadPoolExecutor
import unittest, time, re

###########################################################
######################Parms for Job########################
if len(sys.argv) > 1:
    Org         =   sys.argv[1]
    User        =   sys.argv[2]
    Pwd         =   sys.argv[3]
    domain      =   sys.argv[4]
    domain_type =   sys.argv[5]
    page        =   sys.argv[6]
    size        =   sys.argv[7]
    Poll_Int    =   sys.argv[8]
else:
    Org         = ""
    User        = 
    Pwd         = 
    domain      = 
    domain_type = "
    page        = "0"
    size        = "1000"
    Poll_Int    = 60

###########################################################
orgs = {}
###########################################################


############################################################
###################### get meta data #######################
class ELN():

    def __init__(self, Org:str, User:str, Pwd:str):
        self.org                = Org
        self.User               = User
        self.Pwd                = Pwd
        self.domain             = domain
        self.domain_type        = domain_type
        self.page               = page
        self.size               = size
        self.verifcationErrors  = []

    def authorize(self)->str:
        try:
            self.url = ""
            self.payload = {"username": f"{User}", "password": f"{Pwd}"}
            self.header = {'Content-Type': 'application/json'}
            self.response = requests.request("POST", self.url, headers=self.header, data=self.payload)
            self.sessionid = self.response.headers[]
            return self.sessionid
        except Exception as e:
            return 'Authentication Failed: ' + str(e)

    def get_joburls(self)->dict:

        # initial request to get page count and status #
        self.iterator = 0
        self.url_list = []
        self.token_list = []
        try:
            get_joburls_headers = {
                'authorization': f"",
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            self.job_url = f""
            self.job_payload = json.dumps({})
            self.job_header = get_joburls_headers
            self.metadata = requests.request("POST", self.job_url, headers=self.job_header, data=self.job_payload)
            self.totalpages = self.metadata.json()


            while self.iterator < self.totalpages:
                ## scroll required since application is using elastisearch ##
                self.page = self.iterator
                self.joburl = f""
                self.url_list.append(self.joburl)
                self.token_list.append(self.authorize())
                self.iterator += 1
            return dict(zip(self.token_list,self.url_list))

        except Exception as e:
            return 'Metadata fetch failed, nothing returned from server \n exception: ' + str(e) + "\n" + str(self.metadata.content)

##########################################################
################# retrieve actual data ###################
class get_data():

    def __init__(self, urllist:dict,maxpages:int):
        self.urllist    = urllist
        self.maxpages   = maxpages


    def fetch(self)->list:#,session,url):#,session, id):
        tmp =[]
        try:

            for token,url in self.urllist.items():
                get_joburls_headers = {
                    'authorization': f"",
                    'accept': 'application/json',
                    'Content-Type': 'application/json'
                    ,'Connection': 'close'
                }
                self.job_payload = json.dumps({})
                self.job_header = get_joburls_headers
                self.jobdata = requests.request("POST", url, headers=self.job_header, data=self.job_payload)
                data = self.jobdata.json()

                if self.jobdata.status_code != 200:
                    print("Unable to return data from URL::{0}".format(url),'\n',\
                    "Failure On Token::{0}".format(token), '\n'\
                    "Failure Response::{0}".format(self.jobdata.headers)
                    , json.dumps(self.jobdata.json(),indent=4))
                    exit(-1)
                tmp.append(data)
            return tmp

        except Exception as e:
                return  'fetch data failed, no response from server: ' + str(e) + "\n" + str(
                    self.jobdata.content)

######################################################################################

#pwd         = ELN(Org, User, Pwd).authorize()
#urllist     = ELN(Org, User, Pwd).get_joburls()
#data        = get_data(urllist= urllist,maxpages=100100).fetch()

