from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///bot.db')

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    user_tg_id = Column(Integer, nullable=False)
    user_name = Column(String)
    user_last_name = Column(String)
    user_email = Column(String)
    user_api_id = Column(String)
    user_token = Column(String)

start_db = Base.metadata.create_all(engine)