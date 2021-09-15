from sqlalchemy import func, select, and_, desc

from db.db_models import OffersTable as Offers
from db.db_models import UsersTable as Users
from db.users import get_user
from models import Offer, User


def get_last_offers(db):
    subquery = select([func.max(Offers.created).label('mxcreated'),
                       Offers.inner_id]).group_by(Offers.inner_id).subquery()
    query = select([
        Offers.inner_id,
        Offers.price,
        Offers.quantity,
        Offers.server,
        Offers.created,
        Users.name.label('users_name')
    ]) \
        .join(Users, Users.id == Offers.user_id,
              isouter=True)
    query = query.join(subquery, and_(Offers.created == subquery.c.mxcreated,
                                      Offers.inner_id == subquery.c.inner_id))
    query = query.order_by(Offers.price)
    rows = db.engine.execute(query).fetchall()
    offers = {row['inner_id']: row_to_offer(row) for row in rows}
    return offers

def get_offer_history(db, offer_id):
    query = select([db.Offers, db.Users.name.label('users_name')])\
        .join(db.Users, db.Offers.user_id == db.Users.id, isouter=True)\
        .where( db.Offers.inner_id == offer_id).order_by(desc(db.Offers.created))
    rows = db.engine.execute(query).fetchall()
    offers = []
    for row in rows:
        offers.append(row_to_offer(row))
    return offers

def row_to_offer(row):
    return Offer(
        id=row['inner_id'],
        quantity=row['quantity'],
        price=row['price'],
        date=row['created'],
        server=row['server'],
        user=User(name=row['users_name'])
    )


def transforamtion_to_models(records: [dict]):
    offers = []
    for record in records:
        user = get_user(record['user']['name'])
        model = Offer(**record)
        offers.append(model)
    return offers

