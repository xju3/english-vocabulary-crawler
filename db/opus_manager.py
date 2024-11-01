from html.entities import html5

from sqlalchemy import select, update

from common.env import Environment
from db.data import Opus


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
        self.env.logger.info(f"page {page_index} has {hits} of {len(codes)} opus, exists: {exists}")
        if hits > 0:
            self.env.session.commit()

    def get_publish_items(self):
        stmp = select(Opus).where(Opus.downloaded != 1)
        return self.env.session.execute(stmp).fetchmany(2)

    def set_opus_downloaded(self, code):
        item = self.get_opus_by_code(code)
        if item is None:
            self.env.logger.error(f"opus does not exist: {code}")
            return

        stmt = update(Opus.__tablename__).where(Opus.code == code).values(downloaded=1)
        self.env.session.execute(stmt)
