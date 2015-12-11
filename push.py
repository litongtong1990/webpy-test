#!/usr/bin/env python3  
#coding: utf-8  

import smtplib  
import os
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage  
from email import Encoders


def push_kindle(data,bookname,receiver):
    #receiver = '167459012_22@iduokan.com'  
    #receiver = 'litongtong1990@163.com'
    subject = bookname 
    sender = 'zongbengjiao9791@163.com'
    smtpserver = 'smtp.163.com'  
    username = 'zongbengjiao9791'  
    password = 'xrvaih601'  

    
    try:
        msgRoot = MIMEMultipart('related')  
        msgRoot['Subject'] = subject    
        att = MIMEText(data, 'base64', 'utf-8')  
        att["Content-Type"] = 'application/octet-stream'  
        att.add_header('Content-Disposition', 'attachment', filename=bookname.encode("utf-8"))   
        msgRoot.attach(att)  
                  
        smtp = smtplib.SMTP()  
        smtp.connect(smtpserver)  
        smtp.login(username, password)  
        smtp.sendmail(sender, receiver, msgRoot.as_string())  
        smtp.quit() 
        return 1
    
    except Exception, e:
        print str(e)  
        return 0
