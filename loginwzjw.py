from selenium import webdriver
from time import sleep
from PIL import Image 
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import muggle_ocr

#处理验证码图片
def dimg(e):
    left = int(e.location['x'])
    top = int(e.location['y'])
    right = int(e.location['x'] + e.size['width'])
    bottom = int(e.location['y'] + e.size['height'])

    im = Image.open('imgs/screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save('imgs/screenshot.png')

#识别验证码图片
def vcode(image):
    sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

    with open(image, "rb") as f:
        captcha_bytes = f.read()
        
    tword = sdk.predict(image_bytes=captcha_bytes)
    return tword

usern=''#学号
passw=''#密码

#根据自己的浏览器下载相应的webdriver
driver = webdriver.Edge("G:/Python/msedgedriver.exe")#文件路径
driver.get("http://my.sdwz.cn/login")
sleep(1)


while True:    
    #输入用户名和密码
    driver.find_element_by_name('username').send_keys(usern)
    driver.find_element_by_name('password').send_keys(passw)

    #获取与填写验证码
    driver.get_screenshot_as_file(u'imgs/screenshot.png')
    element = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/form/div/div[2]/div[4]/img')
    dimg(element)
    image = r"./imgs/screenshot.png"
    sleep(1)

    tw = vcode(image)
    sleep(2)

    driver.find_element_by_id('code').send_keys(tw)
    sleep(1)

    driver.find_element_by_id('code').send_keys(Keys.ENTER)
    sleep(1)
    
    #判定是否登录成功
    if(driver.current_url == "http://my.sdwz.cn/uc/user/index"):
        break


#获取当前句柄
now_handle = driver.current_window_handle
driver.switch_to.window(now_handle)

driver.find_element_by_link_text("每日健康上报").click()
sleep(1)

handles = driver.window_handles

#句柄切换至新页面
for handle in handles:
    if handle!=now_handle:
        driver.switch_to.window(handle)

driver.find_element_by_id("ext-gen25").click()
sleep(1)

driver.find_element_by_id("ext-gen28").click()
sleep(1)

driver.quit()
