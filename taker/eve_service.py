from datetime import datetime

from sqlalchemy import insert, select, desc, distinct, func, and_, join

from database import DatabaseRepository
from models import User, Offer


class EveService:
    def __init__(self, db: DatabaseRepository):
        self.db = db
        self.__offers = {}
        self.__update_offers()

    def get_user(self, name: str):
        query = select(DatabaseRepository.Users).where(DatabaseRepository.Users.name == name)
        row = self.db.engine.execute(query)
        row = row.fetchone()
        user = User(name=name)
        if not row:
            self._add_user(user)
        return user

    def update_offer(self, offer: Offer) -> bool:
        if offer.id in self.__offers and offer == self.__offers[offer.id]:
            return False
        self._add_offer(offer)
        return True

    def update_crawled_data(self, records: [dict]):
        models = self.__transforamtion_to_models(records)
        for model in models:
            try:
                self.update_offer(model)
            except Exception:
                print('some problem here')
                return False
        return True

    def __transforamtion_to_models(self, records: [dict]):
        offers = []
        for record in records:
            user = self.get_user(record['user']['name'])
            model = Offer(**record)
            offers.append(model)
        return offers

    def _add_user(self, user_model: User):
        query = insert(DatabaseRepository.Users).values(name=user_model.name)
        self.db.engine.execute(query)

    def _add_offer(self, offer_model: Offer):
        query = insert(DatabaseRepository.Offers).values(quantity=offer_model.quantity,
                                                         price=offer_model.price,
                                                         user_id=select(DatabaseRepository.Users.id) \
                                                         .where(
                                                             DatabaseRepository.Users.name == offer_model.user.name).limit(
                                                             1).scalar_subquery(),
                                                         inner_id=offer_model.id,
                                                         server=offer_model.server,
                                                         created=datetime.now())
        self.db.engine.execute(query)
        self.__offers[offer_model.id] = offer_model

    def __row_to_offer(self, row):
        return Offer(
            id=row['inner_id'],
            quantity=row['quantity'],
            price=row['price'],
            date=row['created'],
            server=row['server'],
            user=User(name=row['users_name'])
        )

    def __update_offers(self):
        subquery = select([func.max(DatabaseRepository.Offers.created).label('mxcreated'),
                           DatabaseRepository.Offers.inner_id]).group_by(DatabaseRepository.Offers.inner_id).subquery()
        query = select([
            DatabaseRepository.Offers.inner_id,
            DatabaseRepository.Offers.price,
            DatabaseRepository.Offers.quantity,
            DatabaseRepository.Offers.server,
            DatabaseRepository.Offers.created,
            DatabaseRepository.Users.name.label('users_name')
        ]) \
            .join(DatabaseRepository.Users, DatabaseRepository.Users.id == DatabaseRepository.Offers.user_id,
                  isouter=True)
        query = query.join(subquery, and_(DatabaseRepository.Offers.created == subquery.c.mxcreated,
                                          DatabaseRepository.Offers.inner_id == subquery.c.inner_id))
        rows = self.db.engine.execute(query).fetchall()
        self.__offers = {row['inner_id']: self.__row_to_offer(row) for row in rows}
