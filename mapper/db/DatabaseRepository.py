from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine, URL
from sqlalchemy.orm import Session

from db.db_models import BasicModel, OffersTable, UsersTable

config = {
  "ip": "localhost",
  "port": 5432,
  "database": "funpay_eve",
  "driver": "postgresql+psycopg2",
  "username": "shemand",
  "password": "qwerty"
}

class DatabaseRepository:
    __metadata: MetaData
    __engine: Engine
    __session: Session

    Offers = OffersTable
    Users = UsersTable
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseRepository, cls).__new__(cls)
            cls.instance.initialize(*args, **kwargs)
        return cls.instance

    def initialize(self) -> None:
        db_url = {
            'database': config['database'],
            'drivername': config['driver'],
            'username': config['username'],
            'password': config['password'],
            'host': config['ip']
        }
        self.__engine = create_engine(URL.create(**db_url), echo=False, encoding="utf8", pool_size=10)
        self.__metadata = BasicModel.metadata

    @property
    def engine(self) -> Engine:
        return self.__engine


    @property
    def metadata(self) -> MetaData:
        return self.__metadata
