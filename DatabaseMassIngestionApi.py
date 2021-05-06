##########################################################################################################
# This script was created through intensive investigation of the network traffic while using IICS Portal #
# At the time this was created there was no official documentation or supported process for running dbmi #
#              through rest api calls so initial load jobs needed to be run manually.                    #
#     Make sure to have setup a automation user in your org prior to executing with admin permissions    #
#               IICS_GET_JOB_INFO.py & IICS_Auth_Token.py both must be available in your prj             #
#########################################################################################################


import requests,json, pandas as pd, time,datetime,sys
from IICS_AUTH import SessionId
from IICS_GET_JOB_INFO import job_info,job_detail_response

if len(sys.argv)>1:
  Job_ID = sys.argv[1]
  Poll_Int = int(sys.argv[2])
else :
  Job_ID = '1' # can be obtained from the portal by going to the monitor and opening the job after running manually
  Poll_Int = 30

########################################################################
################## Get Job Details Before Run ##########################
########################################################################

var1 = job_info['assetId'].str.contains(str(Job_ID))
var2 = job_info['duration'] != 0
var3 = job_info['duration'] <= 86400000
var4 = job_info['duration'] <= 86400000
current_job_list = job_info[var1 & var2 & var3 & var4]
rows = 0
rows = current_job_list['assetId'].agg('count')

###################### Make sure job exists ############################
if current_job_list.shape[0] == 0:
  print('Run Message: Job does not exist please enter a valid job id for a job that exists in informatica.')
  exit(-1)
  quit()
########################################################################

current_job = current_job_list.iloc[[-1]]

if current_job['assetType'].item() == 'DBMI_TASK':
  run_url = "https://na1-ing.dm-us.informaticacloud.com/dbmi/api/v1/job/start"
  run_payload = "{\"orgId\":\"{}\",\"dbmiJobId\":"+str(Job_ID)+",\"resume\":false}" # replace {} with your org id 
  run_headers = {
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
  "xsrf_token": "Mirko",
  "cookie": "USER_SESSION="+SessionId+ ";"+"XSRF_TOKEN=PBA" #XSRF_TOKEN value is now required but any value can be passed
}
elif current_job['assetType'].item() == 'MI_TASK':
  run_url = "https://na1.dm-us.informaticacloud.com/mftsaas/api/v1/job"
  run_payload="{\"taskId\":\""+str(Job_ID)+"\"\r\n}"
  run_headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'IDS-SESSION-ID': SessionId,
  'Origin': 'https://na1-ing.dm-us.informaticacloud.com',
  'Referer': 'https://na1-ing.dm-us.informaticacloud.com/',
  'Accept-Language': 'en-US,en;q=0.9',
  }
########################################################################

##################Make sure job is deployed #########################
if current_job['status'].item() == 'undeployed':
  print("Job ID: "+str(Job_ID))
  print("Job Name: "+ str(current_job['assetName'].item()))
  print('Run Message: job is not deployed yet and can not be run')
  print('Response Status: ' + str(job_detail_response.status_code))
  exit(-1)
  quit()

##################Make sure job is not running #########################
if current_job['status'].item() == 'running':
  print("Job ID: "+str(Job_ID))
  print("Job Name: "+ str(current_job['assetName'].item()))
  print('Run Message: job is already running, wait for job to complete or go to the portal and cancel run')
  print("This job has been running for: " + str(round(current_job['duration'].item()/60000))+" min")
  print('Response Status: ' + str(job_detail_response.status_code))
  exit(-1)
  quit()
########################################################################

#######################################################################################
#####if job has multiple runs collect stats to make sure run exec in expected time#####
#######################################################################################
elif rows >=2 and (current_job.shape[0] != 0):
  run_response = requests.request("POST",run_url,headers=run_headers, data= run_payload)
  average_run_duration = round(current_job_list['duration'].agg('mean')/60000)
  standard_dev = abs(round(current_job_list['duration'].agg('std')/60000))
  onestd = abs(average_run_duration-standard_dev)
  onestdhigh= round((average_run_duration+standard_dev))
  onestdlow= round((average_run_duration-standard_dev))
  response_ini = 'Starting'
  wait=0
  print("Run Message: Starting Existing Job")
  print("start time: "+ str(datetime.datetime.now()))
  print("Average run time of this job is:" + str(average_run_duration))
  from IICS_GET_JOB_INFO import job_info, job_detail_response

  exit(0) #remove later to get status upddates
  quit()


  while (response_ini == 'Starting' or current_job['status'] == 'running'):
    #exec(open('IICS_GET_JOB_INFO.py').read())
    from IICS_GET_JOB_INFO import job_info, job_detail_response
    print('#####################')
    print("Job ID: " + str(Job_ID))
    print("Job Name: " + str(current_job['assetName'].item()))
    response_ini = 'In Progress'
    var1 = job_info['assetId'].str.contains(str(Job_ID))
    current_job = job_info[var1].iloc[[-1]]
    print("Execution Time: " +str(wait))
    print('Response Status: '+str(current_job['status'].item()))
    print('Run Response Code: '+str(run_response.status_code))

    if wait < onestdlow:
        print(
          'Alert: This job has run outside of the lower control limit please validate (The run is less than expected)')
    elif wait > onestdhigh:
        print(
          'Alert: This job has run outside of the upper control limit please validate (The run is longer than expected)')
    if current_job['status'].item() == 'completed':
      exit(0)
      quit()
    if wait > 86400000:
      print('Job has exceeded max runtime')
      print("Ending New Job")
      print("End time: " + str(datetime.datetime.now()))
      exit(-1)
    time.sleep(Poll_Int)
    wait += Poll_Int


#########################################################################################
######### if this is a new job or has no history run without expected time range#########
#########################################################################################

else:
  run_response = requests.request("POST",run_url,headers=run_headers, data= run_payload)
  response_ini = 'New Job'
  wait = 0
  print("Starting New Job")
  print("start time: "+ str(datetime.datetime.now()))
  print(run_response.status_code)
  print(run_response.text)
  from IICS_GET_JOB_INFO import job_info, job_detail_response


  exit(0) #remove later to get status upddates
  quit()


  while response_ini == 'New Job' or current_job['status'].item == 'running':
    from IICS_GET_JOB_INFO import job_info, job_detail_response
    response_ini = 'In Progress'
    var1 = job_info['assetId'].str.contains(str(Job_ID))
    current_job = job_info[var1]
    print('#####################')
    print("Job ID: " + str(Job_ID))
    print("Job Name: " + str(current_job['assetName'].item()))
    print('Polling for status, time run: '+str(wait))
    print("Job Status: "+ current_job['status'].item())
    if wait >86400000:
      print('Job has exceeded max runtime')
      print("Ending New Job")
      print("End time: " + str(datetime.datetime.now()))
      exit(-1)
      quit()
    if current_job['status'].item() == 'failed':
      print('#####################')
      print("Ending New Job")
      print("End time: " + str(datetime.datetime.now()))
      exit(-1)
      quit()
    #print('Response Status: '+str(response.status_code))
    time.sleep(Poll_Int)
    wait += Poll_Int
print('#####################')
print("Ending Job")
print("End time: " + str(datetime.datetime.now()))
