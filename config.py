from flask import Flask
from flask import Blueprint
from mongoengine import connect

app = Flask(__name__)
app.debug = True


#app.config["MONGODB_SETTINGS"] = {'DB': "my_tumble_log"}
#app.config["SECRET_KEY"] = "KeepThisS3cr3t"

app.config["MONGODB_DB"] = 'app14403725'
connect(
    'app14403725',
    username='heroku',
    password='11adeea8b870f9f3e576bf7c8ffb1ee9',
    host='mongodb://heroku:11adeea8b870f9f3e576bf7c8ffb1ee9@linus.mongohq.com:10077/app14403725',
    port=10077
)


CSRF_ENABLED = True
SECRET_KEY = 'teddymonkey'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


###########################
### register blueprints ###
###########################
from disc_golf.views import index_page
app.register_blueprint(index_page)
