from flask_restful import Resource, request, reqparse
from flask_jwt import jwt_required
from models.Store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")

    jwt_required()
    def get(self):
        name = request.args.get('name')
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()

        return {'message': 'Store not found'}, 404

    jwt_required()
    def post(self):
        try:
            data = Store.parser.parse_args()
            if StoreModel.find_by_name(data['name']):
                return {'message': "A store with the name '{}' already exists".format(data['name'])}, 400

            store = StoreModel(**data)
            store.save_to_db()

            return store.json(), 201

        except Exception:
            return {'Erro': Exception}, 500


    jwt_required()
    def delete(self):
        name = request.args.get('name')
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()

        return {'message': 'Store deleted successfully'}, 200


class StoreList(Resource):
    def get(self):
        try:
            return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
        except Exception:
            return {'Erro': Exception}
