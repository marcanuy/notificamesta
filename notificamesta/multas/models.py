from notificamesta import db
import datetime

class Notificacion(db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True) #e.g.: 4-2016
    url = db.Column(db.String(200), unique=True)
    bajado = db.Column(db.DateTime)
    html = db.Column(db.Text)
    contravenciones = db.relationship('Contravencion', backref='notificacion', lazy='select')

    def __init__(self, numero, url, html, bajado=None):
        self.numero = numero
        self.url = url
        self.bajado = bajado
        if bajado is None:
            self.bajado = datetime.datetime.utcnow()
        else:
            self.bajado = bajado
        self.html = html
        
class Contravencion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(15))
    fecha = db.Column(db.DateTime, nullable=True)
    interseccion = db.Column(db.String(300), nullable=True)
    intervenido = db.Column(db.String(200), nullable=True)
    articulo = db.Column(db.String(200), nullable=True)
    valor = db.Column(db.Integer, nullable=True)
    tuiteado = db.Column(db.Boolean, unique=False, default=False)
    
    notificacion_id = db.Column(db.Integer, db.ForeignKey('notificacion.id'))
    #notificacion = db.relationship('Notificacion',
    #                                   backref=db.backref('contravencion', lazy='dynamic'))

    def __init__(self, notificacion, matricula="", interseccion="", intervenido="", articulo="", valor=0, fecha=None):
        self.matricula=matricula
        if fecha is None:
            self.fecha = datetime.datetime.utcnow()
        else:
            self.fecha = fecha
        self.interseccion = interseccion
        self.intervenido = intervenido
        self.articulo = articulo
        if valor is '':
            self.valor = 0
        else:
            self.valor = valor
        self.notificacion = notificacion


