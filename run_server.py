# -*- coding:utf-8 -*-
import sys
import socket
import threading
import dbOperate
from struct import *
import dataOp
import time
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
        # print(Data)
        data = Data
        print(len(data))
        struct_data = dataOp.dataConvert(data= data)
        res = struct_data.dataParse()
        print(res)
        # 注册
        if data[0] == 0:
            ret = db_op.addUser(res[0], res[1], res[2])
            print(ret)
            if  ret == 0:
                msg = b'\x00'
                sock.send(msg)
                #sock.send("sorry".encode())
            else:
                msg = b'\x01'
                sock.send(msg)
                #sock.send("succeed".encode())
        # 登陆
        elif data[0] == 1:
            ret = 0
            if len(res[0]) > 0:
                ret = db_op.login(res[0], res[1], res[2], 1)
            elif len(res[1]) > 0:
                ret = db_op.login(res[0], res[1], res[2], 0)
            if ret == 0:
                msg = b'\x00'
                sock.send(msg)
            else:
                msg = b'\x01'
                sock.send(msg)
        # 同步
        elif data[0] == 2:
            ret = 0
            # 修改
            if res[5] == '0':
                update_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

                ret = db_op.modifyEvent(res[2],res[0], res[4], res[6], res[12], update_time, res[8], res[9],
                                        res[10], res[11])
                print(ret)
            # 删除事件
            if res[5] == '1':
                ret = db_op.subEvent(res[0], res[4])
            if ret == 1:
                msg = b'\x01'
                sock.send(msg)
            else:
                sock.send(b'\x00')
        # 下载
        elif data[0] == 3:
            ret = db_op.loadDown(res[0], res[1], res[2])
            print(ret)
            if len(ret) > 0:
                for event in ret:
                    send_data = bytes()
                    send_data += b'\x05'
                    # title
                    send_data += b'\x00'
                    title_len = len(event[2])
                    send_data += pack('B',title_len)
                    send_data += event[2].encode()
                    # update_time
                    send_data += b'\x01'
                    update_len = len(event[4])
                    send_data += pack('B',update_len)
                    send_data += event[4].encode()
                    # alarm_time
                    send_data += b'\x02'
                    alarm_len = len(event[5])
                    send_data += pack('B', alarm_len)
                    send_data += event[5].encode()
                    # action_time
                    send_data += b'\x03'
                    action_len = len(event[6])
                    send_data += pack('B', action_len)
                    send_data += event[6].encode()
                    # if_alarm
                    send_data += b'\x04'
                    if_alarm_len = len(event[7])
                    send_data += pack('B', if_alarm_len)
                    send_data += event[7].encode()
                    # if_email
                    send_data += b'\x05'
                    if_email_len = len(event[8])
                    send_data += pack('B', if_email_len)
                    send_data += event[8].encode()
                    # record
                    # send_data += b'\x04'
                    record_len = len(event[3])
                    send_data += pack('i', record_len)
                    send_data += event[3].encode()
                    sock.send(send_data)
            else:
                sock.send(b'')
        #sock.close()


def getquery():
    db_op = dbOperate.operateMySql()
    db_op.regQuery()


def test_server(port=2592):
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
    s = threading.Thread(target=getquery)
    s.start()
    test_server(port=2592)


if __name__ == "__main__":
    main()
