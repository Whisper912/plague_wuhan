from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

# 创建对象的基类:
Base = declarative_base()

class Result(Base):
    __tablename__ = 'result'
    name = Column(VARCHAR(20), primary_key=True)
    total = Column(INTEGER)
    cure = Column(INTEGER)
    dead = Column(INTEGER)
    update_time = Column(DATETIME)

    def __init__(self, name, total=None, cure=None, dead=None, update_time=None):
        self.name = name
        self.total = total
        self.cure = cure
        self.dead = dead
        self.update_time = update_time

    def __str__(self):
        return "[Result] name: %s , total: %d , cure: %d , dead: %d" % (
            self.name,
            {True: self.total, False: 0}[self.total is not None],
            {True: self.cure, False: 0}[self.cure is not None],
            {True: self.dead, False: 0}[self.dead is not None])