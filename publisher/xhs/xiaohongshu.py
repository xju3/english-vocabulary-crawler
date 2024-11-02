import json
import os
import sys
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.config import get_project_dir
from common.env import Environment
from db.opus_manager import OpusManager, OpusStatus
from publisher.xhs.cmd import extract_single_frame, list_dir_files
from publisher.xhs.web import XhsWeb

env = Environment()


class XiaoHongShu(object):

    def __init__(self):
        self.login_status = False
        self.user_list = []
        self.cookie_dict = {}
        self.web = XhsWeb(env)
        self.curr_user = ''
        self.load_cookie_users()
        self.opus_manager = OpusManager()

    def load_cookie_users(self):
        cookie_file = f'{get_project_dir()}/{env.config.cookie_file_name}'
        if os.path.isfile(cookie_file):
            with open(env.config.cookie_file_name, "r+", encoding="utf-8") as f:
                content = f.read()
                if content:
                    self.cookie_dict.update(json.loads(content))
        else:
            env.logger.error("cookie file not exist")
            return

        for k, _ in self.cookie_dict.items():
            self.user_list.append(k)
        env.logger.debug("user count: " + str(len(self.user_list)))

    def login_by_cookie(self):

        if self.login_status:
            return True

        if len(self.cookie_dict) == 0:
            return False

        if len(self.cookie_dict) == 1:
            cookie = self.cookie_dict[env.config.xhs_phone]
            for cookie in json.loads(cookie):
                env.driver.add_cookie(cookie)
        else:
            return False

        try:
            WebDriverWait(env.driver, 10, 0.2).until(
                lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
        except TimeoutException:
            self.login_status = False
            env.logger.error("login failed")
            return False
        return True

    def login_by_phone(self):
        self.web.send_sms_code(env.config.xhs_phone)
        time.sleep(env.config.sleep_short_time)

        while True:
            code = input("please enter sms code here：")
            if len(code) == 6:
                sms_code_valid = True
                break

        if sms_code_valid:
            self.web.phone_login(code)
            time.sleep(env.config.sleep_short_time)
            return True
        else:
            env.logger.error("sms code not valid")
            sys.exit(0)

    def login(self):
        self.web.open(env.config.xhs_login_url)
        time.sleep(env.config.sleep_medium_time)
        self.login_status = self.login_by_cookie()
        if not self.login_status:
            self.login_status = self.login_by_phone()
        if self.login_status:
            self.login_successfully()

    def login_successfully(self):
        # 获取昵称
        self.curr_user = WebDriverWait(env.driver, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
        env.logger.debug(f"{self.curr_user}, login successfully!")
        cookies = json.dumps(env.driver.get_cookies())
        self.cookie_dict[self.curr_user] = cookies
        with open('cookies.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.cookie_dict))
        env.logger.debug('cookie saved to file')

    def publish(self):
        items = self.opus_manager.get_publish_items(3)
        if len(items) == 0:
            env.logger.error("no publish items")
            sys.exit(0)

        for item in items:
            self.web.open(env.config.xhs_publish_url)
            time.sleep(env.config.sleep_medium_time)
            pics = list_dir_files(f'{env.config.opus_dir}/{item.code}', 'jpg')
            if len(pics) == 0:
                env.logger.error("no pictures")
                continue
            self.web.publish_pictures(pics)


    def upload_video(self, file):
        self.web.open(env.config.xhs_publish_url)
        time.sleep(env.config.sleep_long_time)
        self.web.publish_video(file)

    def upload_pictures(self, pics):
        pass

    def run(self):
        items = self.opus_manager.get_download_videos(5)
        if len(items) == 0:
            sys.exit(0)
        self.extract_pictures(items)
        self.login()
        time.sleep(env.config.sleep_medium_time)
        self.publish()

    def extract_pictures(self, items):
        for item in items:
            path = f'{env.config.opus_dir}/{item.code}'
            files = list_dir_files(path, 'mp4')
            env.logger.debug(f"{item.code}: {len(files)}")
            err = False
            for file in files:
                file_name = f'{path}/{file}'
                try:
                    extract_single_frame(file_name, f'{path}/{file.replace('.mp4', '')}.jpg')
                except Exception as e:
                    err = True
                    env.logger.error(f"{file_name}: {e}")
            if err:
                self.opus_manager.set_opus_status(item.code, OpusStatus.err)
            else:
                self.opus_manager.set_opus_status(item.code, OpusStatus.extracted)
