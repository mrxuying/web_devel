import unittest
from HTMLTestRunner import HTMLTestRunner
import time
import os
##import smtplib
##from email.mime.text import MIMEText
##from email.mime.multipart import MIMEMultipart
##from email.header import Header
##
def new_file():
      lists = os.listdir(test_report_dir)
      lists.sort(key=lambda fn:os.path.getmtime(test_report_dir+'\\'+fn))
      file_path = os.path.join(test_report_dir,lists[-1])
      return file_path

if __name__ == '__main__':
    test_dir = 'E:\\EGT\\eGTAutoTest'
    discover = unittest.defaultTestLoader.discover(test_dir,pattern='test*.py')

    now = time.strftime('%Y-%m-%d %H_%M_%S')
    test_report_dir = 'E:\\EGT\\eGTAutoTest'
    filename = test_report_dir+'\\'+now+'result.html'
    fv = open(filename,'wb')
    runner = HTMLTestRunner(stream = fv,title = 'eGT基础数据测试报告',description = '用例执行情况')
    print('---1---')
    runner.run(discover)
    print('---2---')
    fv.close()
