import sys
import time
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class WebInteraction:

    def __init__(self, config, driver, logger):
        self.config = config
        self.driver = driver
        self.logger = logger

    def send_sms_code(self, phone):
        self.set_values(self.config.xpath_phone_input, phone)
        self.click(self.config.xpath_sms_code_sender)

    def phone_login(self, sms_code):
        # set sms code
        self.set_values(self.config.xpath_sms_code_input, sms_code)
        # 登录
        self.click(self.config.xpath_login_button)

    def open(self, url, until_xpath=None):
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
        self.switch_to_picture_tab()

    def switch_to_picture_tab(self):
        self.click(self.config.xpath_tab_pics, self.config.sleep_medium_time)

    def switch_to_video_tab(self):
        self.click(self.config.xpath_tab_video, self.config.sleep_medium_time)

    def publish_video(self, opus):
        self.switch_to_video_tab()
        file_name = f'{self.config.opus_dir}/{opus.id}.{opus.code}/{opus.id}.mp4'
        self.set_values(self.config.xpath_upload_video_button, file_name)
        self.set_title_comments(item=opus)
        self.click(self.config.xpath_video_publish_button)

    def upload_pics(self, item, pics):
        self.switch_to_picture_tab()
        full_path_pics = []
        for p in pics:
            file_name = f'{self.config.opus_dir}/{item.id}.{item.code}/{p}'
            full_path_pics.append(file_name)
        self.set_values(self.config.xpath_upload_video_button, "\n".join(full_path_pics))

    def set_title_comments(self, item):
        words = item.words.split(",")
        title = datetime.now().strftime("%Y-%m-%d")
        prose = item.prose
        size = 0
        total = 0
        subject = prose
        for word in words:
            total += 1
            subject = subject.replace(word, f'__({total})__')
            prose = prose.replace(word, f'({total}){word.upper()}')
            if len(word) > size:
                title = word
                size = len(word)

        line1 = '#英语 #雅思 #每日 #单词 #词汇书 #专八 #专四 #托福'
        emoji = self.config.title
        titleEmoji = self.config.title
        self.set_values(self.config.xpath_pic_title_input, f'{item.id}.{emoji}{title.upper()}{emoji}')
        if len(prose) > 200:
            line1 = '#填空 #英语 #雅思 #每日 #单词 #词汇书 #专八 #专四 #托福'
            content = f"{line1} \n {item.words} \n 题目:{titleEmoji * 8}\n {subject}"
        else:
            content = f"{line1} \n 短文:{titleEmoji * 8}\n {prose}"
        self.set_values(self.config.xpath_pic_content_input, content)

    def publish_pictures(self, item, pics):
        self.upload_pics(item, pics=pics)
        self.set_title_comments(item=item)
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
