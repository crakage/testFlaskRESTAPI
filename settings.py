from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/crakage/PycharmProjects/webAPI/db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

