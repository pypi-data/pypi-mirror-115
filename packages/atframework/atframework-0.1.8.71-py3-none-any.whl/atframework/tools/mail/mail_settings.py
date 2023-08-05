# -*- coding: utf-8 -*-
# @Time : 2021/8/2 18:18
# @Author : Siro
# @File : mail_settings.py
# @Software: PyCharm

class MailSettings(object):

    PORT = 465
    SMTP_SERVER_DOMAIN_NAME = "smtp.gmail.com"
    SENDER_EMAIL = "siro7test@gmail.com"
    SENDER_PASSWORD = "Ss7777777"

    MAIL_HTML_TEMPLATE = """
                    <h1>Test Report</h1>

                    <p>Hi {0},</p>
                    <p> <b>Have a good day!</b> The automation testing report is generated, following is details.</p>
                    """
    MAIL_SUBJECT = "Automation Test Report"
    RECEIVER_EMAILS = ['hyde_d@qq.com', 'cicitata@163.com']


