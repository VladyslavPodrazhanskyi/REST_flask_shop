from werkzeug.security import safe_str_cmp  # safe compare of strings
from models.user import UserModel


# users = [
#     User(1, 'bob', 'asdf')
# ]

# create mappings to avoid iterate for whole list and have direct access to the user
# by its name or its id.

# username_mapping = {u.username: u for u in users}
# userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    '''
    accept username and password
    returns user if password is correct
    '''
    # user = username_mapping.get(username)
    # if user and user.password == password:
    user = UserModel.find_by_username(username)
    if safe_str_cmp(user.password, password):
        return user


def identity(payload):
    '''
    receive payload (dicitionary that have key  'identity' with user_id)
     from client's JWT -
    returns user
    '''
    user_id = payload['identity']
    # return userid_mapping.get(user_id)
    return UserModel.find_by_id(user_id)
