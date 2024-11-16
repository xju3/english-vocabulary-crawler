from enum import Enum

from sqlalchemy import select, update

from common.env import Environment
from db.model import Opus


class OpusStatus(Enum):
    downloaded = 1
    no_resource = 2
    extracted = 3
    published = 4
    no_pics = 5
    no_contents = 6

class OpusManager:

    def __init__(self):
        self.env = Environment()

    def get_opus_by_code(self, code):
        stmt = select(Opus).where(Opus.code == code)
        return self.env.session.execute(stmt).first()

    def add_opus(self, codes, page_index=0):
        hits = 0
        for code in codes:
            item = self.get_opus_by_code(code)
            if item is not None:
                continue
            hits += 1
            opus = Opus(code=code, downloaded=0, published=0, extracted=0, err=0, author_id=1, account_id=1, page_index=page_index)
            self.env.session.add(opus)
        if hits > 0:
            self.env.session.commit()

    def get_items_for_downloading(self, count):
        if count <= 0:
            return []
        return self.env.session.query(Opus).filter_by(downloaded=0, err=0).limit(count).all()

    def get_items_for_publishing(self, count):
        if count <= 0:
            return []
        return self.env.session.query(Opus).filter_by(extracted = 1, published=0, err=0).limit(count).all()

    def update_extracted_info(self, code, words, prose):
        stmt = update(Opus).where(Opus.code == code).values(extracted=1, words=f"{','.join(words)}", prose=prose)
        self.env.session.execute(stmt)
        self.env.session.commit()

    def set_opus_status(self, code, status):
        stmt = update(Opus).where(Opus.code == code).values(downloaded=1)
        match status:
            case OpusStatus.no_resource:
                stmt = update(Opus).where(Opus.code == code).values(err=1)
            case OpusStatus.no_contents:
                stmt = update(Opus).where(Opus.code == code).values(err=2)
            case OpusStatus.no_pics:
                stmt = update(Opus).where(Opus.code == code).values(err=3)
            case OpusStatus.published:
                stmt = update(Opus).where(Opus.code == code).values(published=1)
            case OpusStatus.extracted:
                stmt = update(Opus).where(Opus.code == code).values(extracted=1)
        self.env.session.execute(stmt)
        self.env.session.commit()
