import server.database.requests as db
from server.token_generator.generator import token_generator
from random import randint
from server.mailing import mailing

# generating a random number for the verification code
def random_number():
    number = []
    count = 0
    while count <= 5:
        number_r = randint(0, 9)
        number.append(str(number_r))
        count += 1

    str_number = ''.join(number)
    return str_number

# email verification
def check_email(email):
    try:
        users = []
        users.append(email)
        print('Start funk ok')
        code = str(random_number())
        mail = str(f'Your verification code: {code}')
        end = mailing(login='noreply014530@gmail.com', password='abpu xbea skec kjrp', topic='Email verification', mail_text=mail, users=users)
        print(str(email))
        return {
            'status': str(end),
            'email_code': str(code)
        }

    except Exception as _ex:
        return str(_ex)

# adding a user to the server database and generating a token
def add_user(name, last_name, phone):
    try:
        token = str(token_generator())
        print('Func ok')
        db.add_user(name, last_name, phone, token)
        print('Insert ok')
        return {
            'registration': 'successful',
            'token': token
        }
    except Exception as _ex:
        return str(_ex)