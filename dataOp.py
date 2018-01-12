# -*- coding:utf-8 -*-
from struct import *


class dataConvert:
    def __init__(self, data):
        self.data = data
        self.service_type = data[0]

    def sign_up(self):
        item_num = self.data[1]
        # 检查表项数
        check_num = 0
        # 已解析的比特数
        n = 2
        email = str()
        psw = str()
        usr_name = str()
        # print(len(self.data))
        while (n < len(self.data)):
            # 表项头
            item_header = self.data[n]
            n += 1
            # 表项长度
            item_len = self.data[n]
            # print(item_len)
            n += 1
            # email
            print(item_header)
            if item_header == 0:
                email = self.data[n:(n + item_len)].decode()
                check_num += 1

            # psw
            elif item_header == 1:
                psw = self.data[n:(n + item_len)].decode()
                check_num += 1

            # usr_name
            elif item_header == 2:
                usr_name = self.data[n:(n + item_len)].decode()
                check_num += 1

            else:
                break
            n += item_len

            if check_num == item_num:
                return (usr_name, psw, email)
        return -1

    def sign_in(self):

        # 表项数
        item_num = self.data[1]
        # 检查表项数
        check_num = 0
        n = 2
        email = str()
        psw = str()
        usr_name = str()
        while (n < len(self.data)):
            # 表项头
            item_header = self.data[n]
            n += 1
            # 表项长度
            item_len = self.data[n]
            n += 1

            # email
            if item_header == 0:
                email = self.data[n:(n + item_len)].decode()
                check_num += 1

            # psw
            elif item_header == 1:
                psw = self.data[n:(n + item_len)].decode()
                check_num += 1

            # usr_name
            elif item_header == 2:
                usr_name = self.data[n:(n + item_len)].decode()
                check_num += 1

            else:
                break
            n += item_len

            if check_num == item_num:
                return (usr_name, email, psw)
        return -1

    def syn(self):
        # 表项数
        item_num = self.data[1]
        # 检查表项数
        check_num = 0
        n = 2
        email = str()
        psw = str()
        usr_name = str()
        token = str()
        reminder = str()
        operation = str()
        title = str()
        update_time = str()
        alarm_time = str()
        action_time = str()
        if_alarm = str()
        if_email = str()
        record = str()
        while (n < len(self.data)):
            # 表项头
            item_header = self.data[n]
            n += 1
            # 表项长度
            item_len = self.data[n]
            n += 1
            # email
            if item_header == 0:
                email = self.data[n:(n + item_len)].decode()
                check_num += 1
                n += item_len

            # psw
            elif item_header == 1:
                psw = self.data[n:(n + item_len)].decode()
                check_num += 1
                n += item_len

            # usr_name
            elif item_header == 2:
                # usr_name = str()
                # for i in range(item_len):
                #     usr_name += chr(ord(self.data[n + i]))
                usr_name = self.data[n:(n + item_len)].decode()
                check_num += 1
                n += item_len

            # token
            elif item_header == 3:
                token = self.data[n:(n + item_len)].decode()
                check_num += 1
                n += item_len

            # reminder id
            elif item_header == 4:
                reminder = self.data[n:(n + item_len)].decode()
                check_num += 1
                n += item_len

            # operation
            elif item_header == 5:
                operation = self.data[n:(n + item_len)].decode()
                check_num += 1
                n += item_len
            else:
                break

            # 读取备忘录数据
            if check_num == item_num:
                if n == len(self.data):
                    return (email,
                 psw,
                 usr_name,
                 token,
                 reminder,
                 operation,
                 title,
                 update_time,
                 alarm_time,
                 action_time,
                 if_alarm,
                 if_email,
                 record)
                # 属性个数
                attr_num = self.data[n]
                # 已检查的属性个数
                check_attr_num = 0

                n += 1

                attr = 0
                while (check_attr_num < attr_num):
                    # 属性表项
                    attr_id = self.data[n]
                    n += 1
                    # title
                    if attr_id == 0:
                        attr_len = self.data[n]
                        n += 1
                        title = self.data[n:(n + attr_len)].decode()
                        n += attr_len
                        check_attr_num += 1
                    # update_time
                    elif attr_id == 1:
                        attr_len = self.data[n]
                        n += 1
                        update_time = self.data[n:(n + attr_len)].decode()
                        n += attr_len
                        check_attr_num += 1
                    # alarm_time
                    elif attr_id == 2:
                        attr_len = self.data[n]
                        n += 1
                        alarm_time = self.data[n:(n + attr_len)].decode()
                        n += attr_len
                        check_attr_num += 1
                    # action_time
                    elif attr_id == 3:
                        attr_len = self.data[n]
                        n += 1
                        action_time = self.data[n:(n + attr_len)].decode()
                        n += attr_len
                        check_attr_num += 1
                    # if_alarm
                    elif attr_id == 4:
                        attr_len = self.data[n]
                        n += 1
                        if_alarm = self.data[n:(n + attr_len)].decode()
                        n += attr_len
                        check_attr_num += 1
                    # if_email
                    elif attr_id == 5:
                        attr_len = self.data[n]
                        n += 1
                        if_email = self.data[n:(n + attr_len)].decode()
                        n += attr_len
                        check_attr_num += 1
                if n < len(self.data):
                    record_len = unpack('i', self.data[n:(n + 4)])[0]
                    # record_len = self.data[n] + 256 * self.data[n + 1] + \
                    #     (256 ** 2) * self.data[n + 2] + (256 ** 3) * self.data[n + 3]
                    n += 4
                    record = self.data[n:(n + record_len)].decode()
                return (email,
                 psw,
                 usr_name,
                 token,
                 reminder,
                 operation,
                 title,
                 update_time,
                 alarm_time,
                 action_time,
                 if_alarm,
                 if_email,
                 record)
    def load(self):
        # 表项数
        item_num = self.data[1]
        # 检查表项数
        check_num = 0
        n = 2
        email = str()
        psw = str()
        usr_name = str()
        while (n < len(self.data)):
            # 表项头
            item_header = self.data[n]
            n += 1
            # 表项长度
            item_len = self.data[n]
            n += 1

            # email
            if item_header == 0:
                email = self.data[n:(n + item_len)].decode()
                check_num += 1

            # psw
            elif item_header == 1:
                psw = self.data[n:(n + item_len)].decode()
                check_num += 1

            # usr_name
            elif item_header == 2:
                usr_name = self.data[n:(n + item_len)].decode()
                check_num += 1

            else:
                break
            n += item_len

            if check_num == item_num:
                return (usr_name, email, psw)
        return -1
    def dataParse(self):
        if self.service_type == 0:
            return self.sign_up()
        elif self.service_type == 1:
            return self.sign_in()
        elif self.service_type == 2:
            return self.syn()
        elif self.service_type == 3:
            return self.load()
        else:
            return -1
