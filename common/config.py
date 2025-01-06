import configparser
import os.path
import sys
import random
from pathlib import Path

from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv

def get_project_dir():
    current_dir = Path(__file__).resolve().parent
    while current_dir != current_dir.root:
        if (current_dir / ".git").exists():
            break
        current_dir = current_dir.parent
    else:
        raise FileNotFoundError("Project root not found")
    return current_dir


def yt_options(path):
    return {
        'outtmpl': f'{path}/%(video_autonumber)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }



class CrawlerConfig(object):
    _emojis = []
    def __init__(self):
        load_dotenv()
        config_file = f'{get_project_dir()}/common/config.ini'
        if not os.path.isfile(config_file):
            print(f'config file not found: {config_file}')
            sys.exit(0)

        cp = configparser.ConfigParser()
        cp.read(config_file)
        # instagram
        self._username = os.getenv('INSTAGAMM_USERNAME')
        self._password = os.getenv('INSTAGRAM_PASSWORD')
        self._home_url = cp.get('instagram', 'host')
        self._vocabulary_url = cp.get('instagram', 'author')
        # sleep
        self._short_sleep = cp.get('sleep', 'short')
        self._medium_sleep = cp.get('sleep', 'medium')
        self._long_sleep = cp.get('sleep', 'long')
        # files
        self._log_file = cp.get('file', 'log')
        self._cookie_file = cp.get('file', 'cookie')
        self._db_path = cp.get('file', 'db')
        self._opus_dir = cp.get('file', 'opus_dir')
        self._emoji_file = cp.get('file', 'emoji')
        self._xhs_phone = os.getenv('XHS_PHONE')
        self._xhs_login_url = cp.get('xhs', 'login_url')
        self._xhs_publish_url = cp.get('xhs', 'publish_url')
        #xpath
        self._xpath_phone_input = cp.get('xpath', 'phone_input')
        self._xpath_sms_code_sender = cp.get('xpath', 'sms_code_sender')
        self._xpath_sms_code_input = cp.get('xpath', 'sms_code_input')
        self._xpath_login_button = cp.get('xpath', 'login_button')
        self._xpath_start_publishing = cp.get('xpath', 'start_publishing')
        self._xpath_tab_pics = cp.get('xpath', 'tab_pics')
        self._xpath_tab_video = cp.get('xpath','tab_video')
        self._xpath_upload_video_button  = cp.get('xpath', 'upload_video_button')
        self._xpath_upload_pic_button = cp.get('xpath', 'upload_pic_button')
        self._xpath_video_publish_button = cp.get('xpath', 'video_publish_button')
        self._xpath_pic_publish_button = cp.get('xpath', 'pic_publish_button')
        self._xpath_pic_title_input = cp.get('xpath', 'pic_title_input')
        self._xpath_pic_content_input = cp.get('xpath', 'pic_content_input')

    @property
    def xpath_pic_title_input(self):
        return self._xpath_pic_title_input

    @property
    def xpath_pic_content_input(self):
        return self._xpath_pic_content_input

    @property
    def xpath_phone_input(self):
        return self._xpath_phone_input

    def insta_opus_url(self,code):
        return f'https://www.instagram.com/p/{code}/'

    @property
    def xpath_sms_code_sender(self):
        return self._xpath_sms_code_sender

    @property
    def xpath_sms_code_input(self):
        return self._xpath_sms_code_input

    @property
    def xpath_login_button(self):
        return self._xpath_login_button

    @property
    def xpath_start_publishing(self):
        return self._xpath_start_publishing

    @property
    def xpath_tab_pics(self):
        return self._xpath_tab_pics
    
    @property
    def xpath_tab_video(self):
        return self._xpath_tab_video

    @property
    def xpath_upload_video_button(self):
        return self._xpath_upload_video_button

    @property
    def xpath_upload_pic_button(self):
        return self._xpath_upload_pic_button

    @property
    def xpath_video_publish_button(self):
        return self._xpath_video_publish_button

    @property
    def xpath_pic_publish_button(self):
        return self._xpath_pic_publish_button


    @property
    def xhs_phone(self):
        return self._xhs_phone

    @property
    def xhs_login_url(self):
        return self._xhs_login_url

    @property
    def xhs_publish_url(self):
        return self._xhs_publish_url

    @property
    def insta_user_name(self):
        return self._username

    @property
    def insta_password(self):
        return self._password

    @property
    def insta_home_url(self):
        return self._home_url

    @property
    def insta_vocabulary_url(self):
        return self._vocabulary_url

    @property
    def sleep_short_time(self):
        return int(self._short_sleep)

    @property
    def sleep_medium_time(self):
        return int(self._medium_sleep)

    @property
    def sleep_long_time(self):
        return int(self._long_sleep)

    @property
    def log_file_name(self):
        return f'{get_project_dir()}/{self._log_file}'

    @property
    def title(self):
        if len(self._emojis)  == 0:
            file_path =  f'{get_project_dir()}/{self._emoji_file}'
            with open(file_path, 'r') as file:
                self._emojis = [line.strip() for line in file]
        return random.choice(self._emojis)

    @property
    def cookie_file_name(self):
        return f'{get_project_dir()}/{self._cookie_file}'

    @property
    def db_file_name(self):
        return f'sqlite:////{get_project_dir()}/{self._db_path}'

    @property
    def opus_dir(self):
        return f'{get_project_dir()}/{self._opus_dir}'

    @property
    def driver_options(self):
        options = Options()
        # 无界面模式
        options.add_argument('--headless')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument(f'user-agent=={UserAgent().random}')
        return options

