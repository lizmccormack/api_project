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

body = {
  "logins": [
    {
      "email": "test@synapsefi.com"
    }
  ],
  "phone_numbers": [
    "901.111.1111",
    "test@synapsefi.com"
  ],
  "legal_names": [
    "Test User 2"
  ],
  "extra": {
    "supp_id": "122eddfgbeafrfvbbb",
    "cip_tag":1,
    "is_business": false
  }
}

new_user = client.create_user(body)

