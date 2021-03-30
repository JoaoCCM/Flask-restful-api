from flask_restful import Resource, reqparse, request
from models.Item import ItemModel
from flask_jwt_extended import get_jwt, jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
    )
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )

    @jwt_required()
    def get(self):
        name = request.args.get('name')        
        item = ItemModel.find_by_name(name)
        
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self):
        claims = get_jwt()

        if not claims['admin']:
            return {'message': 'You need admin privileges'}, 401

        data = Item.parser.parse_args()
        if ItemModel.find_by_name(data['name']):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400


        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self):
        name = request.args.get('name') 
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def put(self):
        name = request.args.get('name') 
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.name = data['name']
            item.price = data['price']
        else:
            item = ItemModel(**data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [x.json() for x in ItemModel.find_all()]}

