
import logging
import sys

logger = logging.getLogger(__name__)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s',
                    datefmt='%H:%M:%S',
                    filename='app.log',
                    filemode='w')
logging.getLogger('sqlalchemy.engine.Engine').disabled = True
logging.getLogger('common').setLevel(logging.DEBUG)
logging.getLogger('crawler').setLevel(logging.DEBUG)
logging.getLogger('publisher').setLevel(logging.DEBUG)

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.debug('init global env variables')