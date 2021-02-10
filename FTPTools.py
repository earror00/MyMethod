# _*_coding:utf-8_*_
import os
from ftplib import FTP
from Utils import Utils
import socket
import urllib.request


class FTPTools:
    """
    :ip: FTP服务器的地址
    :port：连接的端口号，大多数时候默认21
    :username：登录FTP的账号，如果允许匿名登录则可将其置为空字符串
    :password：登录FTP的密码
    """

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.currentDir = '/mnt/work/FTP/'
        self.upload_address = ''
        self.ftp = FTP()
        self.util = Utils()

    # 连接并登录FTP
    def connect_ftp(self):
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

    # 关闭FTP连接
    def close_ftp(self):
        self.ftp.quit()
        self.util.write_log('connect FTP(%s:%s) closed ' % (self.host, self.port))

    # 上传文件至FTP
    def upload_file(self, des_path, sourceFilePath, fileName):
        file = open(os.path.abspath(sourceFilePath), 'rb')
        try:
            self.ftp.cwd(self.currentDir + des_path)
            self.ftp.storbinary('STOR %s.log' % fileName, file)
            self.util.write_log('upload %s successfully' % fileName)
            file.close()
        except socket.error as e:
            self.util.write_log('Error: upload file failed')
            self.close_ftp()

    # 删除FTP服务器中的文件,输入的路径为相对路径
    def delete_file(self, filePath, fileName):
        try:
            self.ftp.cwd(filePath)
            self.ftp.delete(fileName)
            self.util.write_log('delete %s successfully' % fileName)
        except Exception as e:
            print(e)
            self.util.write_log('Error:delete %s failed' % fileName)
            self.close_ftp()

    def download_file(self, source_path, des_path, fileName):
        """
        :从FTP下载文件, 文件下载到当前目录
        :source_path: 文件在FTP中的路径
        :des_path: 文件存储在本地的目标路径
        :fileName: 需要下载的文件名，包含后缀
        :zipSrc: zip文件的路径
        :desDir: 解压缩的目标路径
        :return: 返回文件解压后的绝对路径
        """
        # try:
        file_handler = open(des_path + fileName, 'wb')
        self.ftp.cwd(source_path)
        self.ftp.pwd()
        self.ftp.retrbinary('RETR ' + fileName, file_handler.write)
        self.util.write_log('%s downloaded successfully' % fileName)
        zip_src = des_path + fileName
        des_dir = des_path + '/' + fileName.replace('.zip', '') + '/'
        self.util.decompressed_file(zip_src, des_dir)
        return os.path.abspath(des_dir)
        # except Exception as e:
        #     self.util.write_log('Error: ' + str(e))
        #     self.util.write_log('transform failed')

    # 输入url地址，下载文件到FTP
    def trans_to_ftp(self, git_url, tag, des_path):
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

    # 在FTP服务器上创建目录
    def mkdir_ftp(self, dir_list):
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
