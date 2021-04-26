import datetime

import jwt

from login import app, db
from flask import request, jsonify, make_response

from login.models import User, token_required


@app.route('/')
@app.route('/home')
@token_required
def home_page(current_user):
    return jsonify({'message': current_user.id})


@app.route("/register", methods=["GET", "POST"])
def register_page():
    json_req = request.get_json()
    username = json_req.get('username')
    email = json_req.get('email')
    password = json_req.get('password')

    user_to_create = User.get_by_email(email)

    if user_to_create is not None:
        return make_response({ "message": f'El email {email} ya está siendo utilizado por otro usuario'})
    else:
        user_to_create = User(username=username, email=email)
        user_to_create.set_password(password)
        user_to_create.save()

    return make_response(jsonify({"message": "success"}), 200)


@app.route("/login", methods=["GET", "POST"])
def login_page():

    auth = request.authorization
    print(auth)

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(username=auth.username).first()
    if user.check_password(auth.password):
        token = jwt.encode(
            {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
            app.config['SECRET_KEY'], algorithm="HS256")
        return token
    else:
        return make_response('Esto no funciona', 500, {"goasdmasdasd asdmasd"})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})