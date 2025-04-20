from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

app.secret_key = 'password_tarreo25_app'
bcrypt = Bcrypt(app)