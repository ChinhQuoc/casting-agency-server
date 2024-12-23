from flask import Flask
from .models import setup_db
from flask_cors import CORS
from .settings import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
setup_db(app)
CORS(app)

from app import routes