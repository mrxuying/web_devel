from selenium import webdriver
import time
from PIL import Image
from ShowapiRequest import ShowapiRequest

def screenShot(driver):
    '''截图保存图片'''
    
    ##截图并保存图片（此处是将整个浏览器页面截图保存）
    driver.save_screenshot("D:\\github\\login_with_checkcode\\fullpic.jpg")
    ##获取验证码图片的左上角图标
    left_top = driver.find_element_by_css_selector("img.btn").location
    print(left_top)
    ##获取左上角坐标的两个坐标值
    left = left_top['x']
    top = left_top['y']

    ##获取验证码图片的宽和高
    pic_size = driver.find_element_by_css_selector("img.btn").size
    print(pic_size)
    ##获取验证码图片的右下角坐标
    down = top + pic_size["height"]
    right = left + pic_size["width"]
    print(left,top,right,down)
    ##打开整张截图
    img = Image.open("D:\\github\\login_with_checkcode\\fullpic.jpg")
    ##img = img.convert('RGB')
    ##切割验证码图片并保存
    ver_img = img.crop((left,top,right,down))
    ver_img.save("D:\\github\\login_with_checkcode\\ver_img.png")

def getVerifyCdoe():
    '''调用易源接口进行验证码的识别'''
    req = ShowapiRequest("http://route.showapi.com/184-4","75989","10186a47079e4b8085ddb9bf168d3f70")
    req.addBodyPara("typeId","25")
    req.addBodyPara("convert_to_jpg","0")
    # 告诉接口识别的验证码图片文件
    req.addFilePara("image","D:\\github\\login_with_checkcode\\ver_img.png")
    #访问接口
    result=req.post().json()
    #从json提炼出有效的数据
    text=result['showapi_res_body']['Result']
    print("验证码是",text)
    return  text

def login():
    ##打开浏览器
    driver = webdriver.Chrome()
    ##最大化浏览器
    driver.maximize_window()
    ##浏览器打开被测网站
    driver.get("http://172.26.165.168/#.default?rtnurl=http%3A//172.26.165.168/%23home")
    ##休眠5秒，等待浏览器加载页面完毕
    time.sleep(5)
    #输入用户名
    driver.find_element_by_id("user_name").send_keys("egtxx")
    ##输入密码
    driver.find_element_by_id("pwd").send_keys("1")
    ##调用截图方法
    screenShot(driver)
    ##调用识别验证码方法并获取验证码的值
    verify_code = getVerifyCdoe()
    ##输入验证码
    driver.find_element_by_xpath("//input[@form-model='checkcode-value']").send_keys(verify_code)
    ##driver.find_element_by_xpath("//button[@type='button']").click()
    time.sleep(5)
    ##关闭浏览器
    driver.quit()

if __name__ == "__main__":
    ##调用登录方法
    login()
