#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main app entry point."""

import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy
from .models import db

db = SQLAlchemy()
login_manager = LoginManager()

# connect to a remote application
#oauth = OAuth(app)
oauth = OAuth()

twitter = oauth.remote_app(
    'twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    app_key='TWITTER'
)

def create_app(config_file=None):
    app = Flask(__name__, instance_relative_config=True)

    load_config(app, config_file)

    load_blueprints(app)
    
    #lm = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'index'

    # detect if we are just tweeting 
    tuit = os.getenv('MULTAVISO_TUIT')
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
    oauth.init_app(app)    

    db.app = app
    db.init_app(app)
    return app

def load_config(app, config_file):
    # load config
    app.config.from_object('config.default')
    if config_file is None and 'APP_CONFIG_FILE' in os.environ:
        app.config.from_envvar('APP_CONFIG_FILE')
    else:
        app.config.from_pyfile(config_file)
    
    ## load dotenv
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)

    # optionally have custom configurations in /instance/config.py
    # not git versioned
    app.config.from_pyfile('config.py', silent=True) 


def load_blueprints(app):
    """Load blueprints."""
    from .users.views import users_blueprint
    #from .oauth.views import oauth_blueprint
    from .pages.views import pages_blueprint

    app.register_blueprint(users_blueprint, url_prefix='/users')
    #app.register_blueprint(oauth_blueprint, url_prefix='/oauth')
    app.register_blueprint(pages_blueprint)
