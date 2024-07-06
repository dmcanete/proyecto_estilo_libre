from flask import Flask
from app.visews import *
from app.database import init_app
#from flask_cors import CORS # type: ignore

app = Flask(__name__)

app.route('/',methods=['GET'])(index)
app.route('/api/clientes/',methods=['GET'])(get_all_clientes)
app.route('/api/clientes/',methods=['POST'])(create_cliente)
app.route('/api/clientes/<int:id_cliente>', methods=['GET'])(get_cliente)
app.route('/api/clientes/<int:id_cliente>', methods=['PUT'])(update_cliente)
app.route('/api/clientes/<int:id_cliente>', methods=['DELETE'])(delete_cliente)

if __name__== '__main__':
    app.run(debug=True)