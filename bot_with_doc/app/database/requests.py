from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.models import (Base, User)


engine = create_engine('sqlite:///bot.db')

session = sessionmaker(bind=engine)
s = session()

async def initialization(id):
    user = s.query(User).filter(User.user_tg_id == id).one_or_none()
    if user == None:
        return False
    else:
        return True
    
async def add_user(tg_id, user_name, user_last_name, user_email, user_token):
    user = User(user_tg_id=tg_id, user_name=user_name, user_last_name=user_last_name,
                user_email=user_email, user_token=user_token)
    s.add(user)
    s.commit()

async def get_user_token(user_id):
    token = []
    for i in s.query(User.user_token).filter(User.user_tg_id == user_id):
        token.append(str(i[0]))
    str_token = ''.join(token)
    s.commit()
    return(str_token)
    