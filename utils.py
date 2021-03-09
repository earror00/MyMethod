# -*- coding: utf-8 -*-
# ---
# @Institution: MyMethod
# @Time: 2021年3月4日
# @File: utils.py
# @Author: Earror
# @E-mail: earor@outlook.com
# @Desc: Function of this file
# @update: Record important updates
# ---

import os
import subprocess
import time
import zipfile

from loguru import logger


class Utils:
    def __init__(self):
        self.current_path = os.path.abspath(os.path.dirname(__file__))

    def init_dir(self):
        """
        : 创建必要的文件夹目录
        """
        if not os.path.exists('Log'):
            os.mkdir('Log')

    def make_dir(self, creat_dirname):
        """
        : 在当前目录下创建目录
        :param creat_dirname: 需要被创建的目录，相对路径，格式为test1/test2/test3/
        """
        if os.path.exists(creat_dirname):
            self.write_log('The directory  %s already exists and does not need to be created'
                           % creat_dirname)
        else:
            self.write_log('creat a new directory')
            os.makedirs(creat_dirname)
            for root, dirs, file in os.walk(self.current_path):
                if creat_dirname in dirs:
                    self.write_log('%s Directory created successfully' % creat_dirname)
                else:
                    self.write_log('%s Directory creation failed' % creat_dirname)
                break

    def write_log(self, log_info):
        """
        :param log_info: log内的内容
        :return:
        """
        runtime_log_path = os.path.abspath(os.path.dirname(__file__))
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当前时间
        log_time = time.strftime('%Y%m%d', time.localtime(time.time()))
        file = open(runtime_log_path + '\\Log\\' + 'Log_' + log_time + '.log', 'a+',
                    encoding='utf-8')
        formatted_log = curr_time + ": " + log_info + "\n"
        file.write(formatted_log)
        file.close()

    def addr_translator(self, git_url, h_code):
        """
        : 裁剪git地址，转换成以.zip结尾的zip文件下载地址，该地址拼接规则仅适用于内部搭建的gitblit仓库
        :param git_url git仓地址
        :param h_code git仓中与tag相对应的hash值
        :return 拼接处的最终下载地址
        """
        temp_addr = git_url.replace('/r/', '/zip/?r=') + '&h=' + h_code + '&format=zip'
        # 如果传入的git地址存在用户名，将用户名替换掉，如果不存在，则temp_addr即为最终下载地址
        if '@' in temp_addr:
            final_addr = 'http://' + temp_addr.split('@')[1]
        else:
            final_addr = temp_addr
        return final_addr

    def get_tag_cmd(self, git_url):
        """
        : 通过cmd命令直接执行git指令，获得tag和hash_code, 存在的隐患是，如果执行环境中没有安装git，该命令失效
        :param git_url: 代码的git地址
        """
        command = 'git ls-remote --tag' + ' ' + git_url
        pope = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        pope.wait()
        self.write_log('Git tag retrieved successfully')
        lines = pope.stdout.readlines()
        return [line.decode('gbk') for line in lines]

    def crop_tag_result(self, tag_result):
        """
        对通过cmd命令获取到的结果进行裁切，将结果保存到字典中，key为tag，value为hash_code
        :param tag_result: 裁剪结果，类型为字典
        :return
        """
        crop_result = {}
        for temp in tag_result:
            # 查询结果中带^{}和不带^{}的最终指向的文件是一样的
            if '^{}' not in temp and 'HEAD':
                key = temp.split('/')[2].replace('\n', '')
                value = temp.split("/")[0].replace('\trefs', '')
                crop_result.update({key: value})
            else:
                continue
        self.write_log('The tag and hash value were successfully stored in the dictionary')
        return crop_result

    def get_store_dir(self, category, customer, project, script_number):
        path = ('%s/%s/%s/%s/%s/%s/%s' % ('Macallan', '15A', 'Scripts', category, customer,
                                          project, script_number))
        return path

    def make_dir_by_level(self, new_dir_path):
        """
        : 逐级创建文件夹
        :param new_dir_path: 需要创建的目录，格式为test1\\test2\\test3\\
        """
        dir_list = new_dir_path.split('\\')
        try:
            for dirs in dir_list:
                if os.path.exists(os.path.join(os.getcwd(), dirs)):
                    self.write_log('The %s directory already exists' % dirs)
                    os.chdir(os.path.join(os.getcwd(), dirs))
                else:
                    self.write_log('%s Directory does not exist, '
                                   'create this directory and switch to it' % dirs)
                    os.mkdir(dirs)
                    os.chdir(os.path.join(os.getcwd(), dirs))
        except IOError as err:
            self.write_log('Creating directory Error: ' + str(err))
        return os.path.abspath(os.getcwd())

    def compressed_dir(self, file_path, file_name):
        """
        压缩指定文件夹内的所有内容
        :param file_path: 文件夹的绝对路径 xxx\\xxx
        :param file_name: 压缩后的文件名称 xxx
        """
        zip_file = zipfile.ZipFile(file_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
        logger.info('start compress folder....')
        for dirpath, dirnames, filenames in os.walk(file_path):
            for filename in filenames:
                logger.info('....add %s to zipfile....' % filename)
                zip_file.write(os.path.join(dirpath, filename))
        logger.success('Compressed folder: %s successfully' % file_name)
        zip_file.close()

    def decompressed_file(self, filepath, des_dir):
        """
        : 解压文件
        :filepath: zip压缩文件的路径 xxx\\xxx.zip
        :des_dir: 文件解压的目标路径 xxx\\
        """
        file = zipfile.is_zipfile(filepath)
        if file:
            zip_file = zipfile.ZipFile(filepath, 'r')
            for files in zip_file.namelist():
                zip_file.extract(files, des_dir)
            logger.success("zip file decompressed successfully")
            zip_file.close()
            os.remove(filepath)
            logger.success('ZIP file deleted successfully')
        else:
            logger.error("This is not zip file")


logger: logger
log_time = time.strftime('%Y%m%d', time.localtime(time.time()))
logger.add(f".\\Log\\Runtime_Log_{log_time}.log", rotation="500MB", encoding="utf-8", enqueue=True, compression="zip",
           retention="10 days")
