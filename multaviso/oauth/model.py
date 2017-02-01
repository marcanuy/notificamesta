from flask import url_for, session
from flask_oauthlib.client import OAuth
from flask_login import login_user
from multaviso.users.models import User
from multaviso import db

class OAuthSignIn():

    oauth = None
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name

    def authorize(self):
        return self.service.authorize(self.get_callback_url())

    def authorized_response(self):
        return self.service.authorized_response()

    def get_callback_url(self):
        return url_for('oauth.authorized', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        """
        Returns an instance of the provider subclass
        """
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]

    @staticmethod
    def get_token(token=None):
        return session.get('oauth_token')

    def get_session_data(self, data):
        pass

    def get_user_data(self):
        return None

class TwitterSignIn(OAuthSignIn):

    def __init__(self):
        super().__init__('twitter')
        #self.oauth = OAuth()
        self.oauth = OAuth()
        self.service = self.oauth.remote_app(
            'twitter',
            base_url='https://api.twitter.com/1/',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            app_key='TWITTER',
            #consumer_key=app.config['TWITTER_CUSTOMER_KEY'],
            #consumer_secret=app.config['TWITTER_CUSTOMER_SECRET']
        )
        self.service.tokengetter = TwitterSignIn.get_token

    def get_session_data(self, data):
        """
        Returns token data from response to save in session
        e.g. to keep an authorized login: 
        session['oauth_token'] = oauth.get_session_data(resp)
        """
        print("data: %s" % data)
        return (
            data['oauth_token'],
            data['oauth_token_secret']
        )

    def get_user_data(self, data=None):
        """
        Returns user data sent from Twitter in response
        """
        if data is None:
            return (
                session.get('user_id'),
                session.get('screen_name')
            )
        else:
            return (
                data['user_id'],
                data['screen_name']
            )
    
    def get_user(self, data=None):
        print(self.get_user_data(data))
        user_id, screen_name = self.get_user_data(data)
        print("userid: %s" % user_id)
        user = User.query.filter_by(twitter_user_id=user_id).first()
        if user is None:
            user = User(twitter_user_id=user_id,
                        twitter_screen_name=screen_name,
                        token=session.get('oauth_token'))
            db.session.add(user)
            db.session.commit()

        login_user(user)
