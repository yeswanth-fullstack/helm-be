from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api')
def content():
    data = [{"name": "Yeswanth", "message": "Hello"}, {"name": "Others", "message": "Hi"}]
    return jsonify(data)

