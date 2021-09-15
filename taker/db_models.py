from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

BasicModel = declarative_base()


class UsersTable(BasicModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True, default=datetime.now())

    def __repr__(self):
        return f'<users table ({self.name})>'

class OffersTable(BasicModel):
    __tablename__ = 'eve_offers'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    inner_id = Column(String(64), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False, default=0)
    server = Column(String(64))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'<offers table ({self.name})>'
