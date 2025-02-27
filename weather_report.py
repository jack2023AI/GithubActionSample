import os
import requests
import json
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, sender_email, sender_password, recipient_email):
    # Create the email content
    msg = MIMEText(body)
    msg['Subject'] = subject+body
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Connect to the Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Log in to your email account
            server.login(sender_email, sender_password)
            # Send the email
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == '__main__':
    # Usage
    subject = "关注价差__"
    body = "This is a test email sent from Python!"
    sender_email = os.environ.get("MAIL_SEND")  # Replace with your email
    sender_password = os.environ.get("MAIL_SEND_PASSWORD")  # Replace with your email password or app-specific password
    recipient_email = os.environ.get("MAIL_RECEIVE")  # Replace with recipient's email
    print(sender_email)
    
    #发送邮件
    #send_email(subject, body, sender_email, sender_password, recipient_email)
    send_email(subject, body, sender_email, sender_password, recipient_email)
