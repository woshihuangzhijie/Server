# -*- coding: UTF-8 -*-
import smtplib
import email.mime.multipart
import email.mime.text

# msgTo = '31842165@qq.com' 
class sendemail:
    def __init__(self):
        self.msgFrom = 'your email'
        self.smtpSever='smtp.163.com' 
        self.smtpPort = '25' 
        self.sqm='your password'  
    def sendto(self, msgTo, text):
        msg = email.mime.multipart.MIMEMultipart()
        msg['from'] = self.msgFrom
        msg['to'] = msgTo
        msg['subject'] = u'计划提醒'
        content =  text
        txt = email.mime.text.MIMEText(content)
        msg.attach(txt)
        #smtp = smtplib.SMTP()
        try:
            print(content)
            server = smtplib.SMTP_SSL(self.smtpSever, 465)
            #smtp.connect(self.smtpSever, self.smtpPort)
            server.login(self.msgFrom, self.sqm)
            server.sendmail(self.msgFrom, msgTo, msg.as_string())
            # s = smtplib.SMTP("localhost")
            # s.send_message(msg)
            print('well')
        except:
            print('error')
        finally:
            server.quit()



def main():
    msgTo = ''
    text = u''
    mail = sendemail()
    mail.sendto(msgTo, text)
if __name__ == '__main__':
    main()





