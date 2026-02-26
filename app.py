import app
import flask

from flask import Flask, request, jsonify

app = Flask(__name__)

mystrore = [
    {
        'name': 'my store',
        'items': [
            {
                'product': 'snack',
                'price': 20
            }

        ]

    },
]


@app.get('/store')
def home():
    return jsonify({
        'myStore': mystrore

    })


# request.get_json() returns a python dect or none if no json was sent
# it's also means get the incoming data from the client
@app.post("/store")
def postStore():
    get_request_Data = request.get_json()
    # this will add the posted data into the  store list with null items list
    new_store = {'name': get_request_Data['name'], 'items': []}
    mystrore.append(new_store)

    print(get_request_Data)
    return jsonify(new_store), 201


@app.post('/store/<string:name>/')
def createitems(name):
    get_request_Data = request.get_json()
    for store in mystrore:
        if store['name'] == name:
            newItem = {
                'product' : get_request_Data['product'],
                'price' : get_request_Data['price']
            }



            store['items'].append(newItem)
            return jsonify(newItem), 201


    return jsonify({
        'messeage': 'there is no data found'
    }), 404




if __name__ == '__main__':
    app.run(debug=True)
