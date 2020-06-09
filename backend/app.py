from flask import Flask
from flask import render_template, jsonify, request, redirect, url_for
import json
from connectiondb import crear_usuarios
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
        return user

@app.route('/get_user', methods=['POST'])
def get():
    try:
        name = request.json["name"]
        user = get_user(name)
        return jsonify (user)
    except (Exception) as err:
        return str(err), 500


@app.route('/about')
def about():
    """Retorna la pagina about."""
    return render_template('/about.html', msj="About de la pagina")



if __name__ == '__main__':
    app.run(host='backend', port='5000', debug=True)