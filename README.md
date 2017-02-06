notificamⓔsta.uy
======

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/marcanuy/notificamesta/master/LICENSE)

NotificamⒺsta is built with [Flask](http://flask.pocoo.org/), a Python framework for web applications.

# Contributing

factory_boy is distributed under the MIT License.

Issues should be opened through [GitHub Issues](http://github.com/marcanuy/notificamesta/issues/); whenever possible, a pull request should be included.
Questions and suggestions are welcome.

# Local Environment

    $ pip install -r requirements.txt
    $ export PYTHONPATH="/full/path/to/root/folder/"
	
Configure SQLAlchemy development database with
`DATABASE_URL` environment variable like:
`DATABASE_URL="postgresql://myuser:mypassword@localhost/mydatabase"`
and other custom environment variables located in `.env`

    $ cp .env.skel .env
  
Then create the schema:

    $ flask shell
	>>> from notificamesta import db
    >>> db.create_all()

Use `shell.sh` to run a flask shell with the proper contexts and
`devserver.sh` for a development server.

# License

MIT licensed.
