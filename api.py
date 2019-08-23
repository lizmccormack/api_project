from flask import (Flask, jsonify, request)
from flask_pymongo import PyMongo 
from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps
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

db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['synapse_db']


@app.route('/')
def hello(): 
    """TEST"""
    return 'welcome to my api'

# Users 
@app.route('/users', methods=['GET'])
def get_all_users(): 
    """View all users."""
    allusers = db.synapse_db.users

    output = []
    for user in allusers.find(): 
        output.append({
            'email': user['email'],
            'phone_numbers': user['phone_numbers'],
            'legal_names': user['legal_names']
            })
    
    return jsonify(dumps({'result': output}))


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""

    email = request.json['email']
    phone_numbers = request.json['phone_numbers']
    legal_names = request.json['legal_names']

    body = {
        "logins": [
            {
                "email": email
            }
        ],
        "phone_numbers": [
            phone_numbers
        ],
        "legal_names": [
            legal_names
        ]
    }

    new_user_synapse = client.create_user(body, ip=os.environ['IP_ADDRESS'], fingerprint=os.environ['FINGERPRINT'])
    new_user_id = db.synapse_db.users.insert({
        'email': email, 
        "phone_numbers": phone_numbers, 
        "legal_names": legal_names
        })

    new_user = db.synapse_db.users.find_one({'_id': new_user_id})
    output = {
        '_id': new_user['_id'], 
        'email': new_user['email'], 
        'phone_numbers': new_user['phone_numbers'], 
        'legal_names': new_user['legal_names']
        }
    
    return jsonify(dumps({'result': output}))


@app.route('/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    """View one user."""
    allusers = db.synapse_db.users
    user = allusers.find_one({'_id': user_id})

    if user: 
        output = {
            '_id': user['_id'], 
            'email': user['email'], 
            'phone_numbers': user['phone_numbers'], 
            'legal_names': user['legal_names']
        }

    else: 
        output = "user does not exist" 
    
    return jsonify(dumps({'result': output}))

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(): 
    """Update one user."""
    pass 

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(): 
    """Delete a user."""
    

# functionality 

# link bank accounts to make transactions 

@app.route('/accounts', methods=['POST'])
def link_bank_accounts(): 
    """Add a node to link a bank account."""
    pass


@app.route('/accounts/<node_id>', methods=['GET'])
def view_bank_account(): 
    """View added bank accounts."""
    pass


@app.route('/accounts/<node_id>/trans', methods=['POST'])
def create_transaction():
    """Create a new transaction."""
    pass

# open a deposit accout 







# open an interest bearing account 







# open a subnet / issue debit card 






# view statements 






# transactions 







# wire money from app / to app 




# loans 




if __name__ == "__main__": 
    app.debug = True 
    app.run(port=5000, host='0.0.0.0', debug=True)


