from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.database.models import (Base, User)


engine = create_engine('sqlite:///server.db')

session = sessionmaker(bind=engine)
s = session()

# adding a user to the server database
def add_user(name, last_name, phone, token):
    user = User(user_name=name, user_last_name=last_name, user_phone=phone, user_token=token)
    s.add(user)
    s.commit()

# checking the token
def check_token(token):
    token = s.query(User).filter(User.user_token == token).one_or_none()
    if token == None:
        s.commit()
        return False
    else:
        s.commit()
        return True
    