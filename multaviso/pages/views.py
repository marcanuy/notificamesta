from multaviso import db
from flask import Blueprint
from flask import render_template

pages_blueprint = Blueprint(
    'pages', __name__,
    template_folder='templates'
)

    
@pages_blueprint.route('/')
def home():
    #@todo mostrar datos usuario 
    # tweets = None
    # if g.user is not None:
    #     resp = twitter.request('statuses/home_timeline.json')
    #     if resp.status == 200:
    #         tweets = resp.data
    #     else:
    #         flash('Unable to load tweets from Twitter.')
    # return render_template('index.html', tweets=tweets)
    return render_template('home.html')
