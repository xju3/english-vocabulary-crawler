# This is a sample Python script.
#
# this function is now working well for vocabulary_sailingo on instagram
# there are some unexpected risks using for other account
#
import time

from selenium.webdriver.common.by import By

from common.env import Environment
from db.opus_manager import OpusManager


class SaiLingoVoc:

    def __init__(self):
        self.opus_manager = OpusManager()
        self.env = Environment(app=0)
        self.driver = self.env.driver
        self.codes = []
        self.URL_AUTHOR_HOME = f'{self.env.config.insta_home_url}/{self.env.config.insta_vocabulary_url}'
        self.URL_POST_PREFIX = f'{self.URL_AUTHOR_HOME}/p/'
        # self.driver.minimize_window()

    def run(self):
        self._login(self.env.config.insta_user_name, self.env.config.insta_password)

    def _login(self, username, password):
        self.driver.get(self.env.config.insta_home_url)
        time.sleep(self.env.config.sleep_medium_time)
        input_user_name = self.driver.find_element(By.NAME, 'username')
        input_password = self.driver.find_element(By.NAME, 'password')
        input_user_name.send_keys(username)
        input_password.send_keys(password)
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(self.env.config.sleep_medium_time)
        self.env.logger.debug("login successful")
        self._show_vocabulary_page()

    def _show_vocabulary_page(self):
        self.driver.get(self.URL_AUTHOR_HOME)
        time.sleep(self.env.config.sleep_long_time)
        self._get_vocabulary_codes()
        self._scroll_to_bottom()

    def _get_vocabulary_codes(self, page_index = 0):
        all_links = self.driver.find_elements(By.XPATH, "//a[@role='link']")
        if all_links is None or len(all_links) == 0:
            self.env.logger.error("no links found")
            return

        page_codes = []

        for link in all_links:
            try:
                href = link.get_attribute("href")
                if not href.startswith(self.URL_POST_PREFIX):
                    continue
                code = href.replace(self.URL_POST_PREFIX, '')[:-1]
                # self.env.logger.debug(code)
                if code in self.codes:
                    continue
                self.codes.append(code)
                page_codes.append(code)
            except Exception as e:
                self.env.logger.error(e)
        self.env.logger.debug(f"total: {len(self.codes)}, page: {page_index}, curr: {len(page_codes)}/{len(all_links)}")
        if len(page_codes) > 0:
            self.opus_manager.add_opus(page_codes, page_index)

    def _scroll_to_bottom(self):
        page_index = 0
        self._get_vocabulary_codes(page_index)
        scrolldown = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        while True:
            try:
                page_index += 1
                time.sleep(self.env.config.sleep_medium_time)
                self._get_vocabulary_codes(page_index)
                last_count = scrolldown
                scrolldown = self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
                if last_count == scrolldown:
                    self.env.logger.debug(f"reach the end of page: {page_index}")
                    break
            except Exception as e:
                self.env.logger.error(e)
