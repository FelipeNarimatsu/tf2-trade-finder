from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship
import os

# definindo a URL para conexão no banco
# url = URL.create(
#     drivername='postgresql+psycopg2',
#     username='postgres',
#     password='banco',
#     host=os.getenv('PS_DATABASE_URL'),
#     database='postgres',
#     port=5432
# )

url = URL.create(
    drivername='mysql+pymysql',
    username=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
    database=os.getenv('MYSQL_DATABASE'),
    port=3306
)

engine  = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Trades(Base):
    __tablename__ = 'trades'
    trade_id         = Column(Integer, primary_key=True)
    item_name   = Column(String)
    sell_price  = Column(Float)
    buy_price   = Column(Float)
    profit      = Column(Float)

Base.metadata.create_all(engine)