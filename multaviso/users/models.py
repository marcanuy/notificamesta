from multaviso import db
from multaviso import Contravencion

class User(UserMixin, db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # social_id = db.Column(db.String(64), nullable=False, unique=True)
    # nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    twitter_screen_name = db.Column(db.String(20), unique=True)
    twitter_user_id = db.Column(db.String(64), unique=True)
    matricula = db.Column(db.String(10), unique=True)
    created_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, twitter_screen_name, twitter_user_id, email="", matricula=""):
        self.twitter_screen_name = twitter_screen_name
        self.twitter_user_id = twitter_user_id
        self.email = email
        self.matricula = matricula
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Usuario %r>' % escape(self.twitter_screen_name)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    @property
    def multas(self):
        multas = Contravencion.query.filter_by(matricula=self.matricula).all()
        return multas

    def multas_sin_tuitear(self):
        """ obtener las multas que no se hayan tuiteado y que sean mas nuevas que la fecha de creado el usuario en el sitema """
        multas = Contravencion.query.filter(Contravencion.matricula==self.matricula) \
                                    .filter(Contravencion.tuiteado==False) \
                                    .filter(Contravencion.fecha>self.created_at) \
                                    .all()
        return multas
