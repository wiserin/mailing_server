from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///server.db')

Base = declarative_base()

# creating a database model of server users
class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_last_name = Column(String)
    user_email = Column(String)
    user_phone = Column(String)
    user_token = Column(String)

start_db = Base.metadata.create_all(engine)