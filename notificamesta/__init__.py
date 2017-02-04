#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main app entry point."""

import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

# connect to a remote application
#oauth = OAuth()

# import OAuthSign after initializing db
from notificamesta.oauth.model import OAuthSignIn
twitter = OAuthSignIn.get_provider('twitter')

def create_app(env_type=None):
    app = Flask(__name__, instance_relative_config=True)

    load_config(app, env_type)

    db.init_app(app)

    load_blueprints(app)
    
    login_manager.init_app(app)

    # detect if we are just tweeting 
    tuit = os.getenv('NOTIFICAMESTA_TUIT')
    if tuit=="True":
        app.config['TWITTER'] = {
            'consumer_key': os.getenv('TWITTER_NOTIFY_CONSUMER_KEY'),
            'consumer_secret': os.getenv('TWITTER_NOTIFY_CONSUMER_SECRET'),
        }
    else:
        app.config['TWITTER'] = {
            'consumer_key': os.getenv('TWITTER_CONSUMER_KEY'),
            'consumer_secret': os.getenv('TWITTER_CONSUMER_SECRET'),
        }
    app.config.secret_key = os.getenv('SECRET_KEY')
    #twitter.get_oauth()
    #print(twitter.service)
    twitter.oauth.init_app(app)    
    

    return app

def load_config(app, env_type):
    """
    

    Config load order:
    1. Load environment variables: /.env
    2. Load in app.config
      1. /config/default.py
      2. environment type:
         - testing
         - development
         - production
      3. /instance/config.py #optional
    """
    ## load environment variables from .env (dotenv)
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
    
    ## load default config
    app.config.from_object('config.default')
    ## load the environment dependent config

    config_path = os.path.join(APP_ROOT, 'config')    
    if env_type is "testing":
        app.config.from_pyfile( os.path.join(config_path, "testing.py") )
    elif env_type is "development":
        app.config.from_pyfile( os.path.join(config_path, "development.py") )
    elif env_type is "production":
        app.config.from_pyfile( os.path.join(config_path, "production.py") )
    else:
        print("Wrong environment, you need to specify a configuration file when calling create_app.")
    # if config_file is None and 'APP_CONFIG_FILE' in os.environ:
    #     app.config.from_envvar('APP_CONFIG_FILE')
    # else:
    #     app.config.from_pyfile(config_file)
    


    # optionally have custom configurations in /instance/config.py
    # not git versioned
    app.config.from_pyfile('config.py', silent=True) 


def load_blueprints(app):
    """Load blueprints."""
    from .users.views import users_blueprint
    from .oauth.views import oauth_blueprint
    from .pages.views import pages_blueprint

    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(oauth_blueprint, url_prefix='/oauth')
    app.register_blueprint(pages_blueprint)

from notificamesta.users.models import User

login_manager.login_view = 'pages.home'
login_manager.login_message = "Tenés que estar registrado para ver esta página, podes entrar con Twitter."
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(user_id):
    """Load the logged in user for the LoginManager."""
    return User.query.filter(User.id == int(user_id)).first()
