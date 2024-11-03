import sys
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.env import Environment


class WebInteraction:

    def __init__(self):
        env = Environment()
        self.driver = env.driver
        self.config = env.config
        self.logger = env.logger

    def send_sms_code(self, phone):
        self.set_values(self.config.xpath_phone_input, phone)
        self.click(self.config.xpath_sms_code_sender)

    def phone_login(self, sms_code):
        # set sms code
        self.set_values(self.config.xpath_sms_code_input, sms_code)
        # 登录
        self.click(self.config.xpath_login_button)

    def open(self, url, timeout=8):
        self.driver.get(url)
        time.sleep(timeout)

    def quit(self):
        self.driver.quit()
        sys.exit(0)

    def start_publishing(self):
        self.click(self.config.xpath_start_publishing)
        self.switch_to_publishing_picture()

    def switch_to_publishing_picture(self):
        self.click(self.config.xpath_tab_pics, self.config.sleep_short_time)

    def publish_video(self, video_local_path):
        self.set_values(self.config.xpath_video_input, video_local_path)
        time.sleep(self.config.sleep_long_time)
        self.click(self.config.xpath_video_publish_button)

    def publish_pictures(self, code, pics):
        self.switch_to_publishing_picture()
        full_path_pics = []
        for p in pics:
            file_name = f'{self.config.opus_dir}/{code}/{p}'
            self.logger.debug(file_name)
            full_path_pics.append(file_name)

        self.set_values(self.config.xpath_upload_video_button, "\n".join(full_path_pics))
        time.sleep(self.config.sleep_short_time)

        title = datetime.now().strftime("%Y-%m-%d")
        self.set_values(self.config.xpath_pic_title_input, title)

        content = "#vocabulary #gre  #tofel #ielts #synonym"
        self.set_values(self.config.xpath_pic_content_input, content)

        self.click(self.config.xpath_pic_publish_button)
        time.sleep(self.config.sleep_long_time)

    # default timeout time is 3s
    def click(self, xpath, timeout=3, poll_frequency=0.5):
        try:
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda x: x.find_element(By.XPATH, xpath)).click()
        except Exception as e:
            self.logger.error(e)

    # default timeout time is 3s
    def set_values(self, xpath, values, timeout=3, poll_frequency=0.5):
        try:
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda x: x.find_element(By.XPATH, xpath)).send_keys(values)
        except Exception as e:
            self.logger.error(e)

    # get text by css selector
    def get_text_by_css(self, css_selector, timeout=3, poll_frequency=0.5):
        try:
            return WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda x: x.find_element(By.CSS_SELECTOR, css_selector)).text
        except Exception as e:
            self.logger.error(e)
        return None
