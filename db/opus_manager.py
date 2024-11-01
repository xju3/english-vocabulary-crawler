from enum import Enum

from sqlalchemy import select, update

from common.env import Environment
from db.model import Opus


class OpusStatus(Enum):
    downloaded = 1
    err = 2
    published = 3


class OpusManager:

    def __init__(self):
        self.env = Environment()

    def get_opus_by_code(self, code):
        stmt = select(Opus).where(Opus.code == code)
        return self.env.session.execute(stmt).first()

    def add_opus(self, codes, page_index=0):
        hits = 0
        exists = 0
        for code in codes:
            item = self.get_opus_by_code(code)
            if item is not None:
                # self.env.logger.info(f'opus already exists: {code}')
                exists += 1
                continue
            hits += 1
            opus = Opus(code=code, downloaded=0, published=0, author_id=1, account_id=1, page_index=page_index)
            self.env.session.add(opus)
        if hits > 0:
            self.env.session.commit()

    def get_download_items(self, count):
        if count <= 0:
            return []
        return self.env.session.query(Opus).filter_by(downloaded=0).limit(count).all()

    def get_publish_items(self, count):
        if count <= 0:
            return []
        return self.env.session.query(Opus).filter_by(downloaded=1, err=0).limit(count).all()

    def set_opus_status(self, code, status):
        item = self.get_opus_by_code(code)
        if item is None:
            self.env.logger.error(f"opus does not exist: {code}")
            return
        stmt = update(Opus.__tablename__).where(Opus.code == code).values(downloaded=1)

        if status != OpusStatus.err:
            stmt = update(Opus.__tablename__).where(Opus.code == code).values(err=1)

        if status != OpusStatus.published:
            stmt = update(Opus.__tablename__).where(Opus.code == code).values(published=1)

        self.env.session.execute(stmt)
