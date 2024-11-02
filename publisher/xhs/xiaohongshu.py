import json
import os
import sys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.env import Environment
from db.opus_manager import OpusManager, OpusStatus
from publisher.xhs.cmd import extract_single_frame, list_dir_files
from publisher.xhs.web import XhsWeb

env = Environment()


class XiaoHongShu(object):

    def __init__(self):
        self.has_cookie = False
        self.user_list = []
        self.cookie_dict = {}
        self.web = XhsWeb(env)
        self.curr_user = ''
        self.load_cookie_users()
        self.opus_manager = OpusManager()

    def load_cookie_users(self):
        cookie_file = f'{env.config.cookie_file_name}'
        if os.path.isfile(cookie_file):
            with open(env.config.cookie_file_name, "r+", encoding="utf-8") as f:
                content = f.read()
                if content:
                    self.cookie_dict.update(json.loads(content))
                    self.has_cookie = True
        else:
            env.logger.error("cookie file not exist")
            return

        for k, _ in self.cookie_dict.items():
            self.user_list.append(k)
        env.logger.debug("user count: " + str(len(self.user_list)))

    def login_by_cookie(self):
        cookie = self.cookie_dict[env.config.xhs_phone]
        for cookie in json.loads(cookie):
            env.driver.add_cookie(cookie)
            expiry = cookie['expiry']
            now = int(time.time())
            if now > expiry:
                self.login_by_phone()
                return
        try:
            WebDriverWait(env.driver, 10, 0.2).until(
                lambda x: x.find_element(By.CSS_SELECTOR, ".name-box")).text
        except Exception as e:
            env.logger.error(e)
        self.login_successfully()


    def login_by_phone(self):
        self.web.send_sms_code(env.config.xhs_phone)

        while True:
            code = input("please enter sms code here：")
            if len(code) == 6:
                sms_code_valid = True
                break

        if sms_code_valid:
            self.web.phone_login(code)
            self.login_successfully()
        else:
            env.logger.error("sms code not valid")
            sys.exit(0)

    def run(self):
        # open browser
        self.web.open(env.config.xhs_login_url)
        # if there are cookies at local, login by cookie*
        if self.has_cookie:
            self.login_by_cookie()
        else:
            self.login_by_phone()

    def login_successfully(self):
        # 获取昵称
        time.sleep(env.config.sleep_medium_time)
        cookies = json.dumps(env.driver.get_cookies())
        self.cookie_dict[env.config.xhs_phone] = cookies
        with open(env.config.cookie_file_name, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.cookie_dict))
        env.logger.debug('cookie saved to file')
        self.web.start_publishing()
        # self.publish()

    def publish(self):
        self.extract_pictures(self.opus_manager.get_download_videos(5))
        items = self.opus_manager.get_publish_items(3)
        env.logger.error(f"publishing items: {len(items)}")
        if len(items) == 0:
            sys.exit(0)

        for item in items:
            self.web.start_publishing()
            pics = list_dir_files(f'{env.config.opus_dir}/{item.code}', 'jpg')
            env.logger.error(f"code: {item.code}, pictures: {len(pics)}")
            if len(pics) == 0:
                continue
            self.web.publish_pictures(pics)


    def upload_video(self, file):
        self.web.open(env.config.xhs_publish_url)
        self.web.publish_video(file)


    def extract_pictures(self, items):
        for item in items:
            path = f'{env.config.opus_dir}/{item.code}'
            v_files = list_dir_files(path, 'mp4')
            p_files = list_dir_files(path, 'jpg')
            if len(p_files) > 0:
                env.logger.debug(f'{item.code} pictures has been extracted')
                continue
            err = False
            for file in v_files:
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
