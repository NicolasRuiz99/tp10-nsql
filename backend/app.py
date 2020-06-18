from flask import Flask
from flask import render_template, jsonify, request, redirect, url_for
import json
from connectiondb import crear_usuarios,get_user,cargar_coins,get_assets,cargar_armas,get_user_coins,transfer_coins,get_user_weapons,transfer_weapon,prueba
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/crear_usuarios', methods=['GET'])
def get():
    try:
        user = crear_usuarios ()
        return jsonify (user)
    except (Exception) as err:
        return str(err), 500

@app.route('/cargar_coins', methods=['GET'])
def punto3():
    try:
        res = cargar_coins()
        return jsonify (res)
    except (Exception) as err:
        return str(err), 500

@app.route('/cargar_armas', methods=['GET'])
def punto4():
    try:
        res = cargar_armas()
        return jsonify (res)
    except (Exception) as err:
        return str(err), 500

@app.route('/get_assets', methods=['GET'])
def assets():
    try:
        res = prueba ()
        return jsonify (res)
    except (Exception) as err:
        return str(err), 500

@app.route('/get_user_coins', methods=['POST'])
def user_coins():
    try:
        name = request.json["name"]
        user = get_user(name)
        res = get_user_coins (user)
        return jsonify ({"coins":res})
    except (Exception) as err:
        return str(err), 500

@app.route('/get_user_weapons', methods=['POST'])
def user_weapons():
    try:
        name = request.json["name"]
        user = get_user(name)
        res = get_user_weapons (user)
        return jsonify (res)
    except (Exception) as err:
        return str(err), 500

@app.route('/transfer_coins', methods=['POST'])
def transferCoins():
    try:
        name1 = request.json["name1"]
        name2 = request.json["name2"]
        coins = request.json["coins"]
        user1 = get_user(name1)
        user2 = get_user(name2)
        res = transfer_coins (user1,user2,coins)
        return jsonify ({"result":res})
    except (Exception) as err:
        return str(err), 500

@app.route('/transfer_weapon', methods=['POST'])
def transferWeapon():
    try:
        name1 = request.json["name1"]
        name2 = request.json["name2"]
        id_weapon = request.json["id_weapon"]
        user1 = get_user(name1)
        user2 = get_user(name2)
        res = transfer_weapon (user1,user2,id_weapon)
        return jsonify ({"result":res})
    except (Exception) as err:
        return str(err), 500

@app.route('/buy_weapon', methods=['POST'])
def BuyWeapon():
    try:
        name1 = request.json["user"]
        id_weapon = request.json["weapon"]
        coins = request.json["coins"]
        user = get_user(name1)
        darth_vader = get_user("Darth Vader")
        transfer_coins (user,darth_vader,coins)
        transfer_weapon (darth_vader,user,id_weapon)
        return jsonify ({"result":"OK"})
    except (Exception) as err:
        return str(err), 500

@app.route('/about')
def about():
    """Retorna la pagina about."""
    return render_template('/about.html', msj="About de la pagina")



if __name__ == '__main__':
    app.run(host='backend', port='5000', debug=True)
