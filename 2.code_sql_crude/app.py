'''app.py
JWT  -  json web token   ( userid - is encoded and given to the user, the client gives the password to the server
server receive JWT to be sure that the client is authenticated
1. Install Flask_JWT
2. Set secret_key to application
import os
# >>> os.urandom(24)
3. Create new file security.py ( define func authenticate and identity
4. Create new file user.py : create class User in it
5. Import class User to security.py
6. Create instance jwt   -  Import JWT, authenticate, identity
create endpoint /auth
we can send jwt with request and app checks that the client is authenticated
7. import decorator jwt_required to give access to the Resource functions only if the user is authenticated
set this decorator to the function get(self, name) of Item(Resource)
8. Receive JWT token  -  make POST request to the endpoint /auth ( header set -  Content-Type: application/json)
 Body: {"username":"bob", "password":"asdf"}  ??? why without id ???
 we received {"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
 eyJleHAiOjE2MTY4MzU2NjQsImlhdCI6MTYxNjgzNTM2NCwibmJmIjoxNjE2ODM1MzY0LCJpZGVudGl0eSI6MX0.
 qOnJ_4_pSXCy8nrM4t7FDUxMGeXKQBtaNxh_jfyxoXA"} in response
If we try to receive item by name from get we receive following response:
{
    "description": "Request does not contain an access token",
    "error": "Authorization Required",
    "status_code": 401
}
To have access to the item we need to copy access token and mention in header
 Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciO..... after that we receive access to any item by name
9. Using regparse for checking data
9.1 import reqparse from flask_restful
9.2 correct put function to make sure that only float value with key "price" was given in the body.
9.3. update post function with parser
9.4. make parser as Class Varuable.
10. Using db sqlite for storing and retrieving users
10.1. Add 2 class methods to the class User: find_by_username(cls, username), ind_by_id(cls, _id)
10.2. Correct authenticate and identity function in security.py
10.3. Test.py  -  file with connectin to dp and requests for:
-create table users
-add several users to users table of db
- retrieve all the users from db and print them to check that they were added
11. Testing how it works from postman:
- POST request from /auth with body (name and password of the user that was add to db
- receive JWT in response
- GET response ( adding token to the headers) to receive one of item.
12. Create file (create_tables.py):
-import db, connection, cursor, query to create users table with incrementing id, commit and close connectin.
13.user.py -  create new class UserRegister(Resource)
- with parser that have 2 args username and password
- post method to create new user to the database with autoincrement id,
username and password from the client adding it to db.
14. Delete previous db and run create_tables.py to create new db. (vide0 81)
- run app.py
- add new user to db from /register resourse (post request)
- receive JWT input username and password in /auth ( post request),
- get request /item/<name> (add JWT at athorisation in headers).
15. Preventing duplicate of usernames ( video 82) - corectin in UserRegister method post
16. Retrieving items from the Database
16.1.remove items from app.py ( list) and create new file -  item.py
16.2 move classes Item and ItemList from app.py to item.py, clean imports
16.3. add correct imports in item.py and start to correct methods of Classes Item and ItemList
(for work with db instead of list items ).
16.3.1. Class Item, method get.
- Create new table items in create_tables.py and insert test_item
- delete old db to create new one with 2 tables ( users and items)
17. Adding items to db -  Class Item method post (video 84)
18. Deleting item from Db Class Item method delete (video 85)
19. Update item in db  Class Item method put
19.1 Extract 2.code_sql_crude from method to put to separate method that will be used for put also ( DRY )  - video 86
@classmethod    def insert(cls, item)
19.2 Reformat method put using classmethod insert
19.3. Create classmethod def update(cls, item), reformat method put using both insert and update classmethods.
20. Reformat class ItemList
'''


from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = b'\x18$\x93\xbf\x9c\xc5\x9c\xd4{\t\xfc\x07y\x89=\xf6\x9a\xc8[\xffG\xea\x97\x13'

api = Api(app)

# /auth (by default)
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
