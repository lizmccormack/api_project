import os
from synapsepy import Client

client = Client(
    'client_id'= os.environ['CLIENT_ID'], # your client id
    'client_secret'= os.environ['CLIENT_SECRET'], # your client secret
    'fingerprint'= USER_FINGERPRINT,
    'ip_address'= USER_IP_ADDRESS, # user's IP
    'devmode'= True, # (optional) default False
    'logging'= False # (optional) logs to stdout if True
)