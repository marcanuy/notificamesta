# coding: utf-8

import click
import datetime
import urllib.request
from bs4 import BeautifulSoup
from cgi import escape
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import Form, BooleanField, StringField
from wtforms.validators import DataRequired, Length

# def get_or_create_user(session, model, **kwargs):
#     instance = session.query(model).filter_by(twitter_user_id=kwargs["twitter_user_id"]).first()
#     if instance:
#         return instance
#     else:
#         instance = model(**kwargs)
#         session.add(instance)
#         session.commit()
#         return instance

class UserForm(FlaskForm):
    matricula = StringField(u'Matricula', validators=[Length(min=3, max=10), DataRequired()])
    #email = StringField('Correo', validators=[Length(min=6, max=120)])
    #notify = BooleanField('Notificar por Twitter', default=True)

@login_manager.user_loader
def load_user(id):
    if id != "None":
        return User.query.get(int(id))

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


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
    ultima_notificacion = Notificacion.query.order_by(desc('numero')).first()
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

# if __name__ == '__main__':
#     app.run()
