import sys

from selenium.webdriver.common.by import By
import time


class XhsWeb:

    def __init__(self, env):
        self.driver = env.driver
        self.config = env.config

    def send_sms_code(self, phone):
        xpath_phone_input = "/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[1]/input"
        xpath_code_sender = "/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]"
        self.driver.find_element(By.XPATH, xpath_phone_input).send_keys(phone)
        # click for send sms code
        self.driver.find_element(By.XPATH, xpath_code_sender).click()

    def phone_login(self, sms_code):
        # set sms code
        xpath_code_input = "/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/input"
        self.driver.find_element(By.XPATH, xpath_code_input).send_keys(sms_code)
        # 登录
        xpath_login_button = "/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/button"
        self.driver.find_element(By.XPATH, xpath_login_button).click()

    def open(self, url):
        self.driver.get(url)

    def quit(self):
        self.driver.quit()
        sys.exit(0)

    def upload_video(self, video_local_path):
        xpath_upload_video_button = "/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div[2]/div[1]/div/input"

        button_upload = self.driver.find_element(By.XPATH, xpath_upload_video_button)
        button_upload.send_keys(video_local_path)
        time.sleep(self.config.sleep_long_time)
        xpath_publish_button = "/html/body/div[1]/div/div[2]/div/div[2]/main/div[3]/div/div/div[1]/div/div/div/div[2]/div[2]/div/button[1]"
        self.driver.find_element(By.XPATH, xpath_publish_button).click()
