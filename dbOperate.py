# -*- coding:utf-8 -*-

# 数据库操作类
import pymysql
import random
import string
import time
import sendemail
class operateMySql:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.user = 'root'
        self.passwd = ''
        self.db = 'reminder'

    # 用户注册
    def addUser(self, user_name, user_psw, user_email):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset='UTF8')
        cur = db.cursor()
        # 查询用户是否已存在
        sql = ("""SELECT * FROM user WHERE user_email = '%s' """% (user_email))

        # 执行sql语句
        cur.execute(sql)
        # 用户已存在
        if cur.fetchall():
            db.close()
            return 0 #("用户已存在,请直接登录")
        else:
        # 用户不存在
            # SQL 插入语句
            sql =("""INSERT INTO user(user_name,
                user_psw, user_email, token)
                VALUES ('%s', '%s', '%s', '%s')"""%(user_name, user_psw, user_email, '1'))
            try:
                # 执行sql语句
                cur.execute(sql)
                # 提交到数据库执行
                db.commit()
                db.close()
                return 1 # ("注册成功")
            except:
                # 如果发生错误则回滚
                db.rollback()
                db.close()
                return 0 #("注册失败")

    # 用户登录
    def login(self, user_name, user_email, user_psw, flag):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset='UTF8')
        cur = db.cursor()
        # 查询用户是否存在
        if flag == 0:
            sql = ("""SELECT * FROM user WHERE user_email =
                '%s' and user_psw = '%s' """% (user_email, user_psw))
        else:
             sql = ("""SELECT * FROM user WHERE user_name =
                '%s' and user_psw = '%s' """ % (user_name, user_psw))
        # 执行sql语句
        cur.execute(sql)
        if cur.fetchall():
            # 用户存在
            if flag == 0:
                op = ("""UPDATE user SET token = '%s' WHERE user_email =
                '%s' and user_psw = '%s' """ % ('1', user_email, user_psw))
            else:
                op = ("""UPDATE user SET token = '%s' WHERE user_name =
                '%s' and user_psw = '%s' """ % ('1', user_name, user_psw))
            cur.execute(op)
            db.close()
            return 1 # ("登陆成功")
        else:
            db.close()
            return 0 #("邮箱或密码错误，请重新登录")
    # 添加事件
    
    def modifyEvent(self,user_name, email, reminder, title, record, update_time, alarm_time, action_time, if_alarm, if_email):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset='UTF8')
        cur = db.cursor()
        # 查询事件的的id
        if len(email) > 0:
            cur.execute("""select * from event where user_email = '%s' and  reminder = '%s'""" % (email, reminder))
        else:
            cur.execute("""select * from user where user_name = '%s' """ % (user_name))
            r = cur.fetchall()[0]
            print(r)
            email = r[2]
            cur.execute("""select * from event where user_email = '%s' and  reminder = '%s'""" % (r[2], reminder))
        if cur.fetchall():
            # 修改事件
             sql = ("""UPDATE event SET title = '%s', record = '%s', update_time = '%s',alarm_time = '%s',action_time = '%s',
             if_alarm = '%s', if_email = '%s' where user_email = '%s' and  reminder = '%s'""" % (title, record, update_time, 
             alarm_time, action_time, if_alarm, if_email, email, reminder))
        else:
            # 添加事件
            print((email, reminder, title, record, update_time, alarm_time, action_time, if_alarm, if_email))
            sql = ("""INSERT into event(user_email, reminder, title, record, update_time, alarm_time, action_time, if_alarm, if_email) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')"""
                    % (email, reminder, title, record, update_time, alarm_time, action_time, if_alarm, if_email))
        try:
            cur.execute(sql)
            db.commit()
            db.close()
            return 1 #("修改成功")
        except:
            db.rollback()
            db.close()
            return 0 #("创建失败")

    def subEvent(self,user_email, reminder):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset='UTF8')
        cur = db.cursor()
        sql = ("""delete from event where user_email = '%s' and reminder = '%s' """ % (
            user_email, reminder))
        try:
            cur.execute(sql)
            db.commit()
            db.close()
            return 1 #("删除成功")
        except:
            db.rollback()
            db.close()
            return 0
    def loadDown(self,user_name, user_email, user_psw):
        db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                             charset='UTF8')
        cur = db.cursor()
        # 查询用户是否存在
        if len(user_email) > 0:
            sql = ("""SELECT * FROM user WHERE user_email =
                        '%s' and user_psw = '%s' """ % (user_email, user_psw))
        if len(user_name) > 0:
            sql = ("""SELECT * FROM user WHERE user_name =
                        '%s' and user_psw = '%s' """ % (user_name, user_psw))
        cur.execute(sql)
        res = cur.fetchall()
        if res:
            email = res[0][2]
            SQL = ("""select * from event where user_email = '%s' """ % (email))
            cur.execute(SQL)
            event = cur.fetchall()
            db.close()
            return event

    def regQuery(self, interval = 60):
        while True:
            try:
                # sleep for the remaining seconds of interval
                time_remaining = interval - time.time() % interval
                time.sleep(time_remaining)
                db = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                     charset='UTF8')
                cur = db.cursor()
                # 选择时间已到的事件
                sql = (
                    """select * from event where UNIX_TIMESTAMP(alarm_time) = '%d' and if_email = '%s'""" % (
                        int(time.time()), '1'))
                cur.execute(sql)
                res = cur.fetchall()
                if res:
                    for row in res:
                        print(row)
                        msgto = row[0]
                        title = row[2]
                        alarm_time = row[5]
                        action_time = row[6]
                        delta = action_time - alarm_time
                        #print(delta.days, delta.seconds)
                        days = delta.days
                        hours = delta.seconds // 3600
                        minutes = delta.seconds // 60
                        #print(hours, minutes, seconds)
                        text = ('您好，您的事件' + title + '还有' + str(days) + '天' + str(hours)
                            + '小时' + str(minutes) + '分就要开始了')
                        # 发送email
                        Send = sendemail.sendemail()
                        Send.sendto(msgto, text)
                else:
                    pass
                db.close()
            except Exception as e:
                print(e)
def main():
    s = operateMySql()
    # print(s.addUser("john", "123@134.com", "1234"))
    # print(s.login("123@134.com", "1234"))
    # print(s.login("123@134.com", "123"))
    #self, email, reminder, title, record, update_time, alarm_time, action_time, if_alarm, if_email):
    print(s.regQuery())
    #print(s.subEvent("b3xQOIwN"))
if __name__ == '__main__':
    main()
