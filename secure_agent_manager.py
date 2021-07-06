import paramiko,time,sys,json,os,pandas
from pathlib import Path
home = str(Path.home())

########################################################################################################################
hosts={

}
################################################### parms  #############################################################
proxy = None
Port = 22
Username = ''
#'545001'
Pwd = open('').read()
Host = ''
remote_host = '' #use this to deploy auth key from one server to another using deploy key exe
keys= '' # location of keyfile
sudo_user = 'sudo su - ### enter sudo name ###' #optional parameter fill in if using sudo option in function must be passed as full command ie: sudo su - user
path = ''
download_from = ""
download_to = "C:/Users/545001/Downloads"
job_name = '' # for mass ingestion log collection
job_type = 'dbmi' # set what job type you want to run
file = ""
home = str(Path.home())
########################################################################################################################
###########################################  pre cached cmds  ##########################################################

job_exe = {'dbmi_job'           :   f'cd /tmp/iics_logs/ \n /app/ipaas/isa/jdk/jre/bin/java -jar $(find /app/ipaas/isa/downloads/package-DBMI.*/package/dbmi-diagnostic-tool/dbmi.diagnostic.tool.jar) -h /app/ipaas/isa/ -j {job_name}',
           'dbmi_agent'     :   'cp -r /app/ipaas/isa/apps/Database_Ingestion/logs/services/dbmi_agent /tmp/iics_logs/',
           'agent_shutdown' :   'cd /app/ipaas/isa/apps/agentcore/ \n ./infaagent shutdown',
           'agent_startup'  :   'cd /app/ipaas/isa/apps/agentcore/ \n ./infaagent startup',
           'tomcat_log'     :   'cp `find /app/ipaas/isa/apps/Data_Integration_Server/logs/tomcat/| tail -1` /tmp/iics_logs/',
           'import_log'     :   'cp `find /app/ipaas/isa/apps/Data_Integration_Server/logs/*import.log| tail -1` /tmp/iics_logs/',
           'agent_core_log' :   'cp `find /app/ipaas/isa/apps/agentcore/agentcore.log| tail -1` /tmp/iics_logs/',
           'infaagent_log'  :   'cp `find /app/ipaas/isa/apps/agentcore/infaagent.log| tail -1` /tmp/iics_logs/',
           'zip_logs'       :   'zip -rm /tmp/iics_logs/iics_logs.zip /tmp/iics_logs/',
           'check_zip_logs' :   'zip -sf /tmp/iics_logs/iics_logs.zip',
           'remove_logs'    :   'rm -f /tmp/iics_logs/iics_logs.zip',
           'download_agent' :   'wget https://na1.dm-us.informaticacloud.com/saas/download/installer/linux64/agent64_install_ng_ext.bin',
           'deploy_install' :   'cd /app/ \n ./agent64_install_ng_ext.bin -i silent -DUSER_INSTALL_DIR=/app/ipaas/isa',
           'config_install' :   'cd /app/ipaas/isa/apps/agentcore \n ./infaagent startup \n',
           'config_intall_2':   'cd /app/ipaas/isa/apps/agentcore \n ./consoleAgentManager.sh configureToken sebastian_hansen@saveonfoods.com.SAML2 lbXoVLWlHBqcvVScwrWim5x3leNKxhYubvkWnGIQKy3tOMPsbeAorykoKVVljCHrfAKs97LFAEjk0wUMA1Fr4H',
           'generate_keys'  :   "ssh-keygen -q -t rsa -b 4096 -N '' <<<$'\ny\n'",
           'check_keys'     :   'ls -lha ~/.ssh/',
           'deploy_keys'    :   f"scp ~/.ssh/authorized_keys {Username}@{remote_host}:~/.ssh/authorized_keys <<<$'{Pwd}\n'",
           'tmp_log_check'  :   '[ ! -d /tmp/iics_logs/] || mkdir /tmp/iics_logs/'
            }

########################################################################################################################
#############################################  custom functions  #######################################################

def exec_remote_cmds(commands,waittime,sudo = None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=Host, username=Username, password=Pwd, port=Port,
                   key_filename=keys)  # instantiate connection

    shell = client.invoke_shell()

    if sudo != None:
        shell.send(sudo)
        time.sleep(waittime)
        receive_buffer = shell.recv(1024)

    receive_buffer = ""
    shell.send(commands)
    status = shell.recv_ready()
    cmple = []
    return_cursor_item = None
    page = 0
    time.sleep(waittime)
    while return_cursor_item != '$':
        # status ==False :
        time.sleep(waittime)
        output = shell.recv(32768000).decode("utf-8")
        for i in output.split(';', ):
            cmple.append(''.join(s for s in i))
        # print(cmple)
        # print("Page :", page)
        return_val = [s for s in output.splitlines()][-2].strip()
        return_cursor = [s for s in output.splitlines()][
            -1].strip()  ## needed for custom exit subroutine since paramiko hangs the session
        return_cursor_item = [l for l in return_cursor][
            len([l for l in return_cursor]) - 1]  ## needed for custom exit subroutine since paramiko hangs the session
        return (
        (json.loads(json.dumps({'value': return_val, 'output': output, 'cursor': return_cursor_item}, indent=4))))
        status += shell.recv_ready()
        page += 1
    #print("Pages Read:",page)
    #for i in cmple: print(i.replace('[01','').replace('\n',''))


def download_remote_file(remotepath:str,localpath:str,waittime:int,sudo:str = None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=Host, username=Username, password=Pwd, port=Port, key_filename=keys) #instantiate connection

    shell = client.invoke_shell()

    if sudo != None :
        shell.send(sudo)
        time.sleep(waittime)
        receive_buffer = shell.recv(1024)

    sftp = client.open_sftp()
    sftp.get(remotepath,localpath)
    while not os.path.exists(localpath):
        time.sleep(waittime)
    sftp.close()

def write_file_to_remote(remotepath:str,localpath:str,waittime:int,sudo:str = None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=Host, username=Username, password=Pwd, port=Port, key_filename=keys) #instantiate connection

    shell = client.invoke_shell()

    if sudo != None :
        shell.send(sudo)
        time.sleep(waittime)
        receive_buffer = shell.recv(1024)

    sftp = client.open_sftp()
    sftp.put(localpath,remotepath)
    while not os.path.exists(remotepath):
        time.sleep(waittime)
    sftp.close()

def terminal_bot(mode:str,job:str = None,job_type:str = None,err:str = None,out:str = None, sudo:str =None):
    if mode == "Log Collector":
        if job_type == 'dbmi' or job_type == 'dbmi_agent':
            listofcommands = f'''
            {job_exe['remove_logs']}
            {job_exe[job_type]}
            '''
            print(exec_remote_cmds(listofcommands, 1,sudo=sudo_user)[out])
            time.sleep(5)
            zipf = f'''
            {job_exe['zip_logs']}
            '''
            print(exec_remote_cmds(zipf, 1,sudo=sudo_user)[out])
            time.sleep(2)
            print(download_remote_file('/tmp/iics_logs/iics_logs.zip', f'{home}/downloads/iics_logs.zip', 1))
        if job_type == 'dis':
            log_download_path = f"{os.path.expanduser('~')}\Downloads"
            #### collect logs and prepare ####
            collect = f'''
            {job_exe['agent_core_log']}
            {job_exe['infaagent_log']}
            {job_exe['import_log']}
            {job_exe['tomcat_log']}
            '''
            print(exec_remote_cmds(collect, 1, sudo=sudo)[out])
            zipf = f'''
            {job_exe['zip_logs']}
            '''
            print(exec_remote_cmds(zipf, 1)[out])
            time.sleep(2)
            print(download_remote_file('/tmp/iics_logs/iics_logs.zip', f'{home}/downloads/iics_logs.zip', 1))


    if mode == "RSA":
        generate_key = f'''
                        {job_exe['generate_keys']}
                        {job_exe['check_keys']}
                        '''
        getusr = f'''
                   whoami
                  '''
        print(exec_remote_cmds(generate_key, 3)[out])
        #print(exec_remote_cmds(getusr, 0, sudo = sudo )[out])
        #remote_path= f'{find_kydir}/.ssh/id_rsa'
        #print(remote_path)
        #download_key = download_remote_file(remote_path, f'{home}/downloads/id_rsa.txt', 1)
########################################################################################################################
## put commands one line at a time ##
listofcommands=f'''
{job_exe['agent_startup']}
'''

terminal_bot(mode="Log Collector",job_type='dbmi_agent',out='output',sudo=sudo_user)
#print(exec_remote_cmds(listofcommands,1,sudo= sudo_user)['output'])
