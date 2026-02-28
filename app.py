import app
import uuid
from db import mystrore, myitems

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get('/store')
def getStore():
    return list(mystrore.values())


# request.get_json() returns a python dect or none if no json was sent
# it's also means get the incoming data from the client
@app.post("/store")
def postStore():
    requestdata = request.get_json()
    # this will add the posted data into the  store list with null items list
    store_id = uuid.uuid4().hex
    store = {**requestdata, "ids": store_id}
    mystrore[store_id] = store
    return jsonify(store), 201


@app.post('/item/')
def createitems():
    items_Data = request.get_json()
    if items_Data['store_id'] not in mystrore:
        return jsonify({
            'massege': "store id not found "
        })
    item_id = uuid.uuid4().hex
    itemWith_id = {**items_Data, "item id": item_id}
    myitems[item_id] = itemWith_id
    return jsonify(itemWith_id), 201


@app.get("/item")
def getallitem():
    return jsonify({"items": list(myitems.values())})


# now we have accessing the store id from the sore dictionaries
@app.get("/store/<string:store_id>")
def getspecificStore(store_id):
    try:
        return jsonify(mystrore[store_id])
    except KeyError:
        return jsonify("the items id not found ")


@app.get("/items/<string:items_ids>")
def getSpecificItems(items_ids):
    try:
        return jsonify(myitems[items_ids])
    except KeyError:
        return jsonify("not  found the the items id ")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
