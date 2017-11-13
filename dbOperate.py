# -*- coding:utf-8 -*-

# 数据库操作类
import pymysql
import random
import string
import time
import sendemail
class operateMySql:
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.passwd = 'qq596167'
        self.db = 'reminder'

    # 用户注册
    def addUser(self, user_name, user_psw, user_email,  phone_num):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset='UTF8')
        cur = db.cursor()
        # 查询用户是否已存在
        sql = ("""SELECT * FROM user WHERE user_email = '%s' """% (user_email))

        # 执行sql语句
        cur.execute(sql)
        # 用户已存在
        if cur.fetchall():
            db.close()
            return -1 #("用户已存在,请直接登录")
        else:
        # 用户不存在
            # SQL 插入语句
            sql =("""INSERT INTO user(user_name,
                user_psw, user_email,  phone_num)
                VALUES ('%s', '%s', '%s', '%s')"""%(user_name, user_psw, user_email, phone_num))
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
    def login(self, user_email, user_psw):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset='UTF8')
        cur = db.cursor()
        # 查询用户是否存在
        sql = ("""SELECT * FROM user WHERE user_email =
                '%s' and user_psw = '%s' """% (user_email, user_psw))
        
        # 执行sql语句
        cur.execute(sql)
        if cur.fetchall():
            # 用户存在
            db.close()
            return 1 # ("登陆成功")
        else:
            db.close()
            return 0 #("邮箱或密码错误，请重新登录")

    # 添加事件

    def addEvent(self, user_email, time, email_active, clock_active, phone_active, description):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset='UTF8')
        cur = db.cursor()
        # 随机生成事件id
        while True:
            event_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            # 查询事件的的id
            cur.execute("""select * from event where event_id = '%s'"""%(event_id))
            if cur.fetchall():
                pass
            else:
                break
        print(event_id)
        # 添加事件
        sql = ("""insert into event(event_id, user_email, time, description, email_active, clock_active, phone_active) values('%s', '%s', '%s', '%s', '%d', '%d', '%d')"""
               % (event_id, user_email, time, description, email_active, clock_active, phone_active))
        try:
            cur.execute(sql)
            db.commit()
            db.close()
            return event_id #("创建成功")
        except:
            db.rollback()
            db.close()
            return '0' #("创建失败")

    def subEvent(self, event_id):
        db = pymysql.connect(host = self.host, port = self.port, user = self.user, passwd = self.passwd, db = self.db, charset='UTF8')
        cur = db.cursor()
        sql = ("""delete from event where event_id = '%s' """%(event_id))
        try:
            cur.execute(sql)
            db.commit()
            db.close()
            return 1 #("删除成功")
        except:
            db.rollback()
            db.close()
            return 0 #("删除失败")
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
                    """select * from event where UNIX_TIMESTAMP(time) = '%d' and email_active = '%d'""" % (
                        int(time.time()), 1))
                cur.execute(sql)
                res = cur.fetchall()
                if res:
                    for row in res:
                        text = row[3]
                        email = row[1]
                        # 发送email
                        Send = sendemail.sendemail()
                        Send.sendto(email, text)
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
    print(s.addEvent("123@134.com", "qilai","2006-10-03 09:11:20",1,0,0))
    print(s.subEvent("b3xQOIwN"))
if __name__ == '__main__':
    main()
