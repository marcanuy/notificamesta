# SQLAlchemy database
MULTAVISO_DATABASE = "production.sqlite3"
db_path = os.path.join(app.root_path, MULTAVISO_DATABASE)
db_uri = 'sqlite:///{}'.format(db_path)
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG=False
FLASK_DEBUG=False
SQLALCHEMY_ECHO = False
