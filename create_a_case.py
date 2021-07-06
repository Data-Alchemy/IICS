from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import time

problem_type = {'1':"Administration & Security (SSO/SAML, User/user-Group",
                '2':"Connector/Driver",
                '3':"Data Integration Task (Mapping, Mapping Config Task, bundles, Powercenter)",
                '4':"Design Configuration Service (Business Service, Hierarchy, Schedules)",
                '5':"DiscoveryIQ",
                '6':"Proxy",
                '7':"Runtime environment (Agent)",
                '8':"Hosted - Outage/Availability",
                '9':"Hosted - General",
                '10':"Hosted - Database Request",
                '11':"Hosted - Structured Activity",
                '12': "Hosted - Provision/Re-provision",
                '13': "Hosted - Abnormal Usagel",
                '14': "Hosted - Certificate Activity",
                '15': "Hosted - EBF/Patch update",
                '16': "Hosted - Connection/Access Issues"
}
user = "" # to login to portal
password = "" #to login to portal
problem_type_selected = problem_type['7']
secure_agent= ""
server= ""
org_id = ""
jobname = "Database Mass Ingestion"
priority = "P1"
alt_contact = ""
error_summary = "DataBase Ingestion is in error status in secure agent"
previous_case = "None"
local_log_path_1 = ""
if len(previous_case)<1:previous_case_logic = "Previous cases: No previous cases for this case"
else :previous_case_logic = f"Previous cases: {previous_case}"

actions_taken = '''
Component has been restarted several times but continues to error out. 
'''
subject = f"{jobname} is failing due to error in Runtime"
error_message = "DBMI is not working " #TE_7002 Transformation stopped due to a fatal error in the mapping. The expression [﻿SOURCE] contains the following errors [<<PM Parse Error>> invalid token ... ﻿<<<<SOURCE].
description = f'''
Job Name:{jobname} 
\nFailed On {datetime.datetime.now()} 
\nSecure Agent: {secure_agent}
\n{previous_case_logic}
\nActions Taken: {actions_taken}
\ncomplete error message is : {error_message}
'''



class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(5)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_untitled_test_case(self):
        driver = self.driver
        driver.get("https://network.informatica.com/login!input.jspa?referer=https://infapassport.okta.com/app/salesforce/exk15f0x4gft6WrYr1d8/sso/saml")
        driver.maximize_window()
        driver.find_element_by_id("username01").clear()
        driver.find_element_by_id("username01").send_keys(user)
        driver.find_element_by_id("password01").clear()
        driver.find_element_by_id("password01").send_keys(password)
        driver.find_element_by_id("login-submit").click()
        driver.find_element_by_link_text("Create a New Case").click()
        driver.find_element_by_link_text("Technical").click()
        driver.find_element_by_id("customDropDownSpanProductLine").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='customDropDownSpanProductLinecustomdropdown-list']/div[6]").click()
        time.sleep(2)
        driver.find_element_by_id("customDropDownSpanProductLine").click()
        driver.find_element_by_xpath("//div[@id='customDropDownSpanProductLinecustomdropdown-list']/div[6]").click()
        driver.find_element_by_xpath("//div[@id='CoveoPicklistAPINameProductVersion']/div[4]/div/span").click()
        driver.find_element_by_xpath("//div[@id='CoveoPicklistAPINameProductVersion']/div[4]/div/ul/li").click()
        time.sleep(2)
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[10]/div/div/div[2]/div").click()
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[10]/div/div/div[2]/div/ul/li").click()
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[11]/div/div/div[2]/textarea").click()
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[11]/div/div/div[2]/textarea").clear()
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[11]/div/div/div[2]/textarea").send_keys(subject)
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[12]/div/div/div[2]/textarea").click()
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[12]/div/div/div[2]/textarea").clear()
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[12]/div/div/div[2]/textarea").send_keys(error_summary)
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[13]/div/div/div[2]/textarea").click()
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[13]/div/div/div[2]/textarea").clear()
        driver.find_element_by_xpath("//div[@id='coveo-case-creation-main-section']/div/div/div/div[13]/div/div/div[2]/textarea").send_keys(description)
        driver.find_element_by_link_text("Next").click()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails:j_id141:orgId").click()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails:j_id141:orgId").clear()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails:j_id141:orgId").send_keys(org_id)
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails:secureAgent").click()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails:secureAgent").clear()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails:secureAgent").send_keys(secure_agent)
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:AltEmailTable:j_id169:0:j_id170").click()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:AltEmailTable:j_id169:0:j_id170").clear()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:AltEmailTable:j_id169:0:j_id170").send_keys(alt_contact)
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:additionalDetails:j_id181:problemType").click()
        Select(driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:additionalDetails:j_id181:problemType")).select_by_visible_text(problem_type_selected)
        driver.find_element_by_id( "j_id0:s2:j_id134:attachmentStepForm:j_id136:additionalDetails:j_id181:problemType").click()
        driver.find_element_by_xpath("//div[@id='j_id0:s2:j_id134:attachmentStepForm:j_id136:additionalDetails:j_id181']/div/table/tbody/tr[2]/td").click()
        driver.find_element_by_name("j_id0:s2:j_id134:attachmentStepForm:j_id136:AltEmailTable:j_id180").click()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:defaultAttachmentsWrapper:j_id189:2:j_id190:j_id191:j_id192").send_keys(local_log_path_1)
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:defaultAttachmentsWrapper:j_id189:4:j_id190:j_id191:j_id192").send_keys("C:/Users/545001/Downloads/agent_core_logs.log")
        driver.find_element_by_xpath("//div[@id='j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails']/div[2]/table/tbody/tr[2]").click()
        driver.find_element_by_xpath("//div[@id='j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails']/div[2]/table/tbody/tr[2]/td").click()
        driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:OrgDetails:secureAgent").send_keys(server)
        self.accept_next_alert = False
        driver.find_element_by_link_text("Next").click()
        self.assertEqual("You have not attached a file for the problem type selected, press OK to proceed without attaching or Cancel to return to the page",
        self.close_alert_and_get_its_text())
        #driver.find_element_by_id("j_id0:s2:j_id134:attachmentStepForm:j_id136:defaultAttachmentsWrapper:j_id189:2:j_id190:j_id191:j_id192").send_keys("C:\\fakepath\\tomcat_logs.zip")
        driver.find_element_by_name("j_id0:s2:j_id134:attachmentStepForm:j_id136:j_id198").click() # upload attachments
        driver.find_element_by_link_text("Next").click()
        driver.find_element_by_link_text("Finish").click()
        print("Case submitted sucessfully")

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
