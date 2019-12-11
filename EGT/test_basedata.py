from selenium import webdriver
import time
from public import Login,AfterSale
import read
import unittest
import random
from selenium.webdriver.support.ui import WebDriverWait
from pymysql import cursors,connect
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options



rand_num = random.randint(1,10000)
query_res = 0

class TestBase(unittest.TestCase):
    '''基础数据维护'''
    def setUp(self):
        k = read.read_users()
        self.username = k[0][1].decode('utf-8')
        self.pwd = k[1][1].decode('utf-8')

        self.n += 1
        self.chrome_options = Options()
        self.chrome_options.add_argument('--no-sandbox')  ##解决DevToolsActivePort文件不存在的报错
        self.chrome_options.add_argument('--disable-dev-shm-usage')  ##u
        self.chrome_options.add_argument('--headless')       ##无图形界面启动
        ##chrome_options.add_argument('blink-settings=imagesEnabled=false')##不加载图片
        self.chrome_options.add_argument('--disable-gpu')    ##规避bug
        self.chrome_options.add_argument('lang=zh_CN.UTF-8') ##设置编码格式
        ##prefs = {"profile.managed_default_content_settings.images": 2} ##设置浏览器禁止加载图片
        ##self.chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.verificationErrors = []
        print(self.verificationErrors)
        print('case_%d的账号:%s 密码是:%s'%(self.n,self.username,self.pwd))
        self.n += 1

    def test_add_bad_place(self):
        '''故障部位维护'''
        init = AfterSale(self.driver,'故障部位维护')
        init.basedata(self.username,self.pwd)
        # init_handle = self.driver.current_window_handle
        ##点击新增
        self.driver.find_element_by_xpath("//a/label[text()='新增']").click()
        self.driver.implicitly_wait(2)
        ##输入故障部位代码
        bad_code = 'bad' + str(rand_num)
        print(bad_code)
        self.driver.find_element_by_xpath("//input[@data-bv-field='flcode']").send_keys(bad_code)
        self.driver.find_element_by_xpath("//input[@data-bv-field='flname']").send_keys(bad_code)
        ##启用状态为默认启用
        ##点击确定
        self.driver.find_element_by_xpath("//button[text()='保存']").click()
        ##查询查看返回结果断言新增是否成功，同时检验查询功能正确
        time.sleep(5)
        # handles = self.driver.window_handles
        # for i in handles:
        #     if i == init_handle:
        #         self.driver.switch_to_window(i)
        self.driver.find_element_by_xpath("//form/*//input[@name='flcode']").send_keys(bad_code)
        time.sleep(2)
        self.driver.find_element_by_xpath("//label[text()='查询']").click()
        time.sleep(3)
        FAULT_PART_CODE = self.driver.find_element_by_xpath("//td[@title='"+bad_code+"']").text
        self.assertEqual(FAULT_PART_CODE,bad_code)
        # try:
        #     data = self.driver.find_element_by_xpath("//td[text()='"+bad_code+"']").text
        #     self.assertEqual(data,bad_code)
        # except NoSuchElementError:
        #     print('test_add_bad_place failed')
        # except AssertionError as msg:
        #     self.verificationErrors.append(msg)
        #     raise msg

    def test_add_bad_reasoncode(self):
        '''故障现象原因码'''
        init = AfterSale(self.driver,'故障现象原因码')
        init.basedata(self.username,self.pwd)

        self.driver.find_element_by_xpath("//a/label[text()='添加']").click()
        self.driver.implicitly_wait(2)
        ##输入故障部位代码
        reason_code = 'reason' + str(rand_num)
        ##选择故障部位
        self.driver.find_element_by_xpath("//select[@data-bv-field='FAULT_PART_NAME']").click()
        self.driver.find_element_by_xpath("//select[@data-bv-field='FAULT_PART_NAME']/option[@value='BAD001']").click()
        self.driver.find_element_by_xpath("//div/input[@data-bv-field='CS_CT_CODE']").send_keys(reason_code)
        self.driver.find_element_by_xpath("//div/input[@data-bv-field='CS_CT_MARK']").send_keys(reason_code+'maark')
        ##启用状态为默认启用
        ##点击确定
        self.driver.find_element_by_xpath("//button[text()='保存']").click()
        ##查询查看返回结果断言新增是否成功，同时检验查询功能正确
        time.sleep(5)
        self.driver.find_element_by_xpath("//form/*//input[@name='CS_CT_CODE']").send_keys(reason_code)
        time.sleep(2)
        self.driver.find_element_by_xpath("//label[text()='查询']").click()
        time.sleep(3)

        data = self.driver.find_element_by_xpath("//td[text()='"+reason_code+"']").text
        self.assertEqual(data,reason_code)


    def test_other_cost(self):
        '''其他费用类别'''
        init = AfterSale(self.driver,'其他费用类别')
        init.basedata(self.username,self.pwd)

        self.driver.find_element_by_xpath("//a/label[text()='添加']").click()
        self.driver.implicitly_wait(2)
        ##输入
        other_code = 'other' + str(rand_num)
        ##选择故障部位
        self.driver.find_element_by_xpath("//input[@data-bv-field='COST_TYPE_CODE']").send_keys(other_code)
        self.driver.find_element_by_xpath("//input[@data-bv-field='COST_TYPE_NAME']").send_keys(other_code)
        self.driver.find_element_by_xpath("//input[@data-bv-field='OTHER_PRICE']").send_keys(300)
        ##启用状态为默认启用
        ##点击确定
        self.driver.find_element_by_xpath("//button[text()='保存']").click()
        ##查询查看返回结果断言新增是否成功，同时检验查询功能正确
        time.sleep(5)
        self.driver.find_element_by_xpath("//form/*//input[@name='COST_TYPE_CODE']").send_keys(other_code)
        time.sleep(2)
        self.driver.find_element_by_xpath("//label[text()='查询']").click()
        time.sleep(3)
        # try:
        #     data = self.driver.find_element_by_xpath("//td[text()='"+other_code+"']").text
        #     self.assertEqual(data,other_code)
        # except NoSuchElementException:
        #     print('test_add_bad_place failed')
        # except AssertionError as msg:
        #     self.verificationErrors.append(msg)
        #     raise msg
        data = self.driver.find_element_by_xpath("//td[text()='"+other_code+"']").text
        self.assertEqual(data,other_code)

    def test_repair_type(self):
        '''保修类别'''
        init = AfterSale(self.driver,'保修类别')
        init.basedata(self.username,self.pwd)

        self.driver.find_element_by_xpath("//a/label[text()='新增']").click()
        self.driver.implicitly_wait(2)
        ##输入
        repair_type_code = 'repair' + str(rand_num)
        ##选择故障部位
        self.driver.find_element_by_xpath("//input[@data-bv-field='typecode']").send_keys(repair_type_code)
        self.driver.find_element_by_xpath("//input[@data-bv-field='typename']").send_keys(repair_type_code)
        ##启用状态为默认启用
        ##点击确定
        self.driver.find_element_by_xpath("//button[text()='保存']").click()
        ##查询查看返回结果断言新增是否成功，同时检验查询功能正确
        time.sleep(5)
        self.driver.find_element_by_xpath("//form/*//input[@name='typecode']").send_keys(repair_type_code)
        time.sleep(2)
        self.driver.find_element_by_xpath("//label[text()='查询']").click()
        time.sleep(3)
        # try:
        #     data = self.driver.find_element_by_xpath("//td[text()='"+repair_type_code+"']").text
        #     self.assertEqual(data,repair_type_code)
        # except NoSuchElementException:
        #     print('test_add_bad_place failed')
        # except AssertionError as msg:
        #     self.verificationErrors.append(msg)
        #     raise msg
        data = self.driver.find_element_by_xpath("//td[text()='"+repair_type_code+"']").text
        self.assertEqual(data,repair_type_code)

    def test_add_operate_part(self):
        '''维修大类维护——添加'''
        init = AfterSale(self.driver,'维修大类维护')
        init.basedata(self.username,self.pwd)

        ##点击添加
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[@id='add']").click() #点击添加
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("(//input[@name='OPERATE_PART_CODE'])[2]").send_keys('PARTBI' + str(rand_num))
        self.driver.find_element_by_xpath("(//input[@name='OPERATE_PART_NAME'])").send_keys('PARTBI' + str(rand_num))
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//select[@name='FAULT_PART_CODE']").click()  #点击故障部位下拉框
        self.driver.find_element_by_xpath("//option[text()='传动杆']").click() #故障部位选择传动杆

        self.driver.find_element_by_xpath("//select[@data-bv-field='STATUS']").click()  #点击启用状态下拉框
        self.driver.find_element_by_xpath("//option[text()='启用']").click() #选择启用

        self.driver.find_element_by_xpath("//button[text()='保存']").click()  #确定
        time.sleep(3)
        # try:
        #    with self.conn.cursor() as cursor:
        #        sql="select oprate_place_name from t_se_db_oprate_place where OPERATE_PART_CODE like %s;"
        #        FAULT_PART_CODE = 'PARTBI' + str(rand_num)
        #        cursor.execute(sql,(FAULT_PART_CODE,))
        #        global query_res
        #        query_res = cursor.fetchone()
        #        print(query_res)
        # except Exception:
        #    pass
        # self.assertEqual(query_res['oprate_place_name'],'PARTBI' + str(rand_num))

    def test_add_wi_type(self):
        '''维修小类维护'''
        init = AfterSale(self.driver,'维修小类维护')
        init.basedata(self.username,self.pwd)

        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//a/label[text()='添加']").click() #点击添加
        time.sleep(2)
        #点击展开下拉框
        self.driver.find_element_by_xpath("//*[@id='formData']/div[1]/div/select").click()
        time.sleep(3)
        OPERATE_PART_CODE = 'PARTBI' + str(rand_num)
        #选择测试大类名称
        code_path = "//select[@data-bv-field='OPERATE_PART_CODE']/option[text()='PARTBI332']"

        ##智能等待维修大类编码下拉框显示出来
        WebDriverWait(self.driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath(code_path).is_displayed())
        element = self.driver.find_element_by_xpath(code_path)
        ##print(element)
        element.click()
        ##webdriver.ActionChains(self.driver).click_and_hold(element)#点击PARTBI5677

        self.driver.find_element_by_xpath("//input[@data-bv-field='RRPAIR_SMALL_KIND_CODE']").send_keys('RSKC' + str(rand_num))

        #输入测试小类名称
        self.driver.find_element_by_xpath("//input[@data-bv-field='RRPAIR_SMALL_KIND_NAME']").send_keys('测试维修小类' + str(rand_num))
        self.driver.find_element_by_xpath("//div[@class='col-xs-7']/select[@name='STATUS'][1]").click()      #点击启用状态下拉框
        self.driver.find_element_by_xpath("//div[@class='col-xs-7']/select[@name='STATUS'][1]/option[text()='启用']").click() #选择启用

        self.driver.find_element_by_xpath("//button[text()='保存']").click()  #确定
        time.sleep(3)
        # try:
        #     with self.conn.cursor() as cursor:
        #         sql="select rrpair_small_kind_name from t_se_db_wi_type where RRPAIR_SMALL_KIND_CODE like %s;"
        #         RRPAIR_SMALL_KIND_CODE = 'RSKC' + str(rand_num)
        #         cursor.execute(sql,(OPERATE_PART_CODE + RRPAIR_SMALL_KIND_CODE,))
        #         res = cursor.fetchone()
        #         print(res)
        # except Exception as err:
        #    raise err
        # self.assertEqual(res['rrpair_small_kind_name'],'测试维修小类' + str(rand_num))

    def test_add_wi_price(self):
        '''工时单价维护'''
        init = AfterSale(self.driver,'工时单价')
        init.basedata(self.username,self.pwd)

        ##添加工时单价
        self.driver.implicitly_wait(2)
        self.driver.find_element_by_xpath("//a/label[text()='添加']").click() #点击添加
        time.sleep(2)
        ##输入工时单价编码和工时单价名称
        self.driver.find_element_by_xpath("//input[@data-bv-field='WI_PRICE_CODE']").send_keys('WPC' + str(rand_num))
        self.driver.find_element_by_xpath("//input[@data-bv-field='WI_PRICE_NAME']").send_keys('工时单价' + str(rand_num))
        self.driver.find_element_by_xpath("//select[@data-bv-field='CAR_SERIES_CODE']").click()
        ##选择车系编码
        CAR_SERIES_PATH = "//select[@data-bv-field=\'CAR_SERIES_CODE\']/option[@value=\'EGTNEWPOWERECAR\']"
        WebDriverWait(self.driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath(CAR_SERIES_PATH).is_displayed())
        CAR_SERIES_CODE = self.driver.find_element_by_xpath(CAR_SERIES_PATH)
        CAR_SERIES_CODE.click()
        ##选择业务类别
        business_type_code = ['30701','30702','30703','30704','30705','30707','30713','30714']
        n = random.randint(0,7)
        self.driver.find_element_by_xpath("//select[@data-bv-field='BUSINESS_TYPE_CODE']").click()
        business_type = "//select[@data-bv-field=\'BUSINESS_TYPE_CODE\']/option[@value=\'"+ business_type_code[n] + "\']"
        WebDriverWait(self.driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath(business_type).is_displayed())
        repair_type = self.driver.find_element_by_xpath(business_type)
        repair_type.click()
        #输入单价
        wi_price = random.randint(50,80)
        self.driver.find_element_by_xpath("//input[@data-bv-field='WI_PRICE']").send_keys(wi_price)
        ##选择启用状态
        m = random.randint(0,1)
        self.driver.find_element_by_xpath("//select[@data-bv-field='STATUS']").click()
        status_code = "//select[@data-bv-field='STATUS']/option[@value=\'" + str(m) + "\']"
        WebDriverWait(self.driver, 10).until(lambda the_driver: the_driver.find_element_by_xpath(status_code).is_displayed())
        status = self.driver.find_element_by_xpath(status_code)
        status.click()
        self.driver.find_element_by_xpath("//button[text()='保存']").click()  #确定
        time.sleep(5)

        # try:
        #     with self.conn.cursor() as cursor:
        #         sql="select WI_PRICE_NAME from t_se_db_wi_price where WI_PRICE_CODE like %s;"
        #         WI_PRICE_CODE = 'WPC' + str(rand_num)
        #         cursor.execute(sql,(WI_PRICE_CODE,))
        #         global query_res
        #         query_res = cursor.fetchone()
        #         print(query_res)
        # except Exception:
        #    pass
        # self.assertEqual(query_res['WI_PRICE_NAME'],'工时单价' + str(rand_num))


    def test_add_wi_standard(self):
        '''维修工时标准'''
        init = AfterSale(self.driver,'维修工时标准')
        init.basedata(self.username,self.pwd)
        self.driver.implicitly_wait(3)
        ##点击新增
        self.driver.find_element_by_xpath("//a/label[text()='新增']").click()
        #print(type(self.driver.find_element_by_xpath("//a/label[text()='新增']")))
        self.driver.find_element_by_xpath("//div[@id='addfuc_dialog']//div/select[@id='repairclassl']").click()
        self.driver.implicitly_wait(3)
        ##选择维修大类
        operate_part = self.driver.find_element_by_xpath("//div[@id='addfuc_dialog']//div/select[@id='repairclassl']/option[text()='test001']")
        operate_part.click()

        ##选择维修小类
        self.driver.find_element_by_xpath("//div[@id='addfuc_dialog']//div/select[@id='repairclasss']").click()
        wi_type = self.driver.find_element_by_xpath("//div[@id='addfuc_dialog']//div/select[@id='repairclasss']/option[text()='售后sit003']")
        wi_type.click()
        ##输入工时编码
        wi_code = 'wi' + str(rand_num)
        self.driver.find_element_by_xpath("//input[@data-bv-field='wicode']").send_keys(wi_code)
        ##输入维修内容
        self.driver.find_element_by_xpath("//input[@data-bv-field='repairs']").send_keys('content'+str(rand_num))
        ##输入最大工时数
        self.driver.find_element_by_xpath("//input[@data-bv-field='maxtime']").send_keys(8)
        ##保存
        self.driver.find_element_by_xpath("//button[@name='addbutton']").click()
        ##状态选择/默认为启用
        time.sleep(2)
        ##断言
        self.driver.find_element_by_id("wicode").send_keys(wi_code)
        self.driver.find_element_by_link_text("查询").click()
        code = self.driver.find_element_by_xpath("//*/td[@title='"+wi_code+"']").text
        ##print(code)
        self.assertEqual(code,wi_code)



    def test_month_setting(self):
        '''结算月设定'''
        init = AfterSale(self.driver,'结算月设定')
        init.basedata(self.username,self.pwd)

        self.driver.find_element_by_xpath("//a/label[text()='新增']").click()
        self.driver.implicitly_wait(5)
        ##输入结算月名称
        self.driver.find_element_by_xpath("//input[@form-model='yearmonth']").send_keys('201908')
        ##jquery去掉日历控件只读属性，输入开始时间
        js = "$('input[id=startdate]').removeAttr('readonly')"
        self.driver.execute_script(js)
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@data-bv-field='startdate']").clear()
        self.driver.find_element_by_xpath("//input[@data-bv-field='startdate']").send_keys("2019-07-26")
        ##输入结束时间
        js = "$('input[id=enddate]').removeAttr('readonly')"
        self.driver.execute_script(js)
        time.sleep(2)
        self.driver.find_element_by_xpath("//input[@data-bv-field='enddate']").clear()
        self.driver.find_element_by_xpath("//input[@data-bv-field='enddate']").send_keys("2019-08-25")
        self.driver.find_element_by_xpath("//label[text()='备注：']").click()
        time.sleep(5)
        ##启用状态为默认启用
        ##点击确定
        self.driver.find_element_by_xpath("//button[text()='保存']").click()
        ##查询查看返回结果断言新增是否成功，同时检验查询功能正确
        time.sleep(3)
        self.driver.find_element_by_xpath("//*/div/input[@id='yearmonth']").send_keys("201908")
        time.sleep(2)
        self.driver.find_element_by_xpath("//label[text()='查询']").click()
        time.sleep(3)
        # try:
        #     data = self.driver.find_element_by_xpath("//td[text()='201902']").text
        #     self.assertEqual(data,'201902')
        # except NoSuchElementException:
        #     print('test_month_setting failed')
        # except AssertionError as msg:
        #     self.verificationErrors.append(msg)
        #     raise msg
        data = self.driver.find_element_by_xpath("//*/td[@title='201908']").text
        self.assertEqual(data,'201902')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
