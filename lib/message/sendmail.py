#coding:utf-8

import os
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from lib.file.properties import Properties
from lib.encrypt import Encrypt

from configuration.globalcfg import GlobalCfg


class SendMail:
    '''
    SendMail to pointed User
    '''

    msg = {}

    def __init__(self, recver, content=None):
        self.sendTo = recver

        self.globalcfg = GlobalCfg()

        self.msg = MIMEMultipart()

        #Init Sender Info
        cfgPro = Properties(self.globalcfg.configFile())
        self.msg['from'] = cfgPro.getProperty('Send_addr')
        self.sendPwd = cfgPro.getProperty('Send_pwd')

        #Get Mail Server info
        self.smtp_host = cfgPro.getProperty('SMTP_host')
        self.smtp_port = cfgPro.getProperty('SMTP_port')

        #Get Key For decrypt
        self.decryptKey = cfgPro.getProperty('EncryptKey')

    def __take_messages(self):
        """生成邮件的内容，和html报告附件"""
        cfgPro = Properties(self.globalcfg.configFile())
        projectName = cfgPro.getProperty('Project')

        reportPath = os.path.join(self.globalcfg.reportDir(),
                                  'TestResult.html')

        self.msg['Subject'] = '{0}自动化测试报告'.format(projectName)
        self.msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')

        with open(reportPath, 'rb') as f:
            mailbody = f.read()
        html = MIMEText(mailbody, _subtype='html', _charset='utf-8')
        self.msg.attach(html)

        # html附件
        att1 = MIMEText(mailbody, 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        att1[
            "Content-Disposition"] = 'attachment; filename="TestResult.html"'  #这里的filename可以任意写，写什么名字，邮件中显示什么名字
        self.msg.attach(att1)

    def send(self):
        """发送邮件"""
        self.__take_messages()
        try:
            smtp = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            passwd = Encrypt(self.decryptKey).decrypt(self.sendPwd)
            smtp.login(self.msg['from'], passwd)
            smtp.sendmail(self.msg['from'], self.sendTo, self.msg.as_string())
            smtp.close()
        except Exception:
            raise


if __name__ == '__main__':
    sendMail = SendMail('dingquan.wu@dae.org, guangli.wang@dae.org')
    sendMail.send()
