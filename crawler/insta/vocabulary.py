# This is a sample Python script.

import time

from selenium.webdriver.common.by import By

from common.env import Environment
from db.opus_manager import OpusManager

env = Environment()
URL_POST_PREFIX = env.config.insta_home_url + "/" + env.config.insta_vocabulary_url + "p/"
URL_AUTH_HOME = env.config.insta_home_url + "/" + env.config.insta_vocabulary_url


class Vocabulary:

    def __init__(self):
        self.opus_manager = OpusManager()
        self.driver = env.driver()
        self.driver.minimize_window()

    def run(self):
        self._login(env.config.insta_user_name, env.config.insta_password)

    def _login(self, username, password):
        self.driver.get(env.config.insta_home_url)
        time.sleep(env.config.sleep_medium_time)
        input_user_name = self.driver.find_element(By.NAME, 'username')
        input_password = self.driver.find_element(By.NAME, 'password')
        input_user_name.send_keys(username)
        input_password.send_keys(password)
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(env.config.sleep_medium_time)
        env.logger.debug("login successful")
        self._show_vocabulary_page()

    def _show_vocabulary_page(self):
        self.driver.get(URL_AUTH_HOME)
        time.sleep(env.config.sleep_long_time)
        self._get_vocabulary_codes()
        self._scroll_to_bottom()

    def _get_vocabulary_codes(self):
        time.sleep(env.config.sleep_short_time)
        all_links = self.driver.find_elements(By.XPATH, "//a[@role='link']")
        if all_links is None or len(all_links) == 0:
            env.logger.error("no links found")
            return
        for link in all_links:
            href = link.get_attribute("href")
            if href.startswith(URL_POST_PREFIX):
                code = href.replace(URL_POST_PREFIX, '')[:-1]
                env.logger.debug(code)
                self.opus_manager.add_opus(code)

    def _scroll_to_bottom(self):
        scrolldown = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        match = False
        while (match == False):
            time.sleep(env.config.sleep_long_time)
            self._get_vocabulary_codes()
            last_count = scrolldown
            scrolldown = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
            if last_count == scrolldown:
                match = True
