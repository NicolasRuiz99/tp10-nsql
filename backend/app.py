from flask import Flask
from flask import render_template, jsonify, request, redirect, url_for
import json
from connectiondb import crear_usuarios,get_user,cargar_coins,get_assets,cargar_armas,get_user_coins,transfer_coins,get_user_weapons
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_user', methods=['POST'])
def get():
    try:
        name = request.json["name"]
        user = get_user(name)
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
        res = get_assets ()
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

@app.route('/about')
def about():
    """Retorna la pagina about."""
    return render_template('/about.html', msj="About de la pagina")



if __name__ == '__main__':
    app.run(host='backend', port='5000', debug=True)
