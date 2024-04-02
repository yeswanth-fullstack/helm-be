from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from flask import request
from bson.objectid import ObjectId
import socket

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

client = 'mongodb://mongo:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.2'
app.config['MONGO_URI'] = client
mongo = MongoClient(client)
db = mongo['chat']
collection = db['messages']

@app.route('/')
@cross_origin()
def hello():
    hostname = socket.gethostname()
    message = 'Welcome to chat app! App is running inside {} pod!'.format(hostname)
    return jsonify({'message': message})

@app.route('/test')
@cross_origin()
def content():
    data = [{"name": "Yeswanth", "message": "Hello"}, {"name": "Others", "message": "Hi"}]
    return jsonify(data)

# Create a new document
@app.route('/api', methods=['POST'])
@cross_origin()
def create():
    data = request.get_json()
    collection.insert_one(data)
    return jsonify({'message': 'Document created successfully'})

# Read all documents
@app.route('/api', methods=['GET'])
@cross_origin()
def read_all():
    data = list(collection.find({}))
    for doc in data:
        doc['_id'] = str(doc['_id'])
    return jsonify(data)

# Read a specific document
@app.route('/api/<id>', methods=['GET'])
@cross_origin()
def read(id):
    data = collection.find_one({'_id': ObjectId(id)})
    if data:
        data['_id'] = str(data['_id'])
        return jsonify(data)
    else:
        return jsonify({'message': 'Document not found'})

# Update a specific document
@app.route('/api/<id>', methods=['PUT'])
@cross_origin()
def update(id):
    data = request.get_json()
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.modified_count > 0:
        return jsonify({'message': 'Document updated successfully'})
    else:
        return jsonify({'message': 'Document not found'})

# Delete a specific document
@app.route('/api/<id>', methods=['DELETE'])
@cross_origin()
def delete(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Document deleted successfully'})
    else:
        return jsonify({'message': 'Document not found'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)