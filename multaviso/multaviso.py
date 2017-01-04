# coding: utf-8

import os
from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth
from cgi import escape

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

# sqlachemy config
db_path = os.path.join(app.root_path, 'multaviso.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

oauth = OAuth(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key='nRSyCSSNoCPpzdBeImxsm63uR',
    consumer_secret='QzQyfm9Rkv0Ml3tFGF2wP73HmN3zFUiE7JGYwNT37F3OcYwQtQ',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)

def get_or_create_user(session, model, **kwargs):
    instance = session.query(model).filter_by('twitter_user_id').first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitter_screen_name = db.Column(db.String(20), unique=True)
    twitter_user_id = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    matricula = db.Column(db.String(10), unique=True)

    def __init__(self, twitter_screen_name, twitter_user_id, email="", matricula=""):
        self.twitter_screen_name = twitter_screen_name
        self.twitter_user_id = twitter_user_id
        self.email = email
        self.matricula = matricula

    def __repr__(self):
        return '<Usuario %r>' % escape(self.twitter_screen_name)

class UserForm(FlaskForm):
    matricula = StringField('Matricula', validators=[Length(min=3, max=10)])
    email = StringField('Correo', validators=[Length(min=6, max=120)])
    notify = BooleanField('Notificar por Twitter', validators=[DataRequired()])

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.before_request
def before_request():
    g.user = None
    if 'twitter_oauth' in session:
        g.user = session['twitter_oauth']

@app.route('/usuario', methods=('GET', 'POST'))
def usuario():
    print("entro en usuario")
    form = UserForm()
    print("genero form")
    if g.user is None:
        return redirect(url_for('login', next=request.url))
    if form.validate_on_submit():
        print("entro en validate")
        user = User.query.filter_by(twitter_user_id=g.user['user_id']).first()
        user.matricula = form.matricula.data
        user.email = form.email.data
        print(user)
        db.session.commit()
        print("paso el commit")
        flash('Datos actualizados.')
    return render_template('usuario.html', user=g.user, form=form)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = UserForm(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form.username.data, form.email.data,
#                     form.password.data)
#         db_session.add(user)
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)


@app.route('/')
def index():
    tweets = None
    if g.user is not None:
        resp = twitter.request('statuses/home_timeline.json')
        if resp.status == 200:
            tweets = resp.data
        else:
            flash('Unable to load tweets from Twitter.')
    return render_template('index.html', tweets=tweets)


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


@app.route('/login')
def login():
    callback_url = url_for('oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referrer or None)


@app.route('/logout')
def logout():
    session.pop('twitter_oauth', None)
    return redirect(url_for('index'))


@app.route('/oauthorized')
def oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
        user = get_or_create(db.session,
                             User,
                             twitter_screen_name=resp['screen_name'],
                             twitter_user_id=resp['user_id'])
    return redirect(url_for('usuario'))


if __name__ == '__main__':
    app.run()
