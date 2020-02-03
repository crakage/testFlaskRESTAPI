from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqllite:///Users/dvoillemin/PycharmProjects/testFlaskRESTAPI/database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

