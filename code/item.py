import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=int,
                        required=True,
                        help='should have type float and cannot be left blank'
                        )

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x.get('name') == name, items), None)
        # return item, 200 if item is not None else 404
        item = self.find_by_name(name)
        if item:
            return item, 200
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None):
        if self.find_by_name(name):
            return {'message': f'item {name} already exists'}, 400
        # data = request.get_json()              # Content-Type  application/json - set header in postman
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        # items.append(item)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        return item, 201

    # def delete(self, name):
    #     item = next(filter(lambda x: x['name'] == name, items), None)
    #     if item:
    #         items.remove(item)
    #         return {'message': f'item {name} was deleted'}
    #     return {'message': f'item {name} does not exist'}, 404

    def delete(self, name):
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name, ))
            connection.commit()
            connection.close()
            return {'message': f'item {name} was deleted'}
        return {'message': f'item {name} does not exist'}, 404

        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message': f'item {name} was deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        item = {'name': name, 'price': data['price']}
        # if item with name exists:
        if self.find_by_name(name):
            query = "UPDATE items " \
                    "SET price=?," \
                    "WHERE name=?"
            cursor.execute(query, (item['price'], name))
        # if item with name does not exist:
        else:
            query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()
        return item





        # item = next(filter(lambda x: x['name'] == name, items), None)
        # # data = request.get_json()
        # if item is None:
        #     item = {'name': name, 'price': data['price']}
        #     items.append(item)
        # else:
        #     item.update(data)
        # return item

    # def put(self, name):
    #     data = request.get_json()
    #     for item in items:
    #         if item['name'] == name:
    #             item['price'] = data['price']
    #             return {'message': f'item {name} was updated'}
    #     items.append({'name': name, 'price': data['price']})
    #     return {'message': f'item {name} was created'}

    # def put(self, name):
    #     data = Item.parser.parse_args()
    #     item = next(filter(lambda x: x['name'] == name, items), None)
    #     # data = request.get_json()
    #     if item is None:
    #         item = {'name': name, 'price': data['price']}
    #         items.append(item)
    #     else:
    #         item.update(data)
    #     return item


class ItemList(Resource):
    def get(self):
        return {'items': items}

