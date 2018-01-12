# -*- coding:utf-8 -*-
import sys
import socket
import threading
import dbOperate
from struct import *

def threadfun(sock, addr):
    Data = bytes()
    Data = sock.recv(2048)
    print(Data)
    # Len = unpack('i',d[:4])[0]
    # print(Len)
    # Data += d
    # while len(Data) < (Len + 4):
    #     d = sock.recv(2048)
    #     Data += d
        # print(len(d))
        # print(Data)
        # s = b'\x81'
        # sock.send(Data)
    # sock.send(b'\x81')
    # sock.send('succeed'.encode())
    if len(Data) > 0:
        db_op = dbOperate.operateMySql()
        # sock.send(("{0}".format(Data)).encode())
        # b'\x00' ~ b'\xff'
        #print(Data)
        data = Data
        print(len(data))
        if data[0] == 0:
            # 表项数
            item_num = data[1]
            # 检查表项数
            check_num = 0
            n = 2
            #print(len(data))
            while (n < len(data)):
                # 表项头
                item_header = data[n]
                n += 1
                # 表项长度
                item_len = data[n]
                # print(item_len)
                n += 1
                # email
                print(item_header)
                if item_header == 0:
                    # email = str()
                    # for i in range(item_len):
                    #     email += chr(ord(data[n + i]))
                    email = data[n:(n + item_len)].decode()
                    check_num += 1
                # psw
                elif item_header == 1:
                    # psw = str()
                    # for i in range(item_len):
                    #     psw += chr(ord(data[n + i]))
                    psw = data[n:(n + item_len)].decode()
                    check_num += 1
                # usr_name
                elif item_header == 2:
                    # usr_name = str()
                    # for i in range(item_len):
                    #     usr_name += chr(ord(data[n + i]))
                    usr_name = data[n:(n + item_len)].decode()
                    check_num += 1
                else:
                    break
                n += item_len

                if check_num == item_num:
                    ret = db_op.addUser(usr_name, psw, email)
                    print(ret)
                    if ret == 0:
                        msg = b'\x00'
                        sock.send(msg)
                        #sock.send("sorry".encode())
                    else:
                        msg = b'\x01'
                        sock.send(msg)
                        # sock.send("succeed".encode())
        elif data[0] == 1:
            # 表项数
            item_num = data[1]
            # 检查表项数
            check_num = 0
            n = 2
            while (n < len(data)):
                # 表项头
                item_header = data[n]
                n += 1
                # 表项长度
                item_len = data[n]
                n += 1
                # email
                if item_header == 0:
                    # email = str()
                    # for i in range(item_len):
                    #     email += chr(ord(data[n + i]))
                    email = data[n:(n + item_len)].decode()
                    check_num += 1
                # psw
                elif item_header == 1:
                    # psw = str()
                    # for i in range(item_len):
                    #     psw += chr(ord(data[n + i]))
                    psw = data[n:(n + item_len)].decode()
                    check_num += 1
                # usr_name
                elif item_header == 2:
                    # usr_name = str()
                    # for i in range(item_len):
                    #     usr_name += chr(ord(data[n + i]))
                    usr_name = data[n:(n + item_len)].decode()
                    check_num += 1
                n += item_len

                
                if check_num == item_num:
                    
                    if len(usr_name) > 0:
                        ret = db_op.login(usr_name, email, psw, 1)
                    elif len(email) > 0:
                        ret = db_op.login(usr_name, email, psw, 0)

                    if  ret == 0:
                        msg = b'\x00'
                        sock.send(msg)
                    else:
                        msg = b'\x01'
                        sock.send(msg)
        elif data[0] == 2:
            # 表项数
            item_num = data[1]
            # 检查表项数
            check_num = 0
            n = 2
            while (n < len(data)):
                # 表项头
                item_header = data[n]
                n += 1
                # 表项长度
                item_len = data[n]
                n += 1
                # email
                if item_header == 0:
                    # email = str()
                    # for i in range(item_len):
                    #     email += chr(ord(data[n + i]))
                    email = data[n:(n + item_len)].decode()
                    check_num += 1
                    n += item_len
                # psw
                elif item_header == 1:
                    # psw = str()
                    # for i in range(item_len):
                    #     psw += chr(ord(data[n + i]))
                    psw = data[n:(n + item_len)].decode()
                    check_num += 1
                    n += item_len
                # usr_name
                elif item_header == 2:
                    # usr_name = str()
                    # for i in range(item_len):
                    #     usr_name += chr(ord(data[n + i]))
                    usr_name = data[n:(n + item_len)].decode()
                    check_num += 1
                    n += item_len
                elif item_header == 3:
                    token = data[n:(n + item_len)].decode()
                    check_num += 1
                    n += item_len
                elif item_header == 4:
                    reminder = data[n:(n + item_len)].decode()
                    check_num += 1
                    n += item_len
                elif item_header == 5:
                    operation = data[n:(n + item_len)].decode()
                    check_num += 1
                    n += item_len

                # 读取备忘录数据
                if check_num == item_num:
                    attr_num = data[n]
                    check_attr_num = 0
                    n += 1
                    attr = 0
                    while (check_attr_num < attr_num):
                        attr_id = data[n]
                        n += 1
                        if attr_id == 0:
                            attr_len = data[n]
                            n += 1
                            title = data[n:(n + attr_len)].decode()
                            n += attr_len
                            check_attr_num += 1
                        elif attr_id == 1:
                            attr_len = data[n]
                            n += 1
                            update_time = data[n:(n + attr_len)].decode()
                            n += attr_len
                            check_attr_num += 1
                        elif attr_id == 2:
                            attr_len = data[n]
                            n += 1
                            alarm_time = data[n:(n + attr_len)].decode()
                            n += attr_len
                            check_attr_num += 1
                        elif attr_id == 3:
                            attr_len = data[n]
                            n += 1
                            action_time = data[n:(n + attr_len)].decode()
                            n += attr_len
                            check_attr_num += 1
                        elif attr_id == 4:
                            attr_len = data[n]
                            n += 1
                            if_alarm = data[n:(n + attr_len)].decode()
                            n += attr_len
                            check_attr_num += 1
                        elif attr_id == 5:
                            attr_len = data[n]
                            n += 1
                            if_email = data[n:(n + attr_len)].decode()
                            n += attr_len
                            check_attr_num += 1
                    if n < len(data):
                        record_len = unpack('i', data[n:(n+4)])[0]
                        # record_len = data[n] + 256 * data[n + 1] + \
                        #     (256 ** 2) * data[n + 2] + (256 ** 3) * data[n + 3]
                        n += 4
                        record = data[n:(n + record_len)].decode()
            
            # 修改
            if operation == '0':
                ret = db_op.modifyEvent(email, reminder, title, record, update_time, alarm_time, action_time,
                                        if_alarm, if_email)
            # 删除事件
            if operation == '1':
                ret = db_op.subEvent(email, reminder)

            if ret == 0:
                msg = b'\x00'
                sock.send(msg)
            else:
                sock.send(b'\x01')
        

def getquery():
    db_op = dbOperate.operateMySql()
    db_op.regQuery()


def test_server(port=3600):
    # 创建TCP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 启用地址重用
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定地址和端口号
    srv_addr = ("0.0.0.0", port)
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
    # s = threading.Thread(target=getquery)
    # s.start()
    test_server(port=3600)


if __name__ == "__main__":
    main()
