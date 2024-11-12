import sys
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def open(self, url, until_xpath = None):
        self.driver.get(url)

        if until_xpath is None:
            time.sleep(3)
        else:
            try:
                # Wait up to 10 seconds for the element to be located and visible
                 WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, until_xpath))  # Replace with actual element locator
                )
                # Now you can safely interact with the element
            except Exception as e:
                print("Element not found or other exception:", e)

    def quit(self):
        self.driver.quit()
        sys.exit(0)

    def start_publishing(self):
        self.click(self.config.xpath_start_publishing, self.config.sleep_medium_time)
        self.switch_to_publishing_picture()

    def switch_to_publishing_picture(self):
        self.click(self.config.xpath_tab_pics, self.config.sleep_medium_time)

    def publish_video(self, video_local_path):
        self.set_values(self.config.xpath_video_input, video_local_path)
        time.sleep(self.config.sleep_long_time)
        self.click(self.config.xpath_video_publish_button)

    def publish_pictures(self, item, pics):
        self.switch_to_publishing_picture()
        full_path_pics = []
        for p in pics:
            file_name = f'{self.config.opus_dir}/{item.code}/{p}'
            full_path_pics.append(file_name)


        self.set_values(self.config.xpath_upload_video_button, "\n".join(full_path_pics))

        words = item.words.split(",")
        title = datetime.now().strftime("%Y-%m-%d")
        prose = item.prose
        size = 0
        total = 0
        for word in words:
            total += 1
            prose = prose.replace(word, word.upper())
            if len(word) > size:
                title = word
                size = len(word)

        emoji = self.config.title
        self.set_values(self.config.xpath_pic_title_input, f'{item.id}.每日单词({total}):{emoji}{title.upper()}{emoji}')
        line1 = '#英语 #雅思 #高级英文 #词汇书 #专八 #专四 #托福'
        line2 = "🤝🤝🤝🤝🤝🤝🤝🤝🤝🤝🤝🤝"
        content = f"{line1} \n {line2}\n {prose}"
        self.set_values(self.config.xpath_pic_content_input, content)
        self.click(self.config.xpath_pic_publish_button)

    # default timeout time is 3s
    def click(self, xpath, timeout=5, poll_frequency=0.5):
        time.sleep(self.config.sleep_medium_time)
        try:
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda x: x.find_element(By.XPATH, xpath)).click()
        except Exception as e:
            self.logger.error(e)

    # default timeout time is 3s
    def set_values(self, xpath, values, timeout=5, poll_frequency=0.5):
        time.sleep(self.config.sleep_medium_time)
        try:
            WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda x: x.find_element(By.XPATH, xpath)).send_keys(values)
        except Exception as e:
            self.logger.error(e)

    # get text by css selector
    def get_text_by_css(self, css_selector, timeout=5, poll_frequency=0.5):
        try:
            return WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda x: x.find_element(By.CSS_SELECTOR, css_selector)).text
        except Exception as e:
            self.logger.error(e)
        return None
