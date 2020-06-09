from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

bdb = BigchainDB('https://test.ipdb.io')

def crear_usuarios():
    users = []
    users.append (generate_keypair())
    users.append (generate_keypair())
    users.append (generate_keypair())
    users.append (generate_keypair())
    return users

def get_list(nombre):
    db = connect_db()
    db.lpush(nombre, "luke, leia, han, chewbbaca")
    lista = db.lrange(nombre,0,-1)
    return lista


def get_kylo():
    db = connect_db()
    return db.get("kylo").decode('utf-8')
