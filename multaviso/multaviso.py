# coding: utf-8
from multaviso import app, twitter, db, lm
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from cgi import escape
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField
from wtforms.validators import DataRequired, Length
from flask_login import UserMixin, login_user, logout_user, current_user, login_required
import click
import urllib.request
from bs4 import BeautifulSoup
import datetime

def get_or_create_user(session, model, **kwargs):
    instance = session.query(model).filter_by(twitter_user_id=kwargs["twitter_user_id"]).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

class Notificacion(db.Model):
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True) #e.g.: 4-2016
    url = db.Column(db.String(200), unique=True)
    bajado = db.Column(db.DateTime)
    html = db.Column(db.Text)
    contravenciones = db.relationship('Contravencion', backref='notificacion',
                                lazy='select')

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

class UserForm(FlaskForm):
    matricula = StringField(u'Matricula', validators=[Length(min=3, max=10), DataRequired()])
    #email = StringField('Correo', validators=[Length(min=6, max=120)])
    #notify = BooleanField('Notificar por Twitter', default=True)

@lm.user_loader
def load_user(id):
    if id != "None":
        return User.query.get(int(id))

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@app.route('/usuario', methods=('GET', 'POST'))
@login_required
def usuario():
    form = UserForm()
    if form.validate_on_submit():
        db.session.query(User).filter_by(id=current_user.id).update({"matricula": form.matricula.data})
        db.session.commit()
        flash('Datos actualizados. A partir de ahora, si detectamos alguna multa por radar te avisamos con un tuit.')
    user = User.query.get(current_user.id)
    form.matricula.data = user.matricula
    return render_template('usuario.html', user=current_user, form=form)

# @app.route('/info')
# def info():
#     return render_template('info.html')
    
@app.route('/')
def index():
    #@todo mostrar datos usuario 
    # tweets = None
    # if g.user is not None:
    #     resp = twitter.request('statuses/home_timeline.json')
    #     if resp.status == 200:
    #         tweets = resp.data
    #     else:
    #         flash('Unable to load tweets from Twitter.')
    # return render_template('index.html', tweets=tweets)
    return render_template('index.html')


@app.route('/tweet', methods=['POST'])
def tweet():
    if g.user is None:
        return redirect(url_for('login', next=request.url))
    status = request.form['tweet']
    if not status:
        return redirect(url_for('index'))
    resp = twitter.post('statuses/update.json', data={
        'status': status
    })

    if resp.status == 403:
        flash("Error: #%d, %s " % (
            resp.data.get('errors')[0].get('code'),
            resp.data.get('errors')[0].get('message'))
        )
    elif resp.status == 401:
        flash('Authorization error with Twitter.')
    else:
        flash('Successfully tweeted your tweet (ID: #%s)' % resp.data['id'])
    return redirect(url_for('index'))

@app.cli.command()
def tuitear_multa():
    #tuit_multa("marcanuy", "prueba")
    with app.app_context():
         click.echo("entrooooooooooooooo")
         status = "Multa a"
         resp = twitter.post('statuses/update.json', data={
             'status': status
         })

         if resp.status == 403:
             click.echo("Error: #%d, %s " % (
                 resp.data.get('errors')[0].get('code'),
                 resp.data.get('errors')[0].get('message'))
             )
         elif resp.status == 401:
             click.echo('Authorization error with Twitter.')
         else:
             click.echo('Successfully tweeted your tweet (ID: #%s)' % resp.data['id'])

             

#oauth_authorize
@app.route('/login')
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('usuario'))
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    #session.pop('twitter_oauth', None)
    logout_user()
    return redirect(url_for('index'))

#oauth_callback
@app.route('/oauthorized')
def oauthorized():
    ### callback url
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    resp = twitter.authorized_response()
    if resp is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    session['twitter_oauth'] = resp
    user = User.query.filter_by(twitter_user_id=resp['user_id']).first()
    if not user:
        user = User(twitter_screen_name=resp['screen_name'], twitter_user_id=resp['user_id'])
        db.session.add(user)
        db.session.commit()
    login_user(user,True)
    return redirect(url_for('usuario'))

def numero_notificacion_nueva():
    ultima_notificacion = Notificacion.query.order_by('-numero').first()
    if ultima_notificacion is None:
        numero = 1
    else:
        numero = ultima_notificacion.numero + 1
    return numero

def pagina_notificaciones_tiene_datos(data):
    return b"NOTIFICACION POR CONTRAVENCION A NORMAS DE TRANSITO" in data


@app.cli.command()
def bajar():
    numero = numero_notificacion_nueva()
    click.echo('Buscando notificacion numero: %s-2016' % numero)
    procesar = True
    while(procesar):
        url='http://impo.com.uy/bases/notificaciones-cgm/%s-2016' % numero
        click.echo("Procesando: " + url)
        response = urllib.request.urlopen(url)
        data = response.read()
        
        if not pagina_notificaciones_tiene_datos(data):
            click.echo('El siguiente enlace todavia no contiene notificaciones: %s' % url)
            procesar = False
        else:
            fecha = datetime.datetime.now()
            notificacion = Notificacion(numero=numero, url=url, html=data, bajado=fecha)
            db.session.add(notificacion)
            #text = data.decode('utf-8')
            soup = BeautifulSoup(data, "html.parser")

            for tr in soup.find_all('tr')[1:]: # [1:] to skip the first row
                tds = tr.find_all('td')
                #print ("Matricula: %s, Fecha: %s, Interseccion: %s, Intervenido: %s, Articulo: %s, Valor UR: %s" %
                #      (tds[0].text, tds[1].text, tds[2].text, tds[3].text, tds[4].text, tds[5].text))
                matricula = tds[0].text.replace(" ", "")
                interseccion = tds[2].text
                intervenido = tds[3].text
                articulo = tds[4].text
                valor = tds[5].text
                date_string = tds[1].text
                try:
                    fecha = datetime.datetime.strptime(date_string, "%d/%m/%Y %H:%M")
                except ValueError:
                    fecha = None
                contravencion = Contravencion(notificacion, matricula, interseccion, intervenido, articulo, valor, fecha=fecha)
                db.session.add(contravencion)
            db.session.commit()
            numero += 1
            url='http://impo.com.uy/bases/notificaciones-cgm/%s-2016' % numero
            click.echo("Chequeando si %s tiene datos" % url)
            response = urllib.request.urlopen(url)
            data = response.read()

if __name__ == '__main__':
    app.run()
