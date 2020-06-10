from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair,CryptoKeypair
import json

bdb = BigchainDB('https://test.ipdb.io')

def crear_usuarios():
    users = []
    users.append (generate_keypair())
    users.append (generate_keypair())
    users.append (generate_keypair())
    users.append (generate_keypair())
    return users

def get_user (name):
    user = None
    with open ('users.json') as f:
        file_data = json.load(f)
        for element in file_data:
            if element["name"] == name:
                user = element
    if user == None:
        raise Exception ('not found')
    else:
        user = CryptoKeypair (private_key=user["private_key"],public_key=user["public_key"])
        return user

def cargar_coins ():

    darth_vader = get_user ("Darth Vader")
    boba_fett = get_user ("Boba Fett")
    greedo = get_user ("Greedo")
    din_djarin = get_user ("Din Djarin")

    coin_asset = {
    'data': {
        'name': "Galactic Coin",
    },
    }

    prepared_creation_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=darth_vader.public_key,
        asset=coin_asset,
        recipients=[([boba_fett.public_key],5),([greedo.public_key],3),([din_djarin.public_key],8)]
    )

    fulfilled_creation_tx = bdb.transactions.fulfill(
        prepared_creation_tx,
        private_keys=darth_vader.private_key
    )

    sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

    return sent_creation_tx

def cargar_armas ():

    darth_vader = get_user ("Darth Vader")

    metadata = {'type':"weapon"}

    weapon_assets = [
        {
    'data': {
        'name': "Sable de Luz",
        'cost': 6
    },
    },
    {
    'data': {
        'name': "Blaster",
        'cost': 3
    },
    },
    {
    'data': {
        'name': "Carabina Blaster EE-3",
        'cost': 4
    },
    },
    {
    'data': {
        'name': "Cañon Blaster",
        'cost': 8
    },
    },
    {
    'data': {
        'name': "Rifle Blaster E-22",
        'cost': 5
    },
    }
    ]
    
    for a in weapon_assets:
        prepared_creation_tx = bdb.transactions.prepare(
            operation='CREATE',
            signers=darth_vader.public_key,
            recipients=[([darth_vader.public_key], 10)],
            asset=a,
            metadata=metadata
        )

        fulfilled_creation_tx = bdb.transactions.fulfill(
            prepared_creation_tx,
            private_keys=darth_vader.private_key
        )
        sent_creation_tx = bdb.transactions.send_commit(fulfilled_creation_tx)

    return sent_creation_tx

def get_assets (user):
    res = []
    assets = bdb.assets.get(search='Galactic Coin')
    for a in assets:
        res.append (bdb.transactions.get(asset_id=a['id']))
    return res


