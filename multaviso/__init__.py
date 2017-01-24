import os
from flask import Flask
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.default')
app.config.from_envvar('APP_CONFIG_FILE')
# optionally have custom configurations in /instance/config.py
# not git versioned
app.config.from_pyfile('config.py', silent=True) 




# sqlachemy config
db = SQLAlchemy(app)

lm = LoginManager(app)
lm.login_view = 'index'

# detect if we are just tweeting 
tuit = os.getenv('MULTAVISO_TUIT')

oauth = OAuth(app)
# connect to a remote application
twitter=None
if tuit=="True":
    twitter = oauth.remote_app(
        'twitter',
        consumer_key = os.getenv('TWITTER_NOTIFY_CONSUMER_KEY', app.config['TWITTER_NOTIFY_CONSUMER_KEY']),
        consumer_secret = os.getenv('TWITTER_NOTIFY_CONSUMER_SECRET', app.config['TWITTER_NOTIFY_CONSUMER_SECRET']),
        base_url = app.config['TWITTER_BASE_URL'], #prefixed to all relative URLs used in the remote app
        request_token_url = app.config['TWITTER_REQUEST_TOKEN_URL'],
        access_token_url = app.config['TWITTER_ACCESS_TOKEN_URL'],
        authorize_url = app.config['TWITTER_AUTHORIZE_URL']
    )
else:
    twitter = oauth.remote_app(
        'twitter',
        consumer_key = os.getenv('TWITTER_CONSUMER_KEY', app.config['TWITTER_CONSUMER_KEY']),
        consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET', app.config['TWITTER_CONSUMER_SECRET']),
        base_url = app.config['TWITTER_BASE_URL'], #prefixed to all relative URLs used in the remote app
        request_token_url = app.config['TWITTER_REQUEST_TOKEN_URL'],
        access_token_url = app.config['TWITTER_ACCESS_TOKEN_URL'],
        authorize_url = app.config['TWITTER_AUTHORIZE_URL']
    )
    

