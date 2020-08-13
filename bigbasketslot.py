from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import sys
import time
import os
import datetime
import smtplib 
import ast
import imaplib
import base64
import email
import re
from mail_sender import send_mail

#ENTER DETAILS BELOW
EMAIL_ID = ""
pwd = ""

def otp_searcher():
    
    mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
    mail.login(EMAIL_ID,pwd)
    mail.select('Inbox')

    dt = (datetime.date.today()- datetime.timedelta(1)).strftime("%d-%b-%Y")

    this_type, data = mail.search(None, '(SENTSINCE {})'.format(dt))

    mail_ids = data[0]
    id_list = mail_ids.split()
    content_list = []
    for num in id_list:
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        try:
            raw_email_string = raw_email.decode("utf-8",errors='ignore')
        except Exception as e:
            print(e)
            
        email_message = email.message_from_string(raw_email_string)

        if email.utils.parseaddr(email_message['From'])[1] != "alerts@bigbasket.com" or "OTP" not in email_message['Subject']:
            continue


        maintype = email_message.get_content_maintype()
        content = ""
        if maintype == 'multipart':
            for part in email_message.get_payload():
                if part.get_content_maintype() == 'text':
                    content+=(part.get_payload())
        elif maintype == 'text':
            content+=(email_message.get_payload())
        content_list.append(content)
        
    #print(content_list)
    otp = []    
    f = open("mails.txt",'w')
    for content in content_list:
        f.write(content+'\n\n\n\n\n\n\n\n\n\n')
        otp_re = re.compile(r'Use the OTP (\d{6}) to login')
        mo = otp_re.search(content)
        otp.append(mo.group(1))
    f.close()
    return otp                              #here otp is list of strings
    

def get_bb_slot(url):
  
    
    driver = webdriver.Chrome()
    driver.get(url)
    loginButton = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div[1]/ul/li[1]/a")
    loginButton.click()
    inputElement = driver.find_element_by_id("otpEmail")
    inputElement.send_keys(EMAIL_ID)
    inputElement.send_keys(Keys.RETURN)
    
    
    print("Waiting for email...")
    for i in range(30,0,-1):
        print(i)
        time.sleep(1)
    
    
    otp = otp_searcher()

    print(otp)
  
    otp_text_field = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div[1]/div/div[1]/login/div/div[2]/form/div[2]/div[1]/input")
    otp_text_field.send_keys(otp[-1])
    otp_text_field.send_keys(Keys.RETURN)
   
    
    time.sleep(7)
    
    driver.get(url)
    
    time.sleep(10)
    
    address_dropdown = driver.find_element_by_xpath("/html/body/div[1]/div[18]/section[1]/div[2]/div[2]/div/button")
    address_dropdown.click()
    
    time.sleep(3)
    
    my_address = driver.find_element_by_xpath("/html/body/div[1]/div[18]/section[1]/div[2]/div[2]/div/div/div[2]/ul/li/a")
    my_address.click()
    
    time.sleep(5)

    while 1:
        driver.get(url)     
        time.sleep(2)
        print("Trying to find a slot!")
        try:
            driver.find_element_by_xpath("//button[@id = 'checkout']").click()

            time.sleep(5)  #driver take a few sec to update the new url
            src = driver.page_source
            if "checkout" in driver.current_url and not "Unfortunately, we do not have" in src:
                print("Found the slots!")
                mailfile = "slotfound.txt"
                f = open(mailfile,'w')
                f.write("A slot on bigbasket has been found at "+str(datetime.datetime.now().strftime("%H:%M")))
                f.close()
                send_mail(mailfile,"SLOT FOUND",'.')
                for i in range(10000):
                    os.system("beep -f 555 -l 46000")
                sys.exit(0)
                '''for i in range(60):
                     notify("Slots Available!", "Please go and choose the slots!")
                     time.sleep(20)'''
        except Exception as e:
            print("If this message pops up multiple times, please find the error and create a PR!")
            print(e)
            pass
        print("No Slots found. Will retry again."+str(datetime.datetime.now().strftime("%H:%M")))
        time.sleep(120)
        




def main():
    
    get_bb_slot('https://www.bigbasket.com/basket/?ver=1')

if __name__ == '__main__':
    main()
