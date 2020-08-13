# bigbasket_slotfinder
Repeatedly checks for slot availability on bigbasket and notifies user when available.

Following steps must be followed:  
1. Register for a bigbasket account.  

2. Go to bigbasketslot.py and mail_sender.py and below the comment 'ENTER DETAILS BELOW', enter the email id and password for your gmail account associated with bigbasket account. **Do not enter the big basket account password.** You may enter a different mail id and password for mail_sender.py if you want notifications on a gmail account different from that of big basket.   

3. For the program to work, you may need to enable less secure apps in gmail. https://myaccount.google.com/lesssecureapps.  

4. Note that bigbasketslot.py imports from mail_sender.py to send a mail when a slot is found. Thus the two programs must be in same directory or in $PATH for program to work. Also note that bigbasketslot.py **automatically reads and enters OTP** when needed. Thus, once the user executes bigbasketslot.py, no user input is needed. The program executes autonomously. Run the following command on the terminal:  
`python3 bigbasketslot.py`   

5. Also note that mail_sender.py can be used independently to send mails automatically.   

6. Program checks for slots every two minutes. There is a 30 second delay after email ID is entered by the program and other delays everywhere. **Do not interfere with program-controlled browser unless an error message is displayed on stdout(console)**.
