# _*_coding:utf-8_*_
from Utils import Utils
from FTPTools import FTPTools

if __name__ == '__main__':
    tools = Utils()
    tools.init_dir()
    ftp_tool = FTPTools('10.102.4.219', 21, 'ceshi', 'ceshi123')
    ftp_tool.connect_ftp()
    # ftp_tool.mkdir_ftp('new_testDir/test/test')
    # ftp_tool.upload_file('/new_testDir', '.\\Log\\Log_20210203.log', 'Log_20210203')
    # ftp_tool.delete_file('.', 'Log_20210203.log')
    # ftp_tool.download_file('Macallan/15A/Log/HW/QW1900/SC_UL10V100R001C00B132/x001/CALJNJGQCYKNJRKJ', './code/',
    #                        '0121_1801.zip')
    des_path = tools.get_store_dir('DOU', 'HW', 'QW1900', 'SC_UL10V100R001C00B132')
    path = ftp_tool.trans_to_ftp('http://10.102.4.219:58443/r/Test/StressDemo.git', 'v1.0', des_path)
    ftp_tool.close_ftp()
    ftp_tool.connect_ftp()
    path = tools.make_dir_by_level('code')
    ftp_tool.download_file(des_path, path, 'v1.0.zip')
    ftp_tool.close_ftp()
