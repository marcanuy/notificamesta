#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""users/views.py: User views."""

from notificamesta import db
from flask import Blueprint, session, flash, redirect, url_for, render_template
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user
from .forms import UserForm
from .models import User


users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)

@users_blueprint.route('/logout')
@login_required
def logout():
    """Logout route."""
    logout_user()
    if 'oauth_token' in session:
        session.pop('oauth_token', None)
    flash('Sesión terminada', 'info')
    return redirect(url_for('pages.home'))

@users_blueprint.route('/', methods=('GET', 'POST'))
@login_required
def usuario():
    form = UserForm()
    if form.validate_on_submit():
        db.session.query(User).filter_by(id=current_user.id).update({"matricula": form.matricula.data})
        db.session.commit()
        flash('Datos actualizados. A partir de ahora, si detectamos alguna infraccion por radar de la matricula %s te avisamos por Twitter.' % current_user.matricula)
    print("user current_user: %s" % current_user)
    form.matricula.data = current_user.matricula
    #user=current_user
    return render_template('usuario.html', user=current_user, form=form)

@users_blueprint.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    form = UserForm()
    if form.validate_on_submit():
        db.session.query(User).filter_by(id=current_user.id).update({"matricula": form.matricula.data})
        db.session.commit()
        flash('Datos actualizados. A partir de ahora, si detectamos alguna infraccion por radar de la matricula %s te avisamos por Twitter.' % current_user.matricula)
        redirect(url_for('users.usuario'))
    form.matricula.data = current_user.matricula
    return render_template('edit.html', user=current_user, form=form)

