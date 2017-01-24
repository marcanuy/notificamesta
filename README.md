Multaviso
======

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/marcanuy/multaviso/master/LICENSE)

NotificamⒺsta

# Environment Setup

    $ pip install -r requirements.txt
    $ export FLASK_APP=multaviso/multaviso.py
	
For developing we need to load the **full path** of the configuration
file `config/development.py` in the `APP_CONFIG_FILE` environment
variable.

    $ export APP_CONFIG_FILE=$(realpath config/development.py)

Configure SQLAlchemy development database with
`SQLALCHEMY_DATABASE_URI` environment variable: 

You can configure a PostgreSQL local database in
  `/instance/config.py` setting the `SQLALCHEMY_DATABASE_URI`
  environment variable like: `SQLALCHEMY_DATABASE_URI =
  'postgresql://myuser:mypassword@localhost/mydatabase'`.
  
If you don't specify anything, then it will look for a sqlite3
database: `multaviso/development.sqlite3` as specified in
`config/development.py`:

Then we create the schema:

    $ flask shell
	>>> from multaviso import db
    >>> db.create_all()


## Running local server

In the root folder:

    $ flask run
    * Serving Flask app "multaviso.multaviso"
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

## Testing

	$ python tests/test_multaviso.py
	
# Pendientes

- hacer modelo
  
  screen_name': 'marcanuy', 'user_id': '175838359', 
  twitter_screen_name, twitter_user_id, correo:'', matricula:''

- Para el deployment cambiar:
  - app.secret_key = 'development'
  - consumer_key
  - consumer_secret

- cambiar pedido de correo en configuracion de apps.twitter.com
  
> Additional Permissions
> These additional permissions require that you provide URLs to your application or service's privacy policy and terms of service. You can configure these fields in your Application Settings.
> Request email addresses from users
> https://apps.twitter.com/app/*****/permissions

# Modules used

## Twitter oauth

### flask-oauthlib

- <http://flask-oauthlib.readthedocs.io/en/latest/index.html>
  Flask-OAuthlib is designed to be a replacement for Flask-OAuth
  
- <https://github.com/lepture/flask-oauthlib/>
  - <https://github.com/lepture/flask-oauthlib/blob/master/example/twitter.py>

### Login flow

1. route '/' index
2. login button -> route '/login' login
3. twitter.authorize 
4. route 'oauthorized'  next=..
5. https://api.twitter.com/oauth/authorize

## Database

- Flask-sqlalchemy <http://flask-sqlalchemy.pocoo.org/2.1/>
- SQLAlchemy in Flask <http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/>
  
## Testing

- unittest — Unit testing framework <https://docs.python.org/3.5/library/unittest.html>
- Flask-testing <https://pythonhosted.org/Flask-Testing/>
  - Utils.py TestCase <https://github.com/jarus/flask-testing/blob/master/flask_testing/utils.py>

# Resources

- Python 3 unittest <https://docs.python.org/3/library/unittest.html#module-unittest> 
- 

# License

MIT licensed.
