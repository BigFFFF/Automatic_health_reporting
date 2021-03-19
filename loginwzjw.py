from selenium import webdriver
from time import sleep
from PIL import Image 
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import muggle_ocr


class Login():
    
    def __init__(self, usern, passw, url, webdri_path):
        self.usern = usern
        self.passw = passw
        self.url = url
        self.webdri_path = webdri_path

    #处理验证码图片
    def cut_code(self, e):
        left = int(e.location['x'])
        top = int(e.location['y'])
        right = int(e.location['x'] + e.size['width'])
        bottom = int(e.location['y'] + e.size['height'])

        im = Image.open('imgs/screenshot.png')
        im = im.crop((left, top, right, bottom))
        im.save('imgs/screenshot.png')

    #识别验证码图片
    def ocr_code(self, image):
        sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

        with open(image, "rb") as f:
            captcha_bytes = f.read()
            
        tword = sdk.predict(image_bytes=captcha_bytes)
        return tword
    
    def main(self):
        
        driver = webdriver.Edge(webdri_path)
        driver.get(url)
        sleep(1)

        while True:    
            #输入用户名和密码
            driver.find_element_by_name('username').send_keys(usern)
            driver.find_element_by_name('password').send_keys(passw)

            #获取与填写验证码
            driver.get_screenshot_as_file(u'imgs/screenshot.png')
            elem = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/form/div/div[2]/div[4]/img')
            self.cut_code(elem)
            
            image = r"./imgs/screenshot.png"
            tw = self.ocr_code(image)
            sleep(1)

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


if __name__ == "__main__":
    
    usern = ''  #学号
    passw = ''  #密码
    url = 'http://my.sdwz.cn/login'
    webdri_path = 'G:/Python/msedgedriver.exe'

    run = Login(usern,
                passw,
                url,
                webdri_path)

    run.main()

