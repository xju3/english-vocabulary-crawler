from sqlalchemy import select, update

from common.env import Environment
from db.data import Opus


class OpusManager:

    def __init__(self):
        self.env = Environment()

    def get_opus_by_code(self, code):
        stmt = select(Opus).where(Opus.code == code)
        return self.env.session.execute(stmt).first()

    def add_opus(self, code):
        item = self.get_opus_by_code(code)
        if item is not None:
            self.env.logger.debug('Opus already exists')
            return
        opus = Opus(code=code)
        self.env.session.add(opus)
        self.env.session.commit()
        self.env.logger.debug("Added opus:")

    def get_publish_items(self):
        stmp = select(Opus).where(Opus.downloaded != 1)
        return self.env.session.execute(stmp).fetchmany(2)

    def set_opus_downloaded(self, code):
        item = self.get_opus_by_code(code)
        if item is None:
            self.env.logger.error("No opus")
            return

        stmt = update(Opus.__tablename__).where(Opus.code == code).values(downloaded=1)
        self.env.session.execute(stmt)
