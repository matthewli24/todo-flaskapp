from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create flask app
app = Flask(__name__)

#setting up db config
username = "todoflaskapp"
password = "todoflaskapp"
endpoint = "todoflaskapp-db.cejj8nvffgy6.us-east-1.rds.amazonaws.com"
db_instance_name = "todoflaskapp-db"
uri = 'mysql+pymysql://{}:{}@{}:3306/{}'.format(username, password, endpoint,db_instance_name)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = "super_secret_key"

db = SQLAlchemy(app)

from app import routes


