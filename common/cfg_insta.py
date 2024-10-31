import configparser
from pathlib import Path

from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options


class CrawlerConfig(object):

    def __init__(self):
        cp = configparser.ConfigParser()
        cfg_file = Path.joinpath(Path.cwd(), "common/config.ini")
        print(cfg_file)
        cp.read(cfg_file)
        self._username = cp.get('insta.account', 'user_name')
        self._password = cp.get('insta.account', 'password')
        self._home_url = cp.get('insta.url', 'home')
        self._vocabulary_url = cp.get('insta.url', 'vocabulary')
        self._short_sleep = cp.get('sleep.time', 'short')
        self._medium_sleep = cp.get('sleep.time', 'medium')
        self._long_sleep = cp.get('sleep.time', 'long')
        self._log_file = cp.get('file', 'log')
        self._db_path = cp.get('file', 'db')

    @property
    def user_name(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def home_url(self):
        return self._home_url

    @property
    def vocabulary_url(self):
        return self._vocabulary_url

    @property
    def short_sleep_time(self):
        return int(self._short_sleep)

    @property
    def medium_sleep_time(self):
        return int(self._medium_sleep)

    @property
    def long_sleep_time(self):
        return int(self._long_sleep)

    @property
    def log_file_name(self):
        return Path.cwd().joinpath(self._log_file)

    @property
    def db_file_name(self):
        return f'sqlite:////{Path.cwd().joinpath(self._db_path)}'

    @property
    def driver_options(self):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument(f'user-agent=={UserAgent().random}')
        # 无界面模式
        # options.add_argument('--headless')
        return options
