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

def prueba ():
    asset = bdb.assets.get(search='Sable de Luz')[0]
    res = bdb.transactions.get(asset_id=asset["id"])
    return res

def get_assets (user,coins):
    lista = []
    res = bdb.outputs.get(user.public_key,False)
    for i in res:
        i["transaction"] = bdb.transactions.retrieve(txid=i["transaction_id"])
        if i["transaction"]["metadata"] == None and coins == True:
            lista.append (i)
        elif i["transaction"]["metadata"] != None and coins == False:
            lista.append (i)
    return lista

def get_user_weapons (user):
    user_list = get_assets (user,False)
    result = []

    for i in user_list:
        if i["transaction"]["operation"] == 'CREATE':
            data = i["transaction"]["asset"]
            id = i["transaction"]["id"]
        else:
            data = bdb.transactions.get(asset_id=i["transaction"]["asset"]["id"], operation='CREATE')[0]["asset"]
            id = i["transaction"]["asset"]["id"]
        
        amount = i["transaction"]["outputs"][i["output_index"]]["amount"]
        asset = {"id":id,"data":data["data"],"amount":int (amount)}

        found = False
        for r in result:
            if (len(result) > 0) and (r["id"] == asset["id"]):
                r["amount"] = int(r["amount"]) + int(amount)
                found = True
                break

        if (found == False):
            result.append(asset)
            
    return result

def get_user_coins (user):
    coins = 0
    transactions = get_assets (user,True)
    for i in transactions:
        outputs = i["transaction"]["outputs"]
        output = outputs [i["output_index"]]
        coins += int(output["amount"])

    return coins

def transfer_coins (user1,user2,coins):
    transactions = get_assets (user1,True)
    coins_left = int(coins)
    i = 0

    while coins_left != 0 and i < len(transactions):
        item = transactions[i]
        outputs = item["transaction"]["outputs"]
        output = outputs [item["output_index"]]
        amount = int(output["amount"])

        transfer_input = {
                'fulfillment': output['condition']['details'],
                'fulfills': {
                'output_index': item ["output_index"],
                'transaction_id': item["transaction_id"],
            },
                'owners_before': output['public_keys'],
            }

        if (item["transaction"]["operation"] == 'CREATE'):
            transfer_asset = {
            'id': item["transaction"]["id"],
            }
        else:
            transfer_asset = {
            'id': item["transaction"]["asset"]["id"],
            }    

        if amount > coins_left:
            prepared_transfer_tx = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=[([user2.public_key], coins_left), ([user1.public_key], amount - coins_left )]
            )

            fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx, private_keys=user1.private_key)

            bdb.transactions.send_commit(fulfilled_transfer_tx)

            coins_left = 0
        elif amount == coins_left:
            prepared_transfer_tx = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=[([user2.public_key], coins_left)]
            )

            fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx, private_keys=user1.private_key)

            bdb.transactions.send_commit(fulfilled_transfer_tx)

            coins_left = 0

        else:
            prepared_transfer_tx = bdb.transactions.prepare(
            operation='TRANSFER',
            asset=transfer_asset,
            inputs=transfer_input,
            recipients=[([user2.public_key], amount)]
            )

            fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx, private_keys=user1.private_key)

            bdb.transactions.send_commit(fulfilled_transfer_tx)

            coins_left = coins_left - amount

        i += 1

    return "OK"

def transfer_weapon (user1,user2,id_weapon):
    transactions = get_assets (user1,False)

    for i in transactions:
        if (i["transaction"]["operation"] == 'CREATE' and i["transaction"]["id"] == id_weapon) or (i["transaction"]["operation"] == 'TRANSFER' and i["transaction"]["asset"]["id"] == id_weapon):
            outputs = i["transaction"]["outputs"]
            output = outputs [i["output_index"]]
            amount = int(output["amount"])

            transfer_input = {
                    'fulfillment': output['condition']['details'],
                    'fulfills': {
                    'output_index': i ["output_index"],
                    'transaction_id': i["transaction_id"],
                },
                    'owners_before': output['public_keys'],
                }

            if (i["transaction"]["operation"] == 'CREATE'):
                transfer_asset = {
                'id': i["transaction"]["id"],
                }
            else:
                transfer_asset = {
                'id': i["transaction"]["asset"]["id"],
                }    

            if amount == 1:
                prepared_transfer_tx = bdb.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                metadata={"type":"weapon"},
                recipients=[([user2.public_key], amount)]
                )

                fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx, private_keys=user1.private_key)

                return bdb.transactions.send_commit(fulfilled_transfer_tx)

            else:
                prepared_transfer_tx = bdb.transactions.prepare(
                operation='TRANSFER',
                asset=transfer_asset,
                inputs=transfer_input,
                metadata={"type":"weapon"},
                recipients=[([user2.public_key], 1),([user1.public_key], amount - 1)]
                )

                fulfilled_transfer_tx = bdb.transactions.fulfill(prepared_transfer_tx, private_keys=user1.private_key)

                return bdb.transactions.send_commit(fulfilled_transfer_tx)

    raise Exception ("transaction not complete")

    
