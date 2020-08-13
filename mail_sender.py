import smtplib 
import ast
import getpass
import sys

#ENTER DETAILS BELOW

DEFAULT_RECIPIENT = '' 
pwd = ""


def send_mail(mailfile,SUBJECT,recipient = DEFAULT_RECIPIENT):

    if recipient == '.':
        recipient = DEFAULT_RECIPIENT

    s = smtplib.SMTP('smtp.gmail.com', 587) 

    s.starttls() 
 
    s.login(DEFAULT_RECIPIENT, str(pwd)) 
  
        
    
    if mailfile == '.':
        mailfile = "my_mail_auto.txt"
        f = open(mailfile,'w')
        f.write("Test Mail")
        f.close()
    f = open(mailfile,'r')
    TEXT = f.read()
    f.close()
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        
    s.sendmail(DEFAULT_RECIPIENT, recipient, message) 

    s.quit() 
    
    
if __name__ == '__main__':
    if len(sys.argv)<3:
        print("Check number of arguments: py mail_sender.py mailfile(.) subjectstr recepient") #recipient argument is mandatory
        sys.exit(-1)

    send_mail(sys.argv[1]," ".join(sys.argv[2:-1]),sys.argv[-1])










