#!/usr/bin/env python
import os
from flask.ext.mongoengine import MongoEngine
from config import app


app.config['SECRET_KEY'] = 'teddymonkey'


# get config settings
if __name__ == '__main__':
    app.config.from_object('config')
else:
    app.config.from_object('heroku_config')


# instantiate mongengine
db = MongoEngine(app)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.debug = True

    """
    # add flask debug toolbar
    import flask_debugtoolbar

    # Specify the debug panels you want
    app.config['DEBUG_TB_PANELS'] = [
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        # Add the MongoDB panel
        'flask_debugtoolbar_mongo.panel.MongoDebugPanel',
    ]
    toolbar = flask_debugtoolbar.DebugToolbarExtension(app)
    """

    app.run(host='0.0.0.0', port=port)
