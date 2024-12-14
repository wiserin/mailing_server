from flask import Flask, jsonify, request
from server.mailing import mailing
from server.app import check_email
import server.app
from server.database.models import start_db
import server.database.requests as db


app = Flask(__name__)


@app.route('/check', methods=['POST'])
def check_user_token():
    try:
        print('Check')
        new_one = request.json
        print(new_one)
        check_token = db.check_token(new_one['token'])

        if check_token == True:
            print('Ok')
            return jsonify('True')
            
        
        elif check_token == False:
            print('Ok_1')
            return jsonify('False')
            
        
        else:
            print('NOT Ok')
            return jsonify('Unknown server error')
        
    except Exception as _ex:
        return jsonify(f'{_ex} Server error, Incorrect request format') 

# catching mailing requests by email
@app.route('/mailing', methods=['POST'])
def post_list():
    try:
        print('Try ok')
        new_one = request.json
        check_token = db.check_token(new_one['token']) 
        if check_token == True:
            print(new_one['token'])
            end = mailing(new_one['login'], new_one['password'], new_one['topic'], new_one['text'], new_one['users'])
            return jsonify(end)
        
        elif check_token == False:
            return jsonify('Initialization error, unknown token. Please register with: https://t.me/mailing_api_bot')
        
        else:
            return jsonify('Server unknown error')
        
    except Exception as _ex:
        return jsonify(f'{_ex} Server error, Incorrect request format') 


# catching email verification requests
@app.route('/email_verification', methods=['POST'])
def email_verification_f():
    try:
        new_one = request.json
        print('Try ok')
        check_token = db.check_token(new_one['token']) 
        if check_token == True:
            print('Check token ok')
            print(new_one['token'])
            end = check_email(new_one['email'])
            print('End ok')
            return jsonify(end)
        
        elif check_token == False:
            return jsonify('Initialization error, unknown token. Please register with: https://t.me/mailing_api_bot')
        
    except Exception as _ex:
        return jsonify(f'{str(_ex)}, server error')
    

# catching requests to add a user to the server database
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        print('Try ok')
        data = request.json
        user_name = str(data['name'])
        user_last_name = str(data['last_name'])
        user_email = str(data['email'])
        print('Init ok')
        _request = server.app.add_user(user_name, user_last_name, user_email)
        print('Func end ok')
        return jsonify(_request)
    
    except Exception as _ex:
        return jsonify(f'{str(_ex)}, server error')

if __name__ == "__main__":
    start_db
    app.run(host='0.0.0.0')
    