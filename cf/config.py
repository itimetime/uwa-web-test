# coding:utf-8
__author__ = 'GaoRong'

import datetime, time, os

project_path = os.path.dirname(os.path.dirname(__file__))  # 项目路径

driver_path = project_path + '\\drivers\\chromedriver'

test_case_path = project_path + '\\testcase\\'  # testcase路径

test_data_path = 'D:\\jenkins\\workspace\\AutoTest\\'

log_path = project_path + "\\log\\%s.log" % time.strftime('%Y%m%d%H%S', time.localtime())

img_path = project_path + '\\error_img\\' + time.strftime('%Y%m%d%H%S', time.localtime())

report_path = project_path + '\\report\\'

report_name = report_path + time.strftime('%Y%m%d%H%S', time.localtime())

smtp_sever = 'smtp.qq.com'

smtp_port = 25

email_name = ""  # 发件人

email_password = ""  # 发件人密码

email_To = ''  # 收件人邮箱
