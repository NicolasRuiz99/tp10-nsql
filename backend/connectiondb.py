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

def get_assets ():
    asset = bdb.assets.get(search='Galactic Coin')[0]
    res = bdb.transactions.get(asset_id=asset['id'])
    return res

def get_user_coins (user):
    coins = None
    transaction_id = None
    output_index = None
    output = None
    transactions = get_assets ()
    for i in range(len(transactions)):
        t = transactions[-i-1]
        outputs = t["outputs"]        
        for index,o in enumerate (outputs):
            if user.public_key in o["condition"]["details"]["public_key"]:
                coins = o["amount"]
                output_index = index
                break
        if coins != None:
            transaction_id = t["id"]
            output = t["outputs"][output_index]
            break
    return [coins,transaction_id,output_index,output]

def transfer_coins (user1,user2,coins,transaction_id,output,output_index):
    transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills': {
        'output_index': output_index,
        'transaction_id': transaction_id,
    },
        'owners_before': output['public_keys'],
    }

    transfer_asset = {
        'id': transaction_id,
    }

    coins_left = int(output["amount"])- int (coins)
    if (coins_left < 0):
        prepared_transfer_tx = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=[([user2.public_key], int(coins)), ([user1.public_key], coins_left )]
        )
    else:
        prepared_transfer_tx = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=[([user2.public_key], int(coins)), ([user1.public_key], coins_left )]
        )
    

    fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx, private_keys=user1.private_key)

    bdb.transactions.send_commit(fulfilled_transfer_tx)

    return fulfilled_transfer_tx



