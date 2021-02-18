# _*_coding:utf-8_*_
import os
from ftplib import FTP
from Utils import Utils
import socket
import urllib.request


class FTPTools:

    def __init__(self, host, port, username, password):
        """
        : 初始化，将FTP的各类信息导入
        :param host: FTP服务器的地址
        :param port：连接的端口号，大多数时候默认21
        :param username：登录FTP的账号，如果允许匿名登录则可将其置为空字符串
        :param password：登录FTP的密码
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.currentDir = '/mnt/work/FTP/'
        self.upload_address = ''
        self.ftp = FTP()
        self.util = Utils()

    def connect_ftp(self):
        """
        : 连接并登录FTP
        """
        try:
            self.ftp.connect(self.host, self.port)
            self.util.write_log('connect FTP(%s:%s) successfully' % (self.host, self.port))
            self.ftp.set_debuglevel(2)
            self.ftp.login(self.username, self.password)
            self.util.write_log('login FTP(%s:%s) successfully' % (self.host, self.port))
            self.ftp.getwelcome()
        except Exception as e:
            self.util.write_log('connect FTP(%s:%s) Error' % (self.host, self.port))
            self.util.write_log(e)
            self.close_ftp()

    def close_ftp(self):
        """
        : 关闭FTP连接
        """
        self.ftp.quit()
        self.util.write_log('connect FTP(%s:%s) closed ' % (self.host, self.port))

    def upload_file(self, des_path, source_path, filename):
        """
        :上传文件至FTP
        :param des_path: 上传至FTP的目标文件夹
        :param source_path: 需要上传的文件相对路径
        :param filename: 文件名
        """
        file = open(os.path.abspath(source_path), 'rb')
        try:
            self.ftp.cwd(self.currentDir + des_path)
            self.ftp.storbinary('STOR %s.log' % filename, file)
            self.util.write_log('upload %s successfully' % filename)
            file.close()
        except socket.error as e:
            self.util.write_log('Error: ' + e)
            self.util.write_log('upload file failed')
            self.close_ftp()

    def delete_file(self, filepath, filename):
        """
        :删除FTP服务器中的文件
        :param filepath: 文件的相对路径，从登陆FTP账号后的默认文件夹开始
        :param filename: 文件名，包含文件后缀
        """
        try:
            self.ftp.cwd(filepath)
            self.ftp.delete(filename)
            self.util.write_log('delete %s successfully' % filename)
        except Exception as e:
            self.util.write_log('Error: ' + str(e))
            self.util.write_log('delete %s failed' % filename)
            self.close_ftp()

    def download_file(self, source_path, des_path, filename):
        """
        :从FTP下载文件, 文件下载到当前目录
        :可能存在的异常: 文件操作异常，文件传输异常
        :param source_path: 文件在FTP中的路径
        :param des_path: 文件存储在本地的目标路径
        :param filename: 需要下载的文件名，包含后缀
        :zipSrc: zip文件的路径
        :desDir: 解压缩的目标路径
        :return: 返回文件解压后的绝对路径
        """
        try:
            file_handler = open(des_path + filename, 'wb')
            self.ftp.cwd(source_path)
            self.ftp.pwd()
            self.ftp.retrbinary('RETR ' + filename, file_handler.write)
            self.util.write_log('%s downloaded successfully' % filename)
            zip_src = des_path + filename
            des_dir = des_path + '/' + filename.replace('.zip', '') + '/'
            self.util.decompressed_file(zip_src, des_dir)
            file_handler.close()
            return os.path.abspath(des_dir)
        except Exception as e:
            self.util.write_log('Error: ' + str(e))
            self.util.write_log('transform failed')
            self.close_ftp()
            self.connect_ftp()

    def trans_to_ftp(self, git_url, tag, des_path):
        """
        输入url地址，下载文件到FTP
        存在的可能异常：通信异常
        :param git_url: 代码的git仓地址
        :param tag: 脚本的tag标签
        :param des_path: 存储在FTP中的位置
        """
        tag_dict = self.util.crop_tag_result(self.util.get_tag_cmd(git_url))
        url = self.util.addr_translator(git_url, tag_dict[tag])
        handle_file = urllib.request.urlopen(url)
        self.mkdir_ftp(des_path)
        self.ftp.cwd(des_path)
        self.ftp.storbinary('STOR %s.zip' % tag, handle_file)
        self.util.write_log('transform script from git to FTP successfully')
        self.ftp.cwd('/mnt/work/FTP')
        self.util.write_log('Switch to Root Directory')
        return des_path + '/'

    def mkdir_ftp(self, dir_list):
        """
        在FTP服务器上创建目录
        :param dir_list: 需要创建的目录，此处的输入格式为’test1/test2/test3/‘
        """
        self.ftp.cwd(self.currentDir)
        cur_dir_list = self.ftp.nlst(self.currentDir)
        self.util.write_log('current directory in FTP: %s ' % self.ftp.nlst(self.currentDir))
        root_dir = self.currentDir
        if '/' in dir_list:
            dir_list = dir_list.split('/')
            for dirs in dir_list:
                print(root_dir + dirs)
                if (root_dir + dirs) in cur_dir_list:
                    self.util.write_log('%s The folder already exists. Update the DIR list and enter the folder' % dirs)
                    cur_dir_list = self.ftp.nlst(root_dir + dirs + '/')
                    root_dir = root_dir + dirs + '/'
                else:
                    self.util.write_log('%s Folder does not exist, create the folder' % dirs)
                    self.ftp.mkd(root_dir + dirs)
                    cur_dir_list = self.ftp.nlst(root_dir + dirs + '/')
                    root_dir = root_dir + dirs + '/'
                    self.util.write_log(dirs + ' Directory creation completed')
        else:
            dir_namePath = root_dir + dir_list
            if dir_namePath not in cur_dir_list:
                self.util.write_log('FTP current directory do not exist %s, creat %s' % (dir_list, dir_list))
                self.ftp.mkd(dir_namePath)
                self.util.write_log('creat %s directory success' % dir_list)
            else:
                self.util.write_log('FTP current directory exist %s, do not creat %s' % (dir_list, dir_list))
        self.upload_address = root_dir
