from notificamesta import db
from flask_login import UserMixin
import datetime
from notificamesta.multas.models import Contravencion

class User(UserMixin, db.Model):

    """User model."""

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    # social_id = db.Column(db.String(64), nullable=False, unique=True)
    # nickname = db.Column(db.String(64), nullable=False)
#    email = db.Column(db.String(120), nullable=True)
    twitter_screen_name = db.Column(db.String(20), unique=True, nullable=True)
    twitter_user_id = db.Column(db.String(64), unique=True)
    oauth_token = db.Column(db.String(100), nullable=True)
    matricula = db.Column(db.String(10), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, twitter_user_id, twitter_screen_name=None, matricula=None, token=None):
#        self.twitter_screen_name = twitter_screen_name
        self.twitter_user_id = twitter_user_id
        self.twitter_screen_name = twitter_screen_name
        self.oauth_token = token
#        self.email = email
        self.matricula = matricula
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Usuario %r>' % escape(self.twitter_user_id)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def is_authenticated(self):
        """User validated if account has been confirmed."""
        return True

    def is_active(self):
        """All users are automatically active."""
        if self.token is None:
            return True
        return False

    def is_anonymous(self):
        """No anonymous users."""
        return False

    def get_id(self):
        """Make sure id returned is unicode."""
        return self.id

    def __repr__(self):
        """Representation."""
        return '<user {}>'.format(self.twitter_user_id)

    @property
    def multas(self):
        multas = Contravencion.query.filter_by(matricula=self.matricula).all()
        return multas

    # def multas_sin_tuitear(self):
    #     """ obtener las multas que no se hayan tuiteado y que sean mas nuevas que la fecha de creado el usuario en el sitema """
    #     multas = Contravencion.query.filter(Contravencion.matricula==self.matricula) \
    #                                 .filter(Contravencion.tuiteado==False) \
    #                                 .filter(Contravencion.fecha>self.created_at) \
    #                                 .all()
    #     return multas
