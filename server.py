# -*- coding:utf-8 -*-
import sys
import socket
import threading
import dbOperate
def threadfun(sock, addr):
    # sock.send(("裂解陈功").encode())
    while True:
        data = sock.recv(1024).decode()
        # print(str(data))
        # sock.send(("hello,{0}".format(data)).encode())
        # if data == 'quit' or data == 'exit':
        #     print('Client {0} exit'.format(addr[0]))
        #     break
        if data:
            db_op = dbOperate.operateMySql()
            data_list = data.split('\0')
            print(data_list)
            # 用户注册
            if data_list[0] == '0':
                ret = db_op.addUser(data_list[1], data_list[2], data_list[3], data_list[4])
                if ret == 1:
                    sock.send(("创建成功").encode())
                elif ret == 0:
                    sock.send(("创建失败").encode())
                else:
                    sock.send(("用户已存在").encode())
            # 登录
            elif data_list[0] == '1':
                ret = db_op.login(data_list[1], data_list[2])
                if ret == 1:
                    # sock.send()
                    sock.send(("登录成功").encode())
                else:
                    sock.send(("邮箱或密码错误，请重新登录").encode())
            # 创建事件
            elif data_list[0] == '2':
                # user_email + event_description + datetime + email_active + clock_active + phone_active
                ret = db_op.addEvent(data_list[1], data_list[2], data_list[3], int(data_list[4]), int(data_list[5]), int(data_list[6]))
                if ret == '0':
                    sock.send(("创建失败").encode())
                else:
                    sock.send((ret).encode())
            elif data_list[0] == '3':
                ret = db_op.subEvent(data_list[2])
                if ret == '1':
                    sock.send(("删除成功").encode())
                else:
                    sock.send(("删除失败").encode())
            else:
                sock.send(("格式错误").encode())
    sock.close()
def getquery():
    db_op = dbOperate.operateMySql()
    db_op.regQuery()
def test_server(port = 2592):

    # 创建TCP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 启用地址重用
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定地址和端口号
    srv_addr = ("127.0.0.1", port)
    sock.bind(srv_addr)
    # 侦听客户端
    sock.listen(5)
    while True:
        # 接受客户端连接
        conn, addr = sock.accept()
        # sock.send(("用户已存在").encode())
        t = threading.Thread(target=threadfun, args=(conn, addr))
        t.start()

def main():
    s = threading.Thread(target=getquery)
    s.start()
    test_server(port = 2592)


if __name__ == "__main__":
    
    main()
    
