from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db


from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.secret_key = b'\x18$\x93\xbf\x9c\xc5\x9c\xd4{\t\xfc\x07y\x89=\xf6\x9a\xc8[\xffG\xea\x97\x13'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()



# /auth (by default)
jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, "/register")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port=5000)

