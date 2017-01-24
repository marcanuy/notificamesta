import os

FLASK_DEBUG=1
SECRET_KEY="development"

# SQLAlchemy database
MULTAVISO_DATABASE = "development.sqlite3"
db_path = MULTAVISO_DATABASE
db_uri = 'sqlite:///{}'.format(db_path)
#SQLALCHEMY_DATABASE_URI = db_uri

SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_ECHO = False
DEBUG = True
