"""
Database class
"""
from sqlalchemy import Column, Integer, String, TEXT, FLOAT, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import NullPool

Base = declarative_base()


class Journey(Base):
   __tablename__ = "journeys_tonicek"
   id = Column(Integer, primary_key=True)
   source = Column(TEXT)
   destination = Column(TEXT)
   departure_datetime = Column(TIMESTAMP)
   arrival_datetime = Column(TIMESTAMP)
   carrier = Column(TEXT)
   vehicle_type = Column(TEXT)
   price = Column(FLOAT)
   currency = Column(String(3))
   createdAt = Column(TIMESTAMP)


def initialize_database(url: str) -> Session:
    """
    Initialization of the database
    """
    engine = create_engine(
        url,
        echo=True,
        poolclass=NullPool
    )

    if not inspect(engine).has_table("journeys_tonicek"):
        Base.metadata.create_all(engine)
    
    return Session(engine)
