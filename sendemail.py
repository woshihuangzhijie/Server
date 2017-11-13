import smtplib
import email.mime.multipart
import email.mime.text

# msgTo = '31842165@qq.com' #发送到该邮箱
class sendemail:
    def __init__(self):
        self.msgFrom = 'wangluoproject@163.com' #从该邮箱发送
        self.smtpSever='smtp.163.com' # 163邮箱的smtp Sever地址
        self.smtpPort = '25' #开放的端口
        self.sqm='wangluo3'  # 在登录smtp时需要login中的密码应当使用授权码而非账户密码

    def sendto(self, msgTo, text):
        msg = email.mime.multipart.MIMEMultipart()
        msg['from'] = self.msgFrom
        msg['to'] = msgTo
        msg['subject'] = '计划提醒'
        content = '你好：' + text
        txt = email.mime.text.MIMEText(content)
        msg.attach(txt)
        smtp = smtplib.SMTP()
        # smtplib的connect（连接到邮件服务器）、login（登陆验证）、sendmail（发送邮件）
        smtp.connect(self.smtpSever, self.smtpPort)
        smtp.login(self.msgFrom, self.sqm)
        smtp.sendmail(self.msgFrom, msgTo, str(msg))
        # s = smtplib.SMTP("localhost")
        # s.send_message(msg)
        smtp.quit()


def main():
    msgTo = '3150104130@zju.edu.cn'
    text = '熊毓华同学，你的qq密码泄漏了'
    mail = sendemail()
    mail.sendto(msgTo, text)
if __name__ == '__main__':
    main()





