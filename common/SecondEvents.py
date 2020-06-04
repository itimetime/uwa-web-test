from common.Events import EVENTS
from selenium.webdriver.support.select import Select
from time import sleep
import log
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver
from cf.config import img_path
from selenium.webdriver.common.by import By
import allure



class SecondEVENTS(EVENTS):

    #视频播放相关
    #传入参数video是video标签所在的XPATH

    def get_video_url(self, video):
        return self.driver.execute_script("return arguments[0].currentSrc;", self.driver.find_element(*eval(video)))

    def video_stop(self,video):
        v = self.find_element(*eval(video))
        self.driver.execute_script("arguments[0].pause()", v)

    def video_start(self,video):
        v=self.find_element(*eval(video))
        self.driver.execute_script("arguments[0].play()",v)

    # 同名属性有多个（例如历史版本页面）统计一共显示出了多少个版本
    def element_counts(self,element):
        sleep(1)
        whole=self.find_elements(*eval(element))
        count=0
        for a in whole:
            count=count+1
        return count

#表单选择未遇到过情况 但需要考虑
    def frame_switch(self,frame):
        f=self.find_element(*eval(frame))
        self.driver.switch_to.frame(f)
#可以获取id或name时
    def frame_straight_switch(self,frame):
        self.driver.switch_to.frame(*eval(frame))

    def add_cookie(self,nameandvalue):
        name, value = nameandvalue.split('|')
        self.driver.add_cookie({name:value})

    def delete_cookie(self,nameandoption):
        name, option = nameandoption.split('|')
        self.driver.delete_cookie(name,option)

#下拉框使用了select元素时
    def select_value(self,selandvalue):
        sel,value=selandvalue.split("|")
        sel=self.find_element(sel)
        Select(sel).select_by_value(value)

    def select_index(self,selandindex):
        sel,index = selandindex.split("|")
        sel=self.find_element(sel)
        Select(sel).select_by_index(index)

    def select_text(self,selandtext):
        sel,text=selandtext.split("|")
        sel = self.find_element(sel)
        Select(sel).select_by_visible_text(text)

    def upload(self,address):
        self.find_element(By.NAME,'file').send_keys(address)

    def upload_rt_script(self,address):
        self.find_element(By.XPATH,"//span[id='upload-script-file']//input[@id='file']").send_keys(address)

    def upload_rt_game(self,address):
        self.find_element(By.XPATH,"//span[@id='upload-game-file']//input[@id='file']").send_keys(address)
