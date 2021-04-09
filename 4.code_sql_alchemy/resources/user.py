from flask_restful import Resource, reqparse
import sqlite3
from models.user import UserModel


# /register resource
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='username cannot be left blank'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='password cannot be left blank'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': "Sorry, but user with current username already exists"}, 400
        user = UserModel(**data)   #(data['username'], data['password'])
        user.save_to_db()
        return {"message": "User created successfully"}, 201


