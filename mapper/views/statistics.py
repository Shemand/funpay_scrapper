from flask import render_template

from db.DatabaseRepository import DatabaseRepository
from db.offers import get_last_offers, get_offer_history
from db.users import get_user_by_offer_id


def current_offers_list():
    db = DatabaseRepository()
    offers = get_last_offers(db)
    return render_template('CurrentOffersList.html', offers=offers)

def history_offers_list(offer_id):
    db = DatabaseRepository()
    offers = get_offer_history(db, offer_id)
    username = get_user_by_offer_id(db, offer_id)
    return render_template('HistoryOfferList.html', username=username, offers=offers)