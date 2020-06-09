

def connect_db():
    conexion = redis.StrictRedis(port=6379, db=0, host="db-kylo-fr")
    if(conexion.ping()):
        print("conectado a redis")
    else:
        print("error de conexion con redis")
    return conexion

def get_list(nombre):
    db = connect_db()
    db.lpush(nombre, "luke, leia, han, chewbbaca")
    lista = db.lrange(nombre,0,-1)
    return lista


def get_kylo():
    db = connect_db()
    return db.get("kylo").decode('utf-8')
