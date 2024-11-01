import logging
import sys

from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common.config import CrawlerConfig
from db.model import Base


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Environment(metaclass=SingletonMeta):

    def __init__(self, *args, **kwargs):
        self._config = CrawlerConfig()
        self._engine = create_engine(self._config.db_file_name, echo=True)
        Base.metadata.create_all(self.engine)
        self._session = Session(bind=self._engine)

        ##loging
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(level=logging.WARN,
                            format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                            datefmt='%H:%M:%S',
                            filename=self._config.log_file_name,
                            filemode='w')
        logging.getLogger('sqlalchemy.engine.Engine').disabled = True
        logging.getLogger('common').setLevel(logging.DEBUG)
        logging.getLogger('crawler').setLevel(logging.DEBUG)
        logging.getLogger('publisher').setLevel(logging.DEBUG)

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        self._logger.debug('init global env variables')
        # print(logging.BASIC_FORMAT)
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

    def yt_options(self, path):
        return {
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }

