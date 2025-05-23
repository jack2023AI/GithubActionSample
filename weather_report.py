import os
import requests
import json
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText

from datetime import datetime, timedelta
import time
import akshare as ak

subject = "今日启动"
body = "This is a test email sent from Python!"
sender_email = os.environ.get("MAIL_SEND")  # Replace with your email
sender_password = os.environ.get("MAIL_SEND_PASSWORD")  # Replace with your email password or app-specific password
recipient_email = os.environ.get("MAIL_RECEIVE")  # Replace with recipient's email



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

def get_nowTime():
  # Step 1: Get the current time
  current_time = datetime.now()

  # Step 2: Remove seconds and microseconds
  current_time_no_seconds = current_time.replace(second=0, microsecond=0)

  # Step 3: Add 8 hours
  #new_time = current_time_no_seconds + timedelta(hours=8)
  new_time = current_time_no_seconds + timedelta(hours=0)

  # Print the result
  #print("Current Time (without seconds):", current_time_no_seconds)
  #print("New Time (after adding 8 hours):", new_time)

  return new_time

def check_WorkTime0(new_time):
  # Define the time range for 9 AM to 11 AM
  start_time = new_time.replace(hour=9, minute=20, second=0, microsecond=0)
  end_time = new_time.replace(hour=11, minute=30, second=0, microsecond=0)
  # Check if new_time is within the range
  is_within_range = start_time <= new_time <= end_time

  start_time2 = new_time.replace(hour=13, minute=0, second=0, microsecond=0)
  end_time2 = new_time.replace(hour=19, minute=0, second=0, microsecond=0)
  is_within_range2 = start_time2 <= new_time <= end_time2

  return is_within_range or is_within_range2

def check_WorkTime(new_time):
  # Define the time range for 9 AM to 11 AM
  start_time = new_time.replace(hour=8, minute=0, second=0, microsecond=0)
  end_time = new_time.replace(hour=16, minute=0, second=0, microsecond=0)
  # Check if new_time is within the range
  is_within_range = start_time <= new_time <= end_time

  return is_within_range

def check_FinishWorkTime(new_time):
  finish_time = new_time.replace(hour=15, minute=0, second=0, microsecond=0)
  return   new_time > finish_time

def check_difference(a_Old, h_Old, dif_ok,zhangdie_ok,name, a_code,h_code):
  while True:
    if check_WorkTime(get_nowTime()):
    #if True:
      try:
        #下载数据
        a_stock_data = ak.stock_sz_a_spot_em()
        h_stock_data = ak.stock_hk_main_board_spot_em()
      
        #a_Now = a_stock_data[a_stock_data['代码'] == a_code].values[0][3]
        #h_Now = h_stock_data[h_stock_data['代码'] == h_code].values[0][3]
        a_Now = a_stock_data.loc[a_stock_data['代码'] == a_code, '最新价'].item()
        h_Now = h_stock_data.loc[h_stock_data['代码'] == h_code, '最新价'].item()

        a_ZhangDie = a_stock_data.loc[a_stock_data['代码'] == a_code, '涨跌幅'].item()
        h_ZhangDie = h_stock_data.loc[h_stock_data['代码'] == h_code, '涨跌幅'].item()

        if (abs(a_ZhangDie)>zhangdie_ok) or (abs(h_ZhangDie)>zhangdie_ok):
          subject = "关注涨跌幅_"+name
          time_11=get_nowTime()
          body=time_11.strftime('%Y-%m-%d %H:%M:%S')
          send_email(subject, body, sender_email, sender_password, recipient_email)
          zhangdie_ok=zhangdie_ok*2

        #print(a_Now)
        #print(h_Now)

        #dif=(a_Now.iloc[0]/a_Old-h_Now.iloc[0]/h_Old)*100  #已经换算为百分比
        dif=(a_Now/a_Old-h_Now/h_Old)*100  #已经换算为百分比
        print(get_nowTime(),a_Now,h_Now,dif)        

        if abs(dif)>dif_ok:
          subject = "关注套利_"+name
          time_11=get_nowTime()
          body=time_11.strftime('%Y-%m-%d %H:%M:%S')
      
          send_email(subject, body, sender_email, sender_password, recipient_email)
          a_Old = a_Now
          h_Old = h_Now
          dif_ok = dif_ok*2

        #time.sleep(60)  # 模拟等待秒数
      except Exception as e:
          #print(f"Failed to get socket data: {e}")
          print("Failed to get socket data")
    else:
      #print("no work time")
      #time.sleep(60)  # 模拟等待秒数

      subject = "今日结束"
      #body = "今日结束"
      time_11=get_nowTime()
      body=time_11.strftime('%Y-%m-%d %H:%M:%S')
      send_email(subject, body, sender_email, sender_password, recipient_email)
      break

      '''
      if check_FinishWorkTime(get_nowTime()):
        print("当日交易时间结束")
        subject = "今日结束"
        send_email(subject, body, sender_email, sender_password, recipient_email)
        break
      '''

if __name__ == '__main__':
    with open("price.txt", "r", encoding='utf-8') as f:
        line = f.readline()
        values = line.split(',')
        a_Old = float(values[0].strip())
        h_Old = float(values[1].strip())
        dif_ok = float(values[2].strip())
        zhangdie_ok = float(values[3].strip())

     #发送邮件
    subject = "今日启动"
    time_11=get_nowTime()
    body=time_11.strftime('%Y-%m-%d %H:%M:%S')
    #body=values[0].strip()
    send_email(subject, body, sender_email, sender_password, recipient_email)

    
    #a_Old=3.63
    #h_Old=2.50
    #dif_ok=2.0
    #zhangdie_ok=1.5
    name='中国广核'
    a_code='003816'
    h_code='01816'
    
    check_difference(a_Old, h_Old, dif_ok,zhangdie_ok,name, a_code,h_code)
    
