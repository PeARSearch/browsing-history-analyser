from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


class OpenVectors(db.Model):
    __bind_key__ = 'openvectors'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.UnicodeText(64))
    vector = db.Column(db.Text)
