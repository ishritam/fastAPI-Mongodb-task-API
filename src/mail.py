# Python code to illustrate Sending mail from 
# your Gmail account 
import smtplib 
import json
import logging

def send_mail(Mail_sender_id, Mail_sender_password, receiver_mail_id, message_to_send):
    try:
        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        print("========creates SMTP session ===========")

        # start TLS for security 
        s.starttls() 

        # Authentication 
        s.login(Mail_sender_id, Mail_sender_password)
        print("========Authentication Done!!===========")

        # sending the mail 
       
        s.sendmail(Mail_sender_id, receiver_mail_id, message_to_send) 
        print("========sending the mail ===========")

        # terminating the session 
        s.quit() 
        print("========Task sent!!! Done!!============")
    except Exception as e:
        print(e)
        print(f"Couldn't send the mail!!! due to {e}")

