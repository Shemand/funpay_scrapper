from datetime import datetime
from time import sleep

import requests

from database import DatabaseRepository
from eve_currency import crawl
from eve_service import EveService

if __name__ == '__main__':
    db = DatabaseRepository()
    service = EveService(db)
    data = crawl()
    while(True):
        data = crawl()
        if data is None:
            sleep(60)
            continue
        service.update_crawled_data(data)
        print('Data was updated' + str(datetime.now()))
        sleep(30)