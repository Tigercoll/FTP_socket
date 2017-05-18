#!/usr/bin/env python
#_*_coding:utf-8_*_
__author__ = "Tiger"
import socketserver
import os
import json
import configparser
class ftp_socket(socketserver.BaseRequestHandler):#继承BaseRequestHandler
    def get(self,*args,**kwargs):
        #get方法 下载文件
        filename = self.data['filename']
        if os.path.isfile (filename):
            self.data['size'] = os.stat (self.data['filename']).st_size
            self.request.send(json.dumps(self.data).encode('utf-8'))
            self.client.recv (1024)
            with open(filename,'rb') as f:
                for line in f:
                    self.request.send(line)
        else:
            self.data['status']=False





    def put(self,*args,**kwargs):
        #put方法，上传文件
        filename=self.data['filename']
        filesize=self.data['size']
        if os.path.isfile (filename):
            f = open (filename + ".new", "wb")
        else:
            f = open (filename, "wb")

        self.request.send (b"200 ok")
        received_size = 0
        while received_size < filesize:
            get_data = self.request.recv (1024)
            f.write (get_data)
            received_size += len (get_data)
        else:
            print ("file [%s] has uploaded..." % filename)
        f.close()
    def check_username(self):
        #用户名验证
        conf = configparser.ConfigParser ()
        conf.read ('conf.ini', encoding='utf-8')
        user=conf.get('user_info','user')
        passwd=conf.get('user_info','password')
        if self.user==user and self.passwd==passwd:
            return 0
        else:
            return 1
    def handle(self):
        #handle方法，
        self.data=json.loads(self.request.recv(1024).decode().strip())
        self.user=self.data['user']
        self.passwd=self.data['password']
        if self.user and self.passwd:
            result=self.check_username()
            if result==0:
                self.request.send (bytes (str (result), encoding='utf-8'))
                while True:
                    self.data = json.loads (self.request.recv (1024).decode ().strip ())
                    if self.data['cmd']:
                        if hasattr(self,self.data['cmd']):
                            func=getattr(self,self.data['cmd'])
                            func(self.data)
                    else:
                        continue
        else:
            result=1
        self.request.send (bytes (str (result), encoding='utf-8'))

if __name__=='__main__':
    server=socketserver.ThreadingTCPServer(('127.0.0.1',8989),ftp_socket)
    server.serve_forever()