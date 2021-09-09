import requests,json, pandas as pd,datetime,sys
#from IICS_AUTH import SessionId
import unittest, time, re

###########################################################
######################Parms for Job########################
if len(sys.argv)>1:
  Org = sys.argv[1]
  User = sys.argv[2]
  Poll_Int = sys.argv[3]
else :
  Org = "dm-us"                     #"dmr-us"
  Orgid = "60lwBL46tpoiZiD1HbYW2n"
  User = "dis"                      #"DISPRE"
  Job_ID = "105"
  Poll_Int = 60

###########################################################

#Org = "dm-us",Orgid = "60lwBL46tpoiZiD1HbYW2n",User = "dis",Job_ID = 105

###########################################################

class IICS_Run_Job():

    def __init__(self,Org,Orgid,User,Job_ID):
        self.org                = Org
        self.orgid              = Orgid
        self.User               = User
        self.Job                = Job_ID
        self.verifcationErrors  = []


    def authorize(self):

        try:
            self.url                = f"https://{self.org}.informaticacloud.com/ma/api/v2/user/login"
            self.payload            = '{"@type": "login","username": "'+self.User+'","password": ""}'
            self.header             =  {'Content-Type': 'application/json','Accept': 'application/json'}
            self.response           = requests.request("POST", self.url, headers=self.header, data=self.payload)
            self.sessionid          = json.loads(self.response.text)['icSessionId']
            self.serverUrl          = json.loads(self.response.text)['serverUrl']
            #sessionid = self.sessionid
            return self.sessionid
        except Exception as e:
            return 'Authentication Failed: '+str(e)
            #print(self.response.content)
            #exit(-1)

    def runingestionjob(self):
        try:
            headers = {
                'authority': f"{self.orgid}",
                'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                'accept': 'application/json, text/plain, */*',
                'xsrf_token': '6Om3nSBesstd4sU0RQP6uR',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                'content-type': 'application/json',
                'origin': 'https://na1.dm-us.informaticacloud.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://na1.dm-us.informaticacloud.com/cloudUI/products/monitor/main/ingestion-dashboard',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': '_ga=GA1.2.382000473.1603052731; USER_SESSION=' + self.authorize() + '; XSRF_TOKEN=6Om3nSBesstd4sU0RQP6uR'
            }
            self.joburl             = f"https://na1-ing.{self.org}.informaticacloud.com/dbmi/api/v1/job/start"
            self.jobpayload         = '{"orgId":"'+self.orgid+'","dbmiJobId":"'+str(self.Job)+'","resume":"false"}'
            self.jobheader          = headers
            self.jobresponse        = requests.request("POST", self.joburl, headers=self.jobheader, data=self.jobpayload)
            return {'status_code':self.jobresponse.status_code,'content':self.jobresponse.content} # output of response

        except Exception as e:
            return 'Job run failed: ' + str(e) +"\n" +str(self.jobresponse.content)

    def ingestionjobstatus(self):
        status_header ={
                      'authority': 'na1-ing.dm-us.informaticacloud.com',
                      'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
                      'accept': 'application/json, text/plain, */*',
                      'xsrf_token': '6Om3nSBesstd4sU0RQP6uR',
                      'sec-ch-ua-mobile': '?0',
                      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
                      'content-type': 'application/json',
                      'origin': 'https://na1.dm-us.informaticacloud.com',
                      'sec-fetch-site': 'same-site',
                      'sec-fetch-mode': 'cors',
                      'sec-fetch-dest': 'empty',
                      'referer': 'https://na1.dm-us.informaticacloud.com/cloudUI/products/monitor/main/ingestion-dashboard',
                      'accept-language': 'en-US,en;q=0.9',
                      'cookie': '_ga=GA1.2.382000473.1603052731; USER_SESSION='+self.authorize()+'; XSRF_TOKEN=6Om3nSBesstd4sU0RQP6uR'
                    }
        try:
            if self.runingestionjob()['status_code'] != 200:
                print('job was started but failed to initialize \n review that job is deployed and valid')
                exit(-1)
            else:
                self.ingstatusurl       = f"https://na1-ing.{self.org}.informaticacloud.com/mijobmonitor/api/v1/MIJobs?$count=true&$orderby=deployTime%20desc&$skip=0&$top=1000"
                self.ingstatuspayload   = {}
                self.ingstatusheader    = status_header
                self.ingstatusresponse  = requests.request("GET", self.ingstatusurl, headers=self.ingstatusheader, data=self.ingstatuspayload)
                self.df                 = pd.read_json(json.dumps(json.loads(self.ingstatusresponse.content)['value'])).sort_values(by=['runId'])
                self.filter1            = self.df['runId'] == self.Job_ID
                self.myjob              = self.df[self.filter1]
                self.iniresp            = 'New Job'
                self.wait               = 0
                self.pollint            = 120


                while self.iniresp == 'New Job' or self.myjob[0] == 'running':
                    print('#####################')
                    print('processing time :', datetime.datetime.now())
                    response =requests.request("GET", self.joburl, headers=self.jobheader, data=self.jobpayload)
                    job_details = json.loads(response.content)
                    df = pd.read_json(json.dumps(job_details['value'])).sort_values(by=['runId'])
                    var1 = df['runId'] == Job_ID
                    self.myjob = df[var1]
                    print('#####################')
                    print("Job Name: " + str(self.myjob['assetName'].values))
                    print("Job Status: " + self.myjob['status'][0])
                    if self.wait > 86400000:
                        print('Job has exceeded max runtime')
                        print("Ending New Job")
                        print("End time: " + str(datetime.datetime.now()))
                        exit(-1)
                        quit()
                    if self.myjob['status'][0] == 'failed':
                        print('#####################')
                        print("Ending New Job")
                        print("End time: " + str(datetime.datetime.now()))
                        exit(-1)
                        quit()
                    # print('Response Status: '+str(response.status_code))
                    time.sleep(self.pollint)
                    self.wait += self.pollint
                print('#####################')
                print("Ending Job")
                print("End time: " + str(datetime.datetime.now()))
        except:
            print("Could not get status: ", datetime.datetime.now())
            print(self.ingstatusresponse.content)
            exit(-1)

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

#session_id = IICS_Run_Job(Org,Orgid,User,Job_ID).authorize()

if __name__ == "__main__":
    print(IICS_Run_Job(Org, Orgid, User, Job_ID).ingestionjobstatus())
    #print(IICS_Run_Job(Org, Orgid, User, Job_ID).runingestionjob())
    #IICS_Run_Job(Org, Orgid, User, Job_ID).ingestionjobstatus()

'''    def runintegrationjob(self):
        self.joburl     = f"https://na1-ing.{self.Org}.informaticacloud.com/mijobmonitor/api/v1/MIJobs?$count=true&$orderby=deployTime%20desc&$skip=0&$top=1000"
        self.jobpayload = '{"orgId":"'+self.orgid+'","dbmiJobId":"'+str(self.Job)+'","resume":false}'
        self.jobheader  = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        self.jopreponse = requests.request("GET", self.joburl, headers=self.jobheaderheaders, data=self.jobpayloadpayload)'''
