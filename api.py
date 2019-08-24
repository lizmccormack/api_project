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
    pass 
    

# functionality 

# link bank accounts to make transactions / transfer funds 

@app.route('/users/<user_id>/links', methods=['POST'])
def link_bank_accounts(): 
    """Add a node to link a bank account."""
    
    type_ = request.json['type']
    bank_id = request.json['bank_id']
    bank_pw= request.json['bank_pw']
    bank_name = request.json['bank_name']

    body = {
        "type": type_,
        "info": {
            "bank_id": bank_id,
            "bank_pw": bank_pw,
            "bank_name": bank_name
        }
    }

    user = client.get_user(user_id)
    node = user.create_node(body)
    
    # add it to the data base 


@app.route('/users/<user_id>/links/<node_id>', methods=['GET'])
def view_bank_account(): 
    """View added bank accounts."""
    
    user = client.get_user(user_id)
    node = user.get_node(node_id) 
    
    #return json response 


@app.route('/users/<user_id>/links/<node_id>/trans', methods=['POST'])
def create_transaction():
    """Create a new transaction."""
    
    to_type = request.json["to_type"]
    to_id = request.json["to_id"]
    amount = request.json["amount"]
    amount_currency = request.json["currency"]
    ip = request.json["ip"]

    user = client.get_user(user_id)
    user.create_trans(node_id, body)

    # return json response 


# open a synapse deposit accout as a checking or spending account 

@app.route('/users/<user_id>/spending', methods=['POST'])
def open_spending_account(): 
    """Create a spending account as a deposit account."""
    
    type_ = request.json["type"]
    nickname = request.json["nickname"]
    document_id = request.json["document_id"]

    user = client.get_user(user_id)
    user.create_node(body, idempotency_key='123456')

    # add to database 



@app.route('/users/<user_id>/spending/<node_id>', methods=['GET'])
def view_deposit_account():
    """View spending account."""
    
    user = client.get_user(user_id)
    node = user.get_node(node_id)  

    # return json response

@app.route('/users/<user_id>/spending/<node_id>/trans', methods=['POST'])
def fund_withdraw_spending_account():
    """Funds or withdraws from deposit account.""" 

    to_type = request.json['type']
    to_id = request.json["id"]
    amount = reuqest.json["amount"]
    amount_currency = request.json["currency"]
    ip = request.json["ip"]
    note = request.json["note"]

    body = {
        "to": {
            "type": to_type, 
            "id": to_id
        }, 
        "amount": {
            "amount": amount,
            "currency": amount_currency   
        },
        "extra": {
            "ip": ip,
            "note": note
        }
    }

    
    user = client.get_user(user_id)
    user_spending_trans = user.create_trans(node_id, body)

    # return json reponse

# open a synapse interest bearing account as a savings account 

@app.route('users/<user_id>/savings', methods=['POST'])
def open_savings_account(): 
    """Create a savings account as an interest bearing account.""" 
    
    type_ = request.json["type"]
    nickname = request.json["nickname"]

    body = {
        "type": type_,
        "info": {
            "nickname": nickname
        }
    }

    user = client.get_user(user_id)
    user_savings_node = user.create_node(body)

    # add to database 
    # return request kasfj

@app.route('users/<user_id>/savings/<node_id>', methods=['GET'])
def view_savings_account(): 
    """View savings account."""
    
    user = client.get_user(user_id) 
    user.get_user_node(node_id)

    # return json response 


@app.route('/users/<user_id>/savings/<node_id>/trans', methods=['POST'])
def fund_withdraw_savings_account():
    """Funds or withdraws from savings account.""" 

    to_type: request.json["type"]
    to_id: request.json["id"]
    amount: request.json["amount"]
    currency: request.json["currency"]
    ip: reuqest.json["ip"]
    note: request.json["note"]

    user = client.get_user(user_id)
    user_savings_trans = user.create_trans(node_id, body)

    # add to transactions db 
    # return something 


# open a subnet / issue debit card (for your deposit account)

@app.route('/users/<user_id>/spending/<node_id>/cards', methods=['POST'])
def create_card_number():
    """Create a new card number."""
    pass

@app.route('/users/<user_id>/spending/<node_id>/cards/<card_id>', methods=['PUT'])
def update_card_statu():
    """Activate, deactivate or terminate card."""
    pass 

@app.route('/users/<user_id>/spending/<node_id>/cards/<card_id>', methods=['PATCH'])
def update_card_pin():
    """Set the card pin."""
    pass 

@app.route('/users/<user_id>/spending/<node_id>/cards/<card_id>', methods=['GET'])
def view_card(): 
    """View card."""
    pass 

@app.route('/users/<user_id>/spending/<node_id>/cards/<card_id>/send', methods=['POST'])
def send_card():
    """Send physical card."""
    pass 


@app.route('/users/<user_id>/spending/<node_id>/cards/<card_id>', methods=['DELETE'])
def delete_card():
    """Delete card."""
    pass 


# make statements round up to the nearest dollar and add to savings 


# helper functions 

if __name__ == "__main__": 
    app.debug = True 
    app.run(port=5000, host='0.0.0.0', debug=True)


