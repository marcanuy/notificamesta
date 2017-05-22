from notificamesta import db
import datetime

class Radar(db.Model):
    #__tablename__ = 'radars'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(200), unique=True)
    nombre = db.Column(db.String(200), unique=True)
    latitud = db.Column(db.String(20))
    longitud = db.Column(db.String(20))
    contravenciones = db.relationship('Contravencion', backref='radar', lazy='select')
    
    def __init__(self, codigo, nombre, latitud, longitud):
        self.codigo = codigo
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        
