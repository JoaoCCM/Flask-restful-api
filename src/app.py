from flask import Flask, Blueprint, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from resources.UserResource import UserRegister
from resources.ItemResource import Item, ItemList
from resources.StoreResource import Store, StoreList
from resources.AuthResource import Login, RefreshToken

load_dotenv()
  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_user(identity):
    if identity == 1:  # Instead of hard-code, you should read from a config file or database
        return {'admin': True}

    return {'admin': False}

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'Description':'Token Expired'}), 401

api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/user')
api.add_resource(Store, '/store')
api.add_resource(StoreList, '/stores')
api.add_resource(Login, '/signin')
api.add_resource(RefreshToken, '/refresh/token')


if __name__ == '__main__':
    from config.db import db
    db.init_app(app)
    app.run(debug=True, port=5000)
