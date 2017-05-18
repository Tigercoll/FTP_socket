#!/usr/bin/env python
#_*_coding:utf-8_*_
__author__ = "Tiger"
import socket
import configparser
import json
import os

class FtpClient(object):
    def __init__(self):
        #引入configparser模块，加载配置文件
        conf=configparser.ConfigParser()
        conf.read('conf.ini',encoding='utf-8')
        self.ip=conf.get('ipconfig','ip')
        self.port=conf.getint('ipconfig','port')
        self.client=socket.socket()
        self.data={
            'user':'',
            'password':'',
            'cmd':'',
            'filename':'',
            'size':'',
            'status':True,
        }
    def connect(self):
        #链接服务端
        self.client.connect((self.ip,self.port))

    def login(self):
        #用户登录认证
        self.data['user'] = input ('user:').strip ()
        self.data['password'] = input ('password:').strip ()
        self.client.send(json.dumps(self.data).encode('utf-8'))
        result=self.client.recv(1024)
        return int(result)
    def interactive(self):
        #主业务函数

        while True:
            user_input=input('>>>:').strip()
            if len(user_input)==0:continue
            self.data['cmd'],self.data['filename']=user_input.split()
            #这里使用hasattr，getattr内置函数，动态加载
            if hasattr(self,self.data['cmd']):
                func=getattr(self,self.data['cmd'])
                func()
            else:
                self.help()
    def help(self):
        #帮助
        print('useage:get | put | help args' )
    def put(self):
        #put 函数，上传文件
        if os.path.isfile(self.data['filename']):
            self.data['size']=os.stat(self.data['filename']).st_size
            self.client.send(json.dumps(self.data).encode('utf-8'))
            self.client.recv(1024)
            with open(self.data['filename'],'rb') as f:
                for line in f:
                    self.client.send (line)
                else:
                    print('file is success...')
                    print(self.data)
        else:
            print(self.data['filename'],' is not exist')

    def get(self):
        #get 函数，获取文件
        self.client.send (json.dumps (self.data).encode ('utf-8'))
        ret=json.loads(self.client.recv(1024).decode())
        if ret['status']:
            if os.path.isfile(ret['filename']):
                f=open(ret['filename']+'.new','wb')
            else:
                f=open(ret['filename'],'wb')
            size=ret['size']
            file_size=0
            self.client.send(b'200 ok')
            while file_size<size:
                get_data=self.client.recv(1024)
                f.write(get_data)
                file_size+=len(get_data)
            else:
                print(ret['filename'],'is ok')
        else:
            print('文件不存在')
        f.close()
if __name__=='__main__':

    ftp=FtpClient()
    ftp.connect()
    if ftp.login()==0:
        ftp.interactive()
    else:
        print('登录失败')