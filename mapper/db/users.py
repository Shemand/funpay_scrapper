from sqlalchemy import select

from db.DatabaseRepository import DatabaseRepository
from db.db_models import UsersTable as Users
from models import User


def get_user(db: DatabaseRepository, name: str):
    query = select(Users).where(Users.name == name)
    row = db.engine.execute(query)
    row = row.fetchone()
    if not row:
        return None
    user = User(name=name)
    return user


def get_users(db: DatabaseRepository):
    query = select(Users)
    row = db.engine.execute(query)
    rows = row.fetchall()
    users = []
    for row in rows:
        users.append(User(name=row['name']))
    return users


def get_user_by_offer_id(db, offer_id):
    query = select([db.Users.name]).where(db.Users.id == (select([db.Offers.user_id]).where(db.Offers.inner_id == offer_id).limit(1)))
    row = db.engine.execute(query).fetchone()
    return User(name=row['name'])
