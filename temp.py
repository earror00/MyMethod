# -*- coding:utf-8 -*-

import os
import shutil
from ftplib import FTP
import urllib.request
from imaplib import Debug

import git
from git.repo import Repo
import zipfile
import json

# startdir = "E:\Code\PycharmProject\Logkit\Storage"  # 要压缩的文件夹路径
# file_news = startdir + '.zip'  # 压缩后文件夹的名字
# z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
# for dirpath, dirnames, filenames in os.walk(startdir):
#     fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
#     fpath = fpath and fpath + os.sep or ''
#     for filename in filenames:
#         z.write(os.path.join(dirpath, filename), fpath + filename)
#         print('压缩成功')
# z.close()
''''''
# class test:
#
#     def __init__(self):
#         self.rootPath = ''
#         self.currentPath = ''
#         self.filePath = ''
#         self.jointPath = ''
#         self.current_dir = os.path.dirname(__file__)
#         self.resource_path = ''
#         self.PATH = ''
#
#     def get_directory(self):
#         self.currentPath = os.path.abspath(os.path.dirname(__file__))
#         self.filePath = os.path.split(os.path.realpath(__file__))
#         self.jointPath = os.path.join(self.currentPath, 'venv')
#         self.current_dir = os.path.dirname(__file__)
#         self.resource_path = os.path.join(os.path.dirname(self.current_dir), 'resources')
#         self.PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
#
#         print(self.currentPath)
#         print('============')
#         print(self.filePath)
#         print('============')
#         print(os.path.realpath(__file__))
#         print('============')
#         print(os.path.dirname(__file__))
#         print('============')
#         print(self.jointPath)
#         print('============')
#         print(os.path.join(os.path.dirname(self.currentPath)), 'venv')
#         print('============')
#         print(self.current_dir)
#         print('============')
#         print(self.resource_path)
#         print('============')
#         print(os.path.split(__file__)[0])
#         print('============')
#         print(os.path.splitext(__file__))
#         print('============')
#         print(self.PATH)
#         print(__file__)
#
#
# t = test()
# t.get_directory()
''''''
# def clone():
#     """
#     克隆代码
#     :return:
#     """
#     download_path = os.path.join('code')
#     Repo.clone_from('http://101013483@10.102.4.219:58443/r/Test/Vulcan_18115_basic_R.git', to_path=download_path,
#                     branch='master')

# def pull():
#     """
#     pull最新代码
#     :return:
#     """
#     local_path = os.path.join('code', 'codetest')
#     repo = Repo(local_path)
#     repo.git.pull()

# def get_branch():
#     """
#     获取所有分支
#     :return:
#     """
#     local_path = os.path.join('code', 'codetest')
#     repo = Repo(local_path)
#     branches = repo.remote().refs
#     for item in branches:
#         print(item.remote_head)

# def get_tags():
#     """
#     获取所有版本
#     :return:
#     """
#     local_path = os.path.join('code', 'codetest')
#     repo = Repo(local_path)
#     for tag in repo.tags:
#         print(tag.name)

# def get_commits():
#     """
#     获取所有commit
#     :return:
#     """
#     local_path = os.path.join('code', 'codetest')
#     repo = Repo(local_path)
# 
#     # 格式化输出
#     commit_log = repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}', max_count=50,
#                               date='format:%Y-%m-%d %H:%M')
#     log_list = commit_log.split("\n")
#     real_log_list = [json.loads(item) for item in log_list]
#     for commitlog in real_log_list:
#         print(commitlog)

# def checkout():
#     """
#     切换分支和回滚
#     :return:
#     """
#     local_path = os.path.join('code', 'codetest')
#     repo = Repo(local_path)
#     before = repo.git.branch()  # 查看分支
#     print(before)
#     # repo.git.reset('--hard', '854ead2e82dc73b634cbd5afcf1414f5b30e94a8')  # 回滚

# # clone()
# pull()
''''''

# # 创建本地路径用来存放远程仓库下载的代码
# git_url = 'http://101013483@10.102.4.219:58443/r/Test/StressDemo.git'
# a = git_url.split('/')[-1].split('.')[0]
# print(a)
# download_path = os.path.join('./code/' + a)
# # 拉取代码
# Repo.clone_from(git_url, to_path=download_path, branch='master')


class temp:
    def __init__(self):
        self.ftp = FTP('10.102.4.219', 'ceshi', 'ceshi123')
        self.ftp_root_path = '/mnt/work/FTP'
        self.repo = git.Repo.init('.')
        self.git_url = 'http://101013483@10.102.4.219:58443/r/Test/StressDemo.git'
        
    # http://101013483@10.102.4.219:58443/r/Test/StressDemo.git    
    # http://10.102.4.219:58443/zip/?r=Test/StressDemo.git&h=c77fbfba444132f809f4f27695d6effeaf1f84a6&format=zip
    def addr_translator(self, git_url, h_code):
        temp_addr = git_url.replace('/r/', '/zip/?r=') + '&h=' + h_code + '&format=zip'
        # 如果传入的git地址存在用户名，将用户名替换掉，如果不存在，则temp_addr即为最终下载地址
        if '@' in temp_addr:
            final_addr = 'http://' + temp_addr.split('@')[1]
        else:
            final_addr = temp_addr
        return final_addr


    def download_git_file(self, git_url, branch):
        zip_addr = git_url.replace('.git', '/archive/' + branch + '.zip')
        file = urllib.request.urlopen(zip_addr)
        return file

    def get_tag_and_hash(self, git_url):
        repo = git.Repo(git_url)
        remote_branches = []
        for ref in repo.git.branch('-r').split('\n'):
            print(ref)
            remote_branches.append(ref)

        pass

    def trans_to_ftp(self, git_url, branch, des_path):
        handle_file = self.download_git_file(git_url, branch)
        self.ftp.cwd('/' + des_path)
        pass

class temp:
    def __init__(self):
        self.ftp = FTP('10.102.4.219', 'ceshi', 'ceshi123')
        self.ftp_root_path = '/mnt/work/FTP'
        self.repo = git.Repo.init('.')
        self.git_url = 'http://101013483@10.102.4.219:58443/r/Test/StressDemo.git'
        
    # http://101013483@10.102.4.219:58443/r/Test/StressDemo.git    
    # http://10.102.4.219:58443/zip/?r=Test/StressDemo.git&h=c77fbfba444132f809f4f27695d6effeaf1f84a6&format=zip
    def addr_translator(self, git_url, h_code):
        temp_addr = git_url.replace('/r/', '/zip/?r=') + '&h=' + h_code + '&format=zip'
        # 如果传入的git地址存在用户名，将用户名替换掉，如果不存在，则temp_addr即为最终下载地址
        if '@' in temp_addr:
            final_addr = 'http://' + temp_addr.split('@')[1]
        else:
            final_addr = temp_addr
        return final_addr


    def download_git_file(self, git_url, branch):
        zip_addr = git_url.replace('.git', '/archive/' + branch + '.zip')
        file = urllib.request.urlopen(zip_addr)
        return file

    def get_tag_and_hash(self, git_url):
        repo = git.Repo(git_url)
        remote_branches = []
        for ref in repo.git.branch('-r').split('\n'):
            print(ref)
            remote_branches.append(ref)

        pass

    def trans_to_ftp(self, git_url, branch, des_path):
        handle_file = self.download_git_file(git_url, branch)
        self.ftp.cwd('/' + des_path)
        pass


if __name__ == '__main__':
    # repo = git.Git('git ls-remote http://10.102.4.219:3000/Macallan/15A.git')
    # print(repo)
    te = temp()
    # te.get_tag_and_hash('http://101013483@10.102.4.219:58443/r/Test/StressDemo.git')
    te.get_tags('http://101013483@10.102.4.219:58443/r/Test/StressDemo.git')
