from flask import Flask

from views.statistics import current_offers_list, history_offers_list


def initialize_flask_routes(app: Flask):
    app.add_url_rule('/', 'current_offers_list', current_offers_list)
    app.add_url_rule('/history/<offer_id>', 'history_offers_list', history_offers_list)