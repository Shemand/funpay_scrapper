from database import DatabaseRepository
from eve_currency import crawl
from eve_service import EveService
from models import Offer, User


def test_insert_offer():
    db = DatabaseRepository()
    service = EveService(db)
    user1 = service.get_user('Shemand')
    user2 = service.get_user('Danil')
    user3 = service.get_user('KUKUMBER')
    offers = [
        Offer(id='4123341-4-2-4',
              price=30.5,
              quantity=100.42,
              user=user1,
              server='Tranquility'),

        Offer(id='412323424-4-2-4',
              price=40.5,
              quantity=990.42,
              user=user2,
              server='Tranquility'),
        Offer(id='411-4-2-4',
              price=52.58,
              quantity=1234.42,
              user=user3,
              server='Tranquility'),
    ]
    service.update_offer(offers[0])
    service.update_offer(offers[1])
    service.update_offer(offers[2])
    service.update_offer(
        Offer(id='4123341-4-2-4',
              price=30.5,
              quantity=10.42,
              user=user1,
              server='Tranquility')
    )

def test_currency():
    return crawl()


def test_transformation():
    db = DatabaseRepository()
    service = EveService(db)
    data = crawl()
    # service.__transforamtion_to_models(data)

# test_insert_offer()
# x = test_currency()
test_transformation()