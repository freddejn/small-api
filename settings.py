from google.cloud import datastore
import secrets
import datetime

class Settings:
    jwt_id = 1 # Should be 1 as only one secret should exist in database.

def generate_jwt_secret():
    return secrets.token_bytes(16)
    
def get_jwt_secret():
    client, kind = get_secret_client()
    key = client.key(kind, Settings.jwt_id)
    ds_secret = datastore.Entity(key=key)
    return client.get(key=key)

def store_secret_in_datastore(secret):
    client, kind = get_secret_client()
    key = client.key(kind, Settings.jwt_id)
    ds_secret = datastore.Entity(key=key)
    ds_secret['secret'] = secret
    ds_secret['created'] = datetime.datetime.now()
    client.put(ds_secret)
    print('secret created')
    return True

def get_secret_client():
    client = datastore.Client()
    kind = 'Secret'
    return (client, kind)

