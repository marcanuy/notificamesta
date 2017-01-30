#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""users/views.py: User views."""

from multaviso import db
from flask import Blueprint
from flask_login import login_required

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


@users_blueprint.route('/', methods=('GET', 'POST'))
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
