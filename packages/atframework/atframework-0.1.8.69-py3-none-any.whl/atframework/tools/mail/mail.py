# -*- coding: utf-8 -*-
# @Time : 2021/8/2 15:28
# @Author : Siro
# @File : mail.py
# @Software: PyCharm

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from atframework.tools.mail.mail_settings import MailSettings


class Mail:

    def __init__(self):
        self.port = MailSettings.PORT
        self.smtp_server_domain_name = MailSettings.SMTP_SERVER_DOMAIN_NAME
        self.sender_mail = MailSettings.SENDER_EMAIL
        self.password = MailSettings.SENDER_PASSWORD
        self.subject = MailSettings.MAIL_SUBJECT
        self.html_template = MailSettings.MAIL_HTML_TEMPLATE

    def send_html(self, emails, mail_content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        for email in emails:
            mail = MIMEMultipart('alternative')
            mail['Subject'] = self.subject
            mail['From'] = self.sender_mail
            mail['To'] = email
            mail_content_new = self.html_template + mail_content
            # html_content = MIMEText(mail_content_new.format(email.split("@")[0]), 'html')
            html_content = MIMEText(mail_content_new, 'html')
            mail.attach(html_content)
            service.sendmail(self.sender_mail, email, mail.as_string())
        service.quit()

    def send_html_with_attachment(self, emails, mail_content, attachment_path):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        # attachment_path like "test.png"
        mimeBase = MIMEBase("application", "octet-stream")
        with open(attachment_path, "rb") as attachment:
            mimeBase.set_payload(attachment.read())
        encoders.encode_base64(mimeBase)
        mimeBase.add_header("Content-Disposition", f"attachment; filename={Path(attachment_path).name}")
        for email in emails:
            mail = MIMEMultipart('alternative')
            mail['Subject'] = self.subject
            mail['From'] = self.sender_mail
            mail['To'] = email
            mail_content_new = self.html_template + mail_content
            # html_content = MIMEText(mail_content_new.format(email.split("@")[0]), 'html')
            html_content = MIMEText(mail_content_new, 'html')
            mail.attach(html_content)
            mail.attach(mimeBase)
            service.sendmail(self.sender_mail, email, mail.as_string())
        service.quit()

    '''
    use pytest --self-contained-html command, then no need to add css file to html report.
    '''

    def add_css_into_html_report(self, report_path, css_path):
        with open(report_path, "r") as html:
            report_str = html.read()
        with open(css_path, "r") as css:
            css_str = css.read()
        report_with_css = report_str + '<style type="text/css">' + css_str + '</style>'
        return report_with_css

    def get_pytest_html_report(self, report_path):
        with open(report_path, "r") as html:
            report_str = html.read()
            return report_str
