import json
import os
import time

import yt_dlp
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.config import get_project_dir, yt_options
from common.env import Environment
from db.opus_manager import OpusManager
from publisher.xhs.cmd import merge_video_files
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
                env.DRIVER.add_cookie(cookie)
        else:
            return False

        try:
            WebDriverWait(env.DRIVER, 10, 0.2).until(
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
                sms_code_valid = False
                break

        if sms_code_valid:
            self.web.phone_login(code)
            time.sleep(env.config.sleep_short_time)
            return True
        else:
            env.logger.error("sms code not valid")
        return False

    def login(self):
        self.login_status = self.login_by_cookie()
        if not self.login_status:
            self.login_status = self.login_by_phone()
        if self.login_status:
            self.login_successfully()

    def login_successfully(self):
        # 获取昵称
        self.curr_user = WebDriverWait(env.DRIVER, 10, 0.2).until(
            lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
        env.logger(f"{self.curr_user}, login successfully!")
        cookies = json.dumps(env.DRIVER.get_cookies())
        self.cookie_dict[self.curr_user] = cookies
        with open('cookies.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.cookie_dict))
        env.logger.debug('cookie saved to file')

    def publish(self):
        works = self.download()
        for work in works:
            self.upload(work)

    def upload(self, file):
        self.web.open(env.config.xhs_publish_url)
        time.sleep(env.config.sleep_long_time)
        self.web.upload_video(file)

    def download(self):
        files = []
        success = 0
        opus_list = self.opus_manager.get_publish_items()
        for opus in opus_list:
            if success == 2:
                break
            code = opus.code
            path = f'download/{code}'
            try:
                self.dl_insta_video(code, path=path)
                success += 1
                files.append(f'{path}/{code}/1.mp4')
            except Exception as e:
                env.logger.error(e)
        return files

    def dl_insta_video(self, code, path):
        options = yt_options(f'{path}')
        with yt_dlp.YoutubeDL(options) as ydl:
            url = env.config.insta_opus_url(code)
            ydl.download([url])
            merge_video_files(path)
            # self.opus_manager.set_opus_downloaded(code)

    def run(self):
        # self.login()
        self.download()
