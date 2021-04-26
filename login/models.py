from functools import wraps

import jwt
from flask import request, jsonify
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from login import db, app


class User(db.Model, UserMixin):
    __tablename__ = "login_user"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=100), nullable=False)

    def __repr__(self):
        return f"{self.username}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()


def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):

      token = None

      if 'x-access-tokens' in request.headers:
         token = request.headers['x-access-tokens']
      if not token:
         return jsonify({'message': 'a valid token is missing'})

      try:
         data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
         current_user = User.query.filter_by(id=data['id']).first()
      except:
        return jsonify({'message': 'token is invalid'})

      return f(current_user, *args, **kwargs)
   return decorator