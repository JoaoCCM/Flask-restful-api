from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required)
from models.Auth import AuthModel
from models.User import UserModel

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

class Login(Resource):
    def post(self):
        try:
            data = parser.parse_args()
            user = UserModel.find_by_username(data['username'])

            if not user:
                raise Exception('User not found')

            if AuthModel.verify_hash(data['password'], user.password):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)

                return {'access_token': access_token, 'refresh_token': refresh_token}

            else:
                return {'message': 'Wrong credentials'}, 500

        except Exception as err:
            return {'Error': repr(err)}, 500
