客户端基于socket，服务端基于socketserver 写的一个FTP，获取文件，上传文件的脚本
加入用户认证
用法：
    get 文件名
    put 文件名
使用conf.ini 作为配置文件，
[ipconfig] #为ip套接字
ip=127.0.0.1
port=8989

[user_info] #为用户名密码
user=tt
password=123
初学者，希望多多指教