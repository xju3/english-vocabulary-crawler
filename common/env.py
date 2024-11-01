import logging
import sys

from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common.config import CrawlerConfig
from db.data import Base


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Environment:
    def __init__(self):
        self._config = CrawlerConfig()
        self._engine = create_engine(self._config.db_file_name, echo=True)
        Base.metadata.create_all(self.engine)
        self._session = Session(bind=self._engine)
        logging.basicConfig(filename=self._config.log_file_name, level=logging.INFO, format='%(message)s')
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        self._logger.info('init global env variables')
        self._driver = webdriver.Firefox(options=self._config.driver_options)

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        return self._session

    @property
    def logger(self):
        return self._logger

    @property
    def config(self):
        return self._config

    @property
    def driver(self):
        return self._driver

