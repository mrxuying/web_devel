from selenium import webdriver
import time
import read
from selenium.webdriver.support.ui import WebDriverWait
from pymysql import cursors,connect
# import unittest

class Login(object):
    '''登录---------'''
    def login(self,user_name,pass_word,driver):
        result = read.read_urls()
        url = result[0][0].decode('utf-8')##获取测试环境url
        print(url)
        driver.maximize_window()
        driver.get(url)
        driver.implicitly_wait(12)
        driver.find_element_by_xpath("//*/input[@id='user_name']").send_keys(user_name)
        driver.find_element_by_xpath("//*/input[@id='pwd']").send_keys(pass_word)
        driver.find_element_by_css_selector('button.btn').click()


    def quit_driver(self,driver):
        driver.quit()

class AfterSale(object):
    '''售后服务管理'''
    def __init__(self,driver,link_text):
        self.driver = driver
        self.link_text = link_text

    def basedata(self,username,pwd):
        Login.login(self,username,pwd,self.driver) #登录
        #print('login success')
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(lambda the_driver: the_driver.find_element_by_link_text('服务管理').is_displayed())
        self.driver.find_element_by_xpath("//div/ul/li/a[text()='服务管理']").click()
        ##智能等待基础数据 链接在界面中展示出来
        WebDriverWait(self.driver, 10).until(lambda the_driver: the_driver.find_element_by_link_text('基础数据').is_displayed())
        menu = self.driver.find_element_by_link_text('基础数据')
        webdriver.ActionChains(self.driver).move_to_element(menu).perform()#将鼠标移到基础数据的链接上
        menu.click()
        menu = self.driver.find_element_by_link_text(self.link_text)
        webdriver.ActionChains(self.driver).move_to_element(menu).perform()
        self.driver.find_element_by_link_text(self.link_text).click()
        time.sleep(2)

class  DBMysql(object):
    """docstring for  DBMysql."""

    def __init__(self, *args, **kwargs):
        print (*args)
        self.db_info = args


    def mysql_conn(self):
        self.conn = connect(
                        host=self.db_info[0],
                        port=self.db_info[1],
                        user=self.db_info[2],
                        password=self.db_info[3],
                        db=self.db_info[4],
                        charset='utf8mb4',
                        cursorclass=cursors.DictCursor)










##driver = webdriver.Chrome()
##log = Login()
##log.login('xtadmin','1',driver)
##time.sleep(3)
##log.quit_driver()   ##for test
