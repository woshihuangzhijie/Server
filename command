
客户端给服务器发送的数据格式，每个属性之间用制表符隔开
[0-4]
{
  "commandOptions":{
    "create user": "0",

    "user login": "1",

    "create event": "2",

    "delete event": "3",

    "user logout": "4"
  }
}
if 0:
    客户端给服务器发送的数据格式
    user_name + user_password + email + user_phone_number;
    服务器返回：
    创建成功： 1
    创建失败： 0
    用户已存在：-1
if 1:
    客户端给服务器发送的数据格式
    email + user_password
    服务器返回：
    登录成功： 1 + user_name + email + user_phone_number +
            格式化文件
            (event);

    登录失败： 0
    用户不存在： -1

if 2:
    客户端给服务器发送的数据格式
    user_email + datetime + email_active + clock_active + phone_active +  event_description
    服务器返回：
    创建成功：1 + event_id +
    创建失败：0
if 3:
    客户端给服务器发送的数据格式
    user_email + event_id
    服务器返回：
    删除成功：1
    删除失败：0




