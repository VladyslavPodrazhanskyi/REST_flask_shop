from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store {name} already exists'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the store"}, 500  # internal server error

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': f'store {name} was deleted'}
        return {'message': f'store {name} does not exist'}, 404


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}

