from flask import Flask
from flask import render_template, jsonify, request, redirect, url_for
import json
from connectiondb import connect_db, get_kylo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



@app.route('/', methods=['GET'])
def index():
    """Retorna la pagina index."""
    print("OK")
    if(request.method == 'GET'):
        print("get")
        valor = get_kylo()
    return jsonify(valor = str(valor))


@app.route('/about')
def about():
    """Retorna la pagina about."""
    return render_template('/about.html', msj="About de la pagina")



if __name__ == '__main__':
    app.run(host='backend', port='5000', debug=True)