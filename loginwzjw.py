from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support import expected_conditions as EC
import muggle_ocr


class Login():
    
    def __init__(self, usern, passw, url):
        self.usern = usern
        self.passw = passw
        self.url = url  

    #获取验证码图片并识别
    def ocr_code(self, e):
        img_as_bytes = e.screenshot_as_png
        ocr = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
        tword = ocr.predict(img_as_bytes)
        return tword
    
    def main(self):
        options = Options()
        options.use_chromium = True
        options.headless
        #浏览器自动关闭关
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Edge(options = options)
        #隐式等待开(s)
        driver.implicitly_wait(10)
        driver.get(url)

        while True:    
            #输入用户名和密码
            driver.find_element(By.ID, 'username').send_keys(usern)
            driver.find_element(By.ID, 'password').send_keys(passw)

            #获取与填写验证码
            driver.get_screenshot_as_file(u'imgs/screenshot.png')
            elem = driver.find_element(By.ID, 'captchaAccount')

            tw = self.ocr_code(elem)

            driver.find_element(By.ID, 'captcha').send_keys(tw + Keys.ENTER)
            
            #判定是否登录成功
            if(driver.current_url == "http://my.sdwz.cn/uc/user/index"):
                break


        #获取当前句柄
        now_handle = driver.current_window_handle
        driver.switch_to.window(now_handle)

        #句柄切换至新页面
        driver.find_element(By.LINK_TEXT, "每日健康上报").click()
        handles = driver.window_handles
        for handle in handles:
            if handle != now_handle:
                driver.switch_to.window(handle)
                break
                
        #点击单选框
        driver.find_element(By.XPATH, "//*[@id=\"SFHSCY2_ct\"]/label[1]/nobr/input").click()
        driver.find_element(By.XPATH, "//*[@id=\"SKMYS2_ct\"]/label[1]/nobr/input").click()      
        driver.find_element(By.XPATH, "//*[@id=\"GTJZQK2_ct\"]/label[1]/nobr/input").click()

        driver.find_element(By.ID, "ext-gen25").click()
        driver.find_element(By.ID, "ext-gen27").click()

        driver.quit()


if __name__ == "__main__":

    #需要填写的信息
    usern = ''
    passw = ''
    url = 'http://sso.sdwz.cn/cas/login?service=http%3A%2F%2Fmy.sdwz.cn%2Flogin'

    run = Login(usern, passw, url)

    run.main()

