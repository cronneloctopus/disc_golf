#!/usr/bin/env python
import os
from flask.ext.mongoengine import MongoEngine
from flask import Flask
from config import app
#app = Flask(__name__)
#app.debug = True


# get config settings
if __name__ == '__main__':
    app.config.from_object('config')
else:
    app.config.from_object('heroku_config')

# wrapp app in mongengine
db = MongoEngine(app)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
