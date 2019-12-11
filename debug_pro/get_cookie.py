from selenium import webdriver
import requests
import time

driver = webdriver.Chrome()
driver.maximize_window()


url = 'http://172.26.165.168/'
driver.get(url)

time.sleep(15)

driver.find_element_by_xpath("//input[@id='user_name']").send_keys('egtxx')
driver.find_element_by_xpath("//input[@id='pwd']").send_keys('abc123!!')
driver.find_element_by_css_selector('button.btn').click()

time.sleep(5)
cookies = driver.get_cookies()
# cookie = driver.get_cookie()

print(cookies)
# print(cookie)
