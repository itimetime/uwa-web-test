from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from cf.config import img_path
from cf.config import test_data_path
import shutil
import allure
import log
from time import sleep
import os
from selenium.webdriver.common.by import By



class BASE(object):

    def __init__(self, selenium_driver, base_url, page_title):
        self.driver = selenium_driver
        self.url = base_url
        self.title = page_title
        self.mylog = log.log()

    def _open(self, url, page_title):
        try:
            self.driver.get(url)
            self.driver.maximize_window()
            assert page_title in self.driver.title, '打开页面失败:%s' % url
        except:
            self.mylog.error('未能正确打开页面：%s' % url)

    def find_element(self, *loc):
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_any_elements_located(loc))
            return self.driver.find_element(*loc)
        except:
            self.mylog.error('找不到元素：%s' % str(*loc))

    def find_elements(self, *loc):
        try:
            WebDriverWait(self.driver, 30).until(EC.visibility_of_any_elements_located(loc))
            return self.driver.find_elements(*loc)
        except:
            self.mylog.error('找不到元素组：%s' % str(*loc))

    def send_keys(self, value, clear=True, *loc):
        try:
            if clear:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(value)
        except AttributeError:
            self.mylog.error('输入失败，loc = ' + str(loc) + 'value' + value)

    def img_screenshot(self, img_name):
        try:
            _imgname = img_path + img_name + '.png'

            self.driver.get_screenshot_as_file(_imgname)

            _file = open(_imgname, 'rb').read()

            allure.attach(_file, '异常截图', allure.attachment_type.PNG)

        except:

            self.mylog.error('截图失败：%s' % img_name)


class EVENTS(BASE):

    def clear(self):
        DIR = test_data_path
        os.chdir(DIR)
        try:
            shutil.rmtree('allure-results')
                # shutil.rmtree(test_data_path)
            os.makedirs('allure-results')
        except FileNotFoundError as e:
            print(f'r目录不存在，信息如下：\n{e}')


    def get_browser_log(self):
        lists = self.driver.get_log('browser')
        list_value = []
        if lists.__len__() != 0:
            for dicts in lists:
                for key, value in dicts.items():
                    print(key + ": " + str(value))
                    self.mylog.info(str(value))
                    return key + ": " +str(value)
                    # list_value.append(value)
        #allure.attach(lists)
        # if 'SEVERE' in list_value:  # 报红
        #     return "SEVERE"
        # elif 'WARNING' in list_value:  # 报黄
        #     return "WARNING"
        # return True
    def open(self):
        self._open(self.url, self.title)

    def get(self,url):
        self.driver.get(url)

    def set_window_size(self,size):
        w,h=size.split(',')
        self.driver.set_window_size(w,h)

    def js_execute(self,js):
        self.driver.execute_script(js)

    def js_element_execute(self,jsandelement):
        js,element=jsandelement.split('|')
        element=self.driver.find_element(*eval(element))
        self.driver.execute_script("%s"%js,element)

    def click(self, element):
        self.find_element(*eval(element)).click()
        sleep(2)

#下拉框处理。传入下拉框元素（element1）和下拉框中选项元素（element2）
#大部分时间管用 （许多下拉框部分没写select）
    def perform_click(self,element1and2):
        element1,element2=element1and2.split('|')
        element1=self.find_element(*eval(element1))
        ActionChains(self.driver).move_to_element(element1).perform()
        self.find_element(*eval(element2)).click()

    def double_click(self, element):
        self.find_element(*eval(element)).double_click()

    def content_click(self,element):
        self.find_element(*eval(element)).context_click()

    def drag_to(self,sourceandtarget):
        source, target = sourceandtarget.split('|')
        s=self.find_element(*eval(source))
        t=self.find_element(*eval(target))
        ActionChains(self.driver).drag_and_drop(s,t)

#移动滚动条（绝对坐标）
    def move(self, para_xy):
        js = "window.scrollTo %s" % para_xy
        self.driver.execute_script(js)

# 滚轮移动 direction向下为-1，向上为1
    #win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, direction)
#键盘上下键控制页面上下
    def page_down(self,i):
        sleep(2)
        if i <1:
            print('输入值错误')
        while i > 0:
            i=i-1
            ActionChains(self.driver).send_keys(Keys.PAGE_DOWN).perform()
            sleep(1)

    def page_up(self,i):
        sleep(2)
        if i <1:
            print('输入值错误')
        while i > 0:
            i=i-1
            ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()
            sleep(1)

#输入元素
    def input_keywords(self, elementandkeywords):
        element, keywords = elementandkeywords.split('|')
        self.find_element(*eval(element)).clear()
        self.find_element(*eval(element)).send_keys(keywords)

#警告框处理
    def alert_reply(self,option):
        if option==1:
            self.driver.switch_to.alert.accept()
        elif option==0:
            self.driver.switch_to.alert.dismiss()

#跳转到其他标签页 i从0开始

    def handle_switch(self,i):
        handles_all = self.driver.window_handles
        self.driver.switch_to.window(handles_all[i-1])

#关闭所有窗口只保留第一个

    def window_only(self):
        handles_all=self.driver.window_handles
        num=len(handles_all)
        while num>1:
            self.driver.close()
            num=num-1
        self.driver.switch_to.window(handles_all[0])

#assert相关方法
#查看元素是否展示
    def is_displayed(self,element):
        sleep(1)
        return self.find_element(*eval(element)).is_displayed()

# 传入元素 传出需要的属性，元素与所需要的属性以|分隔
    def get_attr(self, elementandattribute):
        sleep(1)
        element, attribute = elementandattribute.split('|')
        x=self.find_element(*eval(element)).get_attribute(attribute)
        return x

    def get_text(self,element):
        sleep(1)
        return self.find_element(*eval(element)).text

    def get_url(self):
        sleep(1)
        return self.driver.current_url

    def get_title(self):
        try:
            sleep(1)
            return self.driver.title
        except:
            self.mylog.error('找不到当前页面title')

#返回目标元素的size 。。目前没想到哪里验证会用到
    def get_size(self,element):
        return self.find_element(*eval(element)).size
