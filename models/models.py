from loguru import logger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, create_engine, Boolean, Time, ForeignKey

database = "sqlite:////Users/user/PycharmProjects/fastAPI-code/models/database.db"
engine = create_engine(database)


class Base(DeclarativeBase):
    pass


class UserDBModel(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: str = Column(Boolean, default=False, nullable=False)
    is_verified: str = Column(Boolean, default=False, nullable=False)
    country: str = Column(String, nullable=False)

    def __init__(self, id, name, email, hashed_password, is_active, is_superuser, is_verified, country):
        super().__init__()
        self.id = id
        self.name = name
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_verified = is_verified
        self.country = country


class UserAccount(Base):
    __tablename__ = "account"

    id: int = Column(Integer, primary_key=True, index=True)
    elo: int = Column(Integer, nullable=False)
    price: float = Column(String, nullable=False)
    hours: float = Column(String, nullable=False)
    date: str = Column(Time)
    account_type: str = Column(String, nullable=False)

    def __init__(self, account_id, elo, price, hours, date, account_type):
        super().__init__()
        self.account_id = account_id
        self.elo = elo
        self.price = price
        self.hours = hours
        self.date = date
        self.account_type = account_type


class AccountBuy(Base):
    __tablename__ = "account_sell"

    account_sell_id: int = Column(Integer, nullable=False, primary_key=True)
    account_id: int = Column(Integer, ForeignKey("account.id"))
    data: str = Column(String, nullable=False)

    def __init__(self, account_sell_id, account_id, data):
        super().__init__()
        self.account_sell_id = account_sell_id
        self.account_id = account_id
        self.data = data


Base.metadata.create_all(bind=engine)
