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


@app.route('/')
def hello(): 
    """TEST"""
    return 'welcome to my api'

# Users 
@app.route('/users', methods=['GET'])
def get_all_users(): 
    """View all users."""
    allusers = mongo.db.users.find()

    output = []
    for users in allusers.find(): 
        output.append({'name': users['name']})
    
    return jsonify({'result': output})
    
    
    
    # allusers = client.get_all_users(show_refresh_tokens=True)
    # print(dir(allusers))
    # print(allusers.list_of_users)
    # users_list = []
    
    # for user in allusers.list_of_users: 

    #     body = {
    #         "_id": user.id,

    #     }
    #     print(user.id)

    #     users_list.append(body)
    
    # print(users_list)
    
    # response = {
    #     "limit": allusers.limit,
    #     "page": allusers.page,
    #     "page_count": allusers.page_count, 
    #     "users": users_list
    # }

    # print(allusers.limit)
    # print(allusers.page)
    # print(allusers.page_count)
    # return jsonify(response)
        


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""

    # get all the feilds you need to create a new user 
    # create the body 
    # get the ip 

    new_user = client.create_user(body, ip, fingerprint=fingerprint)

    

    # return response object, 201 

@app.route('/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    """View one user."""
    allusers = mongo.db.users
    user = allusers.find_one({'user_id': userid})

    if user: 
        output = {body}

    else: 
        output = "user does not exist" 
    
    return jsonify({'result': output})

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(): 
    """Update one user."""
    pass 

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(): 
    """Delete a user."""
    pass 

# functionality 

# link bank accounts 






# open a subnet / issue debit card 






# view statements 






# transactions 





# wire money from app / to app 








# loans 









def connect_to_db(app, db_name='synapse_db', db_uri='mongodb://localhost:27017/synapse_db'): 
    app.config["MONGO_DBNAME"] = db_name
    app.config["MONGO_URI"] = db_uri
    mongo = PyMongo(app)

if __name__ == "__main__": 
    app.debug = True 
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')


