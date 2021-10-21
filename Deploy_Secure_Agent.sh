#username $1
#pwd $2 
mkdir /app/
wget https://na1.dm-us.informaticacloud.com/saas/download/installer/linux64/agent64_install_ng_ext.bin
cd /app/ 
./agent64_install_ng_ext.bin -i silent -DUSER_INSTALL_DIR=/app/ipaas/isa
cd /app/ipaas/isa/apps/agentcore 
./infaagent startup
./consoleAgentManager.sh configureToken $1 $(curl - $2)
            
