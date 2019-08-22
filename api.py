
from flask import (Flask, jsonify, request)
from flask_pymongo import PyMongo 
from pymongo import MongoClient
import os
from synapsepy import Client

client = Client(
    client_id= os.environ['CLIENT_ID'], # your client id
    client_secret= os.environ['CLIENT_SECRET'], # your client secret
    fingerprint= os.environ['FINGERPRINT'],
    ip_address= os.environ['IP_ADDRESS'], # user's IP
    devmode= True, # (optional) default False
    logging= False # (optional) logs to stdout if True
)

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'synapse_db'
app.config["MONGO_URL"] = 'mongodb://localhost:27017/synapse_db'
mongo = PyMongo(app)


@app.route('/')
def hello(): 
    """TEST"""
    return 'welcome to my api'

# Users 
@app.route('/users', methods=['GET'])
def get_all_users(): 
    """View all users."""
    allusers = client.get_all_users(show_refresh_tokens=True)

    return jsonify(allusers)

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    pass

@app.route('/users/<user_id>', methods=['GET'])
def get_one_user():
    """View one user."""
    pass

@app.route('/users/<user_id>' methods=['PUT'])
def update_user(): 
    """Update one user."""
    pass 

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(): 
    """Delete a user."""
    pass 

# functionality 


