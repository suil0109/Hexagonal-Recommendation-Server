from src.infrastructure.configuration.config import global_config

from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, create_engine, DateTime

Base = declarative_base()

class RecModel(Base):
    __tablename__ = 'recs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    image_url = Column(String(255))
    landing_url = Column(String(255))
    weight = Column(Integer)
    target_country = Column(String(20))
    target_gender = Column(String(1))
    point = Column(Integer)

class PointHistoryDB(Base):
    __tablename__ = 'point_history'

    user_id = Column(Integer, primary_key=True)  
    rec_id = Column(Integer)
    transaction = Column(String(20))
    point = Column(Integer)
    remaining_balance = Column(Integer)
    timestamp = Column(DateTime, primary_key=True)
    initialized = Column(String(255), primary_key=True)

class PointUserDB(Base):
    __tablename__ = 'point_user'

    id = Column(Integer, primary_key=True)
    balance = Column(Integer)
    timestamp = Column(DateTime)




username = global_config.MYSQL_USERNAME
password = global_config.MYSQL_PASSWORD
hostname = global_config.MYSQL_HOSTNAME
database_name = global_config.MYSQL_DATABASE

# MySQL DATABASE_URI
# Create MySQL Engine And Create a Session
DATABASE_URI = f'mysql+mysqlconnector://{username}:{password}@{hostname}/{database_name}'
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
