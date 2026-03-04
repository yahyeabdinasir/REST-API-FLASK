
import app
import uuid
from db import mystrore, myitems
from flask import abort

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get('/store')
def getStore():
    return jsonify({"items": list(mystrore.values())})


# request.get_json() returns a python dect or none if no json was sent
# it's also means get the incoming data from the client
@app.post("/store")
def postStore():
    requestdata = request.get_json()
    # this will add the posted data into the  store list with null items list

    # make sure the payload includes the name of the store
    if 'name' not in requestdata:
        abort(400, description="Name already exists")
    # also check if the name is already exists we do this to make that each name is unique
    for store in mystrore.values():
        if store['name'] == requestdata['name']:
            abort(400, description="Store name already exists")


    store_id = uuid.uuid4().hex
    store = {**requestdata, "ids": store_id}
    mystrore[store_id] = store
    return jsonify(store), 201


@app.post('/item')
def createitems():
    items_Data = request.get_json()
    # so here means when we are making the item it must connect with the store it's relational with one two many
    if not items_Data or "store_id" not in items_Data:
        abort(400,
              description="store id or request data  is requires "
              )
    # check if the store id exists
    if items_Data['store_id'] not in mystrore:
        abort(400,
              description="store id not found in my store "
              )
        #  checking duplication if the store already  has the name and also the price
    for myuniqueitem in myitems.values():
        if (myuniqueitem['name'] == items_Data['name'] or
                myuniqueitem['price'] == items_Data['price']):
            abort(400, description=" the items  already exisits in there")

    item_id = uuid.uuid4().hex
    itemWith_id = {**items_Data, "item id": item_id}
    myitems[item_id] = itemWith_id

    return jsonify(itemWith_id), 201,


@app.get("/item")
def getallitem():
    return jsonify({"items": list(myitems.values())})


# now we have accessing the store id from the sore dictionaries
@app.get("/store/<string:store_id>")
def getspecificStore(store_id):
    try:
        return jsonify(mystrore[store_id])
    except KeyError:
        # abort is flask object that handles the  return with the document so it's best practice to use that
        abort(500, description="the items id not found ")




@app.delete("/store/<string:store_id>")
def deletepecificStore(store_id):
    try:

        if store_id not in mystrore:
            abort(500, description="not  found the the store id")

        del mystrore[store_id]
        return jsonify({"messege" : " the store deleted successfuly "})
    except KeyError:
        # abort is flask object that handles the  return with the document so it's best practice to use that
        abort(500, description="the items id not found ")



@app.get("/item/<string:items_ids>")
def getSpecificItems(items_ids):
    try:
        return jsonify(myitems[items_ids])
    except KeyError:
        abort(500, description="not  found the the items id")


@app.delete("/item/<string:items_ids>")
def deleteItem(items_ids):
    try:
        if items_ids not in myitems:
            return jsonify({"messege": "not  found the the items id"})


        del myitems[items_ids]
        return {"message": "Item deleted successfully"}, 200
    except KeyError:
        abort(404, description="Item not found")




@app.put("/item/<string:items_ids>")
def updateItems(items_ids):
    Data = request.get_json()
    #      iterate over the items value

    if not Data:
        abort(400, description="Missing JSON body")

    if items_ids not in myitems:
        abort(404, description="Item not found")

    item = myitems[items_ids]
    item['name'] = Data.get("name", item["name"])
    # now that mean if the client sends data  like name or the price update it if not keep old one
    item['price'] = Data.get("price", item["price"])




    return jsonify(myitems[items_ids]), 201



    return jsonify({"message": "Item not found"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
