from flask import (Flask, jsonify, request)
from flask_pymongo import PyMongo 
from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps
import json 
import os
from synapsepy import Client

client = Client(
    client_id= os.environ['CLIENT_ID'], 
    client_secret= os.environ['CLIENT_SECRET'], 
    fingerprint= os.environ['FINGERPRINT'],
    ip_address= os.environ['IP_ADDRESS'], 
    devmode= True, 
    logging= False 
)

app = Flask(__name__)

db_client = MongoClient('mongodb://localhost:27017/')
db = db_client['synapse_db']


# Users 
@app.route('/v1/users', methods=['GET'])
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


@app.route('/v1/users', methods=['POST'])
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
    new_user = db.synapse_db.users.insert({
        'user_id': new_user_synapse.id,
        'email': email, 
        "phone_numbers": phone_numbers, 
        "legal_names": legal_names
        })

    new_user = db.synapse_db.users.find_one({'user_id': new_user.id})
    output = json.dumps(new_user)

    return jsonify(dumps({'result': output}))


@app.route('/v1/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    """View one user."""
    
    allusers = db.synapse_db.users
    user = allusers.find_one({'user_id': user_id})

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
def update_user(user_id): 
    """Update one user."""
    pass 

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id): 
    """Delete a user."""
    pass 


# link bank accounts to make transactions / transfer funds 

@app.route('/v1/users/<user_id>/links', methods=['POST'])
def link_bank_accounts(user_id): 
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
    response = json.dumps(node)

    new_link = db.synapse_db.links.insert(response) 
    
    return jsonify(dumps({"result": response}))


@app.route('/v1/users/<user_id>/links/<node_id>', methods=['GET'])
def view_bank_account(user_id, node_id): 
    """View added bank accounts."""

    user = client.get_user(user_id)
    
    if user: 
    
        node = user.get_node(node_id) 
        response = json.dumps(node)
    
    else: 
        response = {
            'status_code': 404 
        }

    return jsonify(dumps({"result": response}))


@app.route('/v1/users/<user_id>/links/<node_id>/trans', methods=['POST'])
def create_transaction(user_id, node_id):
    """Create a new transaction."""
    
    to_type = request.json["to_type"]
    to_id = request.json["to_id"]
    amount = request.json["amount"]
    amount_currency = request.json["currency"]
    ip = request.json["ip"]

    user = client.get_user(user_id)
    transaction = user.create_trans(node_id, body)

    response = json.dump(transaction)

    return jsonify(dumps({"result": response})) 


# open a synapse deposit accout as a checking or spending account 

@app.route('/v1/users/<user_id>/spending', methods=['POST'])
def open_spending_account(user_id): 
    """Create a spending account as a deposit account."""
    
    type_ = request.json["type"]
    nickname = request.json["nickname"]
    document_id = request.json["document_id"]

    user = client.get_user(user_id)
    user_spending_node = user.create_node(body, idempotency_key='123456')
    response = json.dumps(user_spending_node)

    new_spending = db.synapse_db.spending.insert(response) 

    return jsonify(dumps{"result": response})



@app.route('/v1/users/<user_id>/spending/<node_id>', methods=['GET'])
def view_deposit_account(user_id, node_id):
    """View spending account."""

    user = client.get_user(user_id)

    if user: 
    
        node = user.get_node(node_id) 
        response = json.dumps(node)
    
    else: 
        response = {
            'status_code': 404 
        }

    return jsonify(dumps({"result": response}))

@app.route('/v1/users/<user_id>/spending/<node_id>/trans', methods=['POST'])
def fund_withdraw_spending_account(user_id, node_id):
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
    response = json.dumps(user_spending_trans)

    new_spending_transaction = db.synapse_db.spending_trans.insert(response)

    return jsonfiy(dumps("result": response))


# open a synapse interest bearing account as a savings account 

@app.route('/v1/users/<user_id>/savings', methods=['POST'])
def open_savings_account(user_id): 
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

    new_savings= db.synapse_db.spending_trans.insert(user_savings_node)
    response = json.dumps(user_savings_node)
    
    return jsonfiy(dumps("result": response))

@app.route('/v1/users/<user_id>/savings/<node_id>', methods=['GET'])
def view_savings_account(user_id, node_id): 
    """View savings account."""

    user = client.get_user(user_id)

    if user: 
    
        node_view = user.get_user_node(node_id)
        response = json.dumps(node_view)
    
    else: 
        response = {
            'status_code': 404 
        }

    return jsonify(dumps({"result": response}))

@app.route('/v1/users/<user_id>/savings/<node_id>/trans', methods=['POST'])
def fund_withdraw_savings_account(user_id, node_id):
    """Funds or withdraws from savings account.""" 

    to_type = request.json["type"]
    to_id = request.json["id"]
    amount = request.json["amount"]
    currency = request.json["currency"]
    ip = reuqest.json["ip"]
    note = request.json["note"]

    user = client.get_user(user_id)
    user_savings_trans = user.create_trans(node_id, body)
    response = json.dumps(user_savings_trans)

    new_savings_transaction = db.synapse_db.saving_trans.insert(response)

    return jsonfiy(dumps("result": response))


# open a subnet / issue debit card (for your deposit account)

@app.route('/v1/users/<user_id>/spending/<node_id>/cards', methods=['POST'])
def create_card_number(user_id, node_id, card_id):
    """Create a new card number."""
    
    nickname = request.json["nickname"]
    account_class = request.json["account_class"]

    user = client.get_user(user_id)
    user_card_number = create_subnet(node_id, body)

    # add to database 
    return jsonfiy(dumps("result": response))


@app.route('/v1/users/<user_id>/spending/<node_id>/cards/<card_id>', methods=['PUT'])
def update_card_status(user_id, node_id, card_id):
    """Activate, deactivate or terminate card."""
    
    status = request.json["status"]
    allow_foreign_transactions = request.json["allow_foreign_transactions"]
    daily_atm_withdrawal = request.json["daily_atm_withdrawal"]
    daily_transaction_limit = request.json["daily_transaction_limit"]

    user = client.get_user(user_id)
    user_card_status = user.update_subnet(node_id, subnet_id, body)

    # update database 
    return jsonfiy(dumps("result": response))

@app.route('/v1/users/<user_id>/spending/<node_id>/cards/<card_id>', methods=['PATCH'])
def update_card_pin(user_id, node_id, card_id):
    """Set the card pin."""
    
    card_pin = request.json["card_pin"] # need to add encryption 

    body = {
        "card_pin": card_pin
    }

    user = client.get_user(user_id) 
    user_pin_update = user.update_subnet(node_id, subnet_id, body)

    # add to database 
    return jsonfiy(dumps("result": response))

@app.route('/v1/users/<user_id>/spending/<node_id>/cards/<card_id>', methods=['GET'])
def view_card(user_id, node_id, card_id): 
    """View card."""
    
    user = client.get_user(user_id)
    user_card = user.get_subnet(node_id, subnet_id)

@app.route('/v1/users/<user_id>/spending/<node_id>/cards/<card_id>/send', methods=['POST'])
def send_card(user_id, node_id, card_id):
    """Send physical card."""
    
    fee_node_id = request.json["fee_node_id"]
    expedite = request.json["expedite"]
    card_style_id = request.json["card_style_id"]
    cardholder_name = request.json["cardholder_name"]

    user = client.get_uer(user_id)
    user_send_card = user.ship_card(node_id, card_id, body)

    # response that it is being sent 
    return jsonfiy(dumps("result": response))


@app.route('/v1/users/<user_id>/spending/<node_id>/cards/<card_id>', methods=['DELETE'])
def delete_card(user_id, node_id, card_id):
    """Delete card."""
    
    status = request.json["status"]

    body = {
        "status": status 
    }

    user = client.get_user(user_id) 
    user_delete_card = user.update_subnet(node_id, card_id, body)

    # return sucess message 
    return jsonfiy(dumps("result": response))


# transactions 

@app.route('/v1/users/<user_id>/trans', methods=['GET'])
def view_user_transactions(user_id): 
    """View transactions for a user.""" 

    user = client.get_user(user_id)
    transactions = user.get_all_trans()

   return jsonfiy(dumps("result": response)) 

@app.route('/v1/users/<user_id>/nodes/<node_id>/trans')
def view_account_transactions(user_id, node_id): 
    """View transactions for an account."""

    user = client.get_user(user_id)
    transactions = user.get_all_node_trans(node_id, page=4, per_page=10)

    return jsonfiy(dumps("result": response))


# helper functions 

if __name__ == "__main__": 
    app.debug = True 
    app.run(port=5000, host='0.0.0.0', debug=True)


