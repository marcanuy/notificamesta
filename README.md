notificamⓔsta.uy
======

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/marcanuy/notificamesta/master/LICENSE)

NotificamⒺsta

# Environment Setup

    $ pip install -r requirements.txt
    $ export PYTHONPATH="/full/path/to/root/folder/"
    $ export FLASK_APP=notificamestaapp.py
	
Configure SQLAlchemy development database with
`DATABASE_URL` environment variable like:
`DATABASE_URL="postgresql://myuser:mypassword@localhost/mydatabase"`
and other custom environment variables located in `.env`

    $ cp .env.skel .env
  
Then we create the schema:

    $ flask shell
	>>> from notificamesta import db
    >>> db.create_all()


## Running local server

In the root folder:

    $ flask run
    * Serving Flask app "notificamesta.notificamesta"
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

## Testing

	$ python tests/test_notificamesta.py
	
# Pending

Get email from Twitter:

> Additional Permissions
> These additional permissions require that you provide URLs to your application or service's privacy policy and terms of service. You can configure these fields in your Application Settings.
> Request email addresses from users
> https://apps.twitter.com/app/*****/permissions

# Modules used

## Twitter oauth

[Twitter](https://dev.twitter.com/oauth)
uses [OAuth](https://oauth.net/) 1.0A so users are not required to
share their passwords with third party applications.

In OAuth 1.0A there are two forms of authentication:

- User authentication
  - is a form of authentication where your application makes API requests on end-users behalf
- Application-only authentication
  - is a form of authentication where your application makes API requests on its own behalf

> To make authorized calls to Twitter’s APIs, your application must
> first obtain an OAuth access token on behalf of a Twitter user (or,
> you could issue Application-only authenticated requests, when user
> context is not required).

To have a [sign-in button](https://dev.twitter.com/web/sign-in/implementing) tokens are obtained like this:

1. Obtain a **request token** (`oauth_token` and `oauth_token_secret`)
   also sending an `oauth_callback`
   - obtain a **request token** by sending a signed message
     to
     [https://api.twitter.com/oauth/request_token](https://api.twitter.com/oauth/request_token) with
     an `oauth_callback` parameter indicating where the user will be
     redirected in *Step 2*.
   - Check that the HTTP status of the response is 200 (success)
   - parameters returned:
	 - `oauth_token` (store for next step)
	 - `oauth_token_secret` (store for next step)
	 - `oauth_callback_confirmed` (verify it is true)
2. Redirect the user to Twitter including the `oauth_token`.
   - We need to direct the user to Twitter to complete sign in.
   - Redirect user with a GET
     to
     [https://api.twitter.com/oauth/authenticate](https://dev.twitter.com/oauth/reference/get/oauth/authenticate)
	 including the `oauth_token` parameter from *Step 1*. (Probably
     an HTTP 302 redirect)
	 - `GET oauth Authenticate` method differs from `GET oauth / authorize`
	   in that if the user has already granted the application
	   permission, the redirect will occur without the user having to
	   re-approve the application.
       - **To realize this behavior, you must enable the Use Sign in
		 with Twitter setting on your application record.** 
		 - `Allow this application to be used to Sign in with Twitter`
           checkbox
	 - The sign in endpoint can behave in three different ways
       depending on this status:
	   - **Signed in and approved**
		 - If the user:
		   - is signed in on twitter.com and
		   - has already approved the calling application
		 - then they will be immediately authenticated and returned to
           the callback URL with a valid OAuth *request token*
	   - **Signed in but not approved**
		 -  If the user:
			- is signed in to twitter.com **but**
			- has not approved the calling application
		 - then:
		   - a request to share access with the calling application
		   will be shown
		   - After accepting the authorization request
			 - the user will be redirected to the callback URL with a
               valid OAuth *request token*
	   - **Not signed in**
		 - If the user is not signed in on twitter.com
		 - then they will be prompted
		   - to enter their credentials and 
		   - grant access for the application to access their
		   information on the same screen. 
		 - Once signed in, 
		   - the user will be returned to the callback URL with a
             valid OAuth *request token*.
	 - Upon a successful authentication, your **callback_url** would
	 receive a request containing
		 - `oauth_token` and
		 - `oauth_verifier `
3. Convert the request token to an access token (Upgrade request token)
   - To render the **request token** into a usable **access token**:
	 - your application must make a request to the `POST oauth /
       access_token`
       endpoint
       [https://api.twitter.com/oauth/access_token](https://dev.twitter.com/oauth/reference/post/oauth/access_token),
       containing the `oauth_verifier` value obtained in step 2
	 - Twitter generates the **access token**
	 - Twitter response with
	   - `oauth_token`
	   - `oauth_token_secret`
	   - `user_id`
	   - `screen_name`
   - **The `token` and `token secret` should be stored and used for future authenticated requests to the Twitter API.**


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
