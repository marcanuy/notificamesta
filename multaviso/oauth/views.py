from .model import OAuthSignIn
from flask import redirect, url_for, request, flash, Blueprint, session

oauth_blueprint = Blueprint(
    'oauth', __name__,
    template_folder='templates'
)


@oauth_blueprint.route('/login/<provider>')
def login(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@oauth_blueprint.route('/authorized/<provider>')
def authorized(provider):
    oauth = OAuthSignIn.get_provider(provider)
    resp = oauth.authorized_response()
    next_url = request.args.get('next') or url_for('users.usuario')
    if resp is None:
        flash('No pudimos iniciarte una sesión', 'error')
        return redirect(url_for('pages.home'))
    session['oauth_token'] = oauth.get_session_data(resp)[0]
    oauth.get_user(resp)
    return redirect(next_url)


@oauth_blueprint.route("/logout")
def logout():
    session.pop('oauth_token', None)
    return redirect(url_for('pages.home'))



