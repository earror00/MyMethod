# _*_coding:utf-8_*_
import os
import subprocess
import time

import zipfile
from os.path import join, getsize


class Utils:
    def __init__(self):
        self.currentPath = os.path.abspath(os.path.dirname(__file__))

    # 创建必要的文件夹目录
    def init_dir(self):
        if not os.path.exists('Log'):
            os.mkdir('Log')

    # 在当前目录下创建目录
    def make_dir(self, creat_dirname):
        if os.path.exists(creat_dirname):
            self.write_log('The directory  %s already exists and does not need to be created' % creat_dirname)
        else:
            self.write_log('creat a new directory')
            os.makedirs(creat_dirname)
            for root, dir, file in os.walk(self.currentPath):
                if creat_dirname in dir:
                    self.write_log('%s Directory created successfully' % creat_dirname)
                else:
                    self.write_log('%s Directory creation failed' % creat_dirname)
                break

    def write_log(self, info):
        format_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_file = 'Log_' + time.strftime("%Y%m%d") + '.log'
        f = open('.\\Log\\' + log_file, 'a+', encoding='utf-8')
        print(format_time + ': ' + info)
        f.write(format_time + ': ' + info + '\n')
        f.close()

    # 解压文件
    def decompressed_file(self, filePath, desDir):
        """
        :filePath: zip压缩文件的路径
        :desDir: 文件解压的目标路径
        """
        f = zipfile.is_zipfile(filePath)
        if f:
            fz = zipfile.ZipFile(filePath, 'r')
            for files in fz.namelist():
                fz.extract(files, desDir)
            self.write_log("zip file decompressed successfully")
            fz.close()
            os.remove(filePath)
            self.write_log('ZIP file deleted successfully')
        else:
            self.write_log("This is not zip file")

    # 裁剪git地址，转换成以.zip结尾的zip文件下载地址，该地址拼接规则仅适用于内部搭建的gitblit仓库，
    def addr_translator(self, git_url, h_code):
        """
        :git_url git仓地址
        :h_code git仓中与tag相对应的hash值
        :return 拼接处的最终下载地址
        """
        temp_addr = git_url.replace('/r/', '/zip/?r=') + '&h=' + h_code + '&format=zip'
        # 如果传入的git地址存在用户名，将用户名替换掉，如果不存在，则temp_addr即为最终下载地址
        if '@' in temp_addr:
            final_addr = 'http://' + temp_addr.split('@')[1]
        else:
            final_addr = temp_addr
        return final_addr

    # 通过cmd命令直接执行git指令，获得tag和hash_code, 存在的隐患是，如果执行环境中没有安装git，该命令失效
    def get_tag_cmd(self, git_url):
        command = 'git ls-remote' + ' ' + git_url
        popen = subprocess.Popen(command, stdout=subprocess.PIPE)
        popen.wait()
        self.write_log('Git tag retrieved successfully')
        lines = popen.stdout.readlines()
        return [line.decode('gbk') for line in lines]

    # 对通过cmd命令获取到的结果进行裁切，将结果保存到字典中，key为tag，value为hash_code
    def crop_tag_result(self, tag_result):
        crop_result = {}
        for i in range(3, len(tag_result)):
            temp = tag_result[i]
            key = temp.split('/')[2].replace('\n', '')
            value = temp.split("/")[0].replace('\trefs', '')
            crop_result.update({key: value})
        self.write_log('The tag and hash value were successfully stored in the dictionary')
        return crop_result

    def get_store_dir(self, category, customer, project, script_number):
        path = ('%s/%s/%s/%s/%s/%s/%s' % ('Macallan', '15A', 'Scripts', category, customer, project, script_number))
        return path

    def make_dir_by_level(self, new_dir_path):
        dir_list = new_dir_path.split('\\')
        try:
            for dirs in dir_list:
                if os.path.exists(os.path.join(os.getcwd(), dirs)):
                    self.write_log('The %s directory already exists' % dirs)
                    os.chdir(os.path.join(os.getcwd(), dirs))
                else:
                    self.write_log('%s Directory does not exist, create this directory and switch to it' % dirs)
                    os.mkdir(dirs)
                    os.chdir(os.path.join(os.getcwd(), dirs))
            return new_dir_path
        except Exception as e:
            self.write_log('Creating directory Error: ' + str(e))

