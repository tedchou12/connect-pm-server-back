from flask import Flask, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .config import config

class mail :
    def __init__(self) :
        self.obj_config = config()
        self.from_addr = self.obj_config.params['smtp_from']
        self.smtp_user = self.obj_config.params['smtp_user']
        self.smtp_pass = self.obj_config.params['smtp_pass']
        self.smtp_host = self.obj_config.params['smtp_host']
        self.smtp_port = self.obj_config.params['smtp_port']

    def send(self, recipient='', subject='', body='') :
        fromaddr = self.from_addr
        toaddrs  = recipient

        # Add the From: and To: headers at the start!
        msg = MIMEMultipart('alternative')
        msg['From'] = fromaddr
        msg['To'] = toaddrs
        msg['Subject'] = subject

        html_body = MIMEText(body, 'html')
        msg.attach(html_body)
        server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        server.ehlo()
        server.login(self.smtp_user, self.smtp_pass)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.close()
