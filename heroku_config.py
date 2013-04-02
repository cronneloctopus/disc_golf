from flask import Flask
from mongoengine import connect

app = Flask(__name__)
app.debug = True

app.config["MONGODB_DB"] = 'app14198794'
connect(
    'app14198794',
    username='heroku',
    password='a614e68b445d0d9d1c375740781073b4',
    host='mongodb://heroku:a614e68b445d0d9d1c375740781073b4@alex.mongohq.com:10095/app14198794',
    port=10095
)
