# first_app.py
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'Our_beautiful_store',
        'items': [
            {
                'name': 'toy',
                'price': 15
            }
        ]
    }
]


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/store', methods=['POST'])   # set headers : Content-Type application/json
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store is not found'})


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store/<name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'store is not found'})


@app.route('/store/<name>/items')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'store is not found'})


if __name__ == '__main__':
    app.run(debug=True)
