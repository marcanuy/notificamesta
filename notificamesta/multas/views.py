#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""multas/views.py: Multas views."""

import click
from notificamesta import db
from notificamesta.multas.models import Contravencion
from flask import Blueprint, session, flash, redirect, url_for, render_template
#from .models import User


multas_blueprint = Blueprint(
    'multas', __name__,
    template_folder='templates'
)

@multas_blueprint.route('/')
def data():
    sql="select * from (\
    Select count(interseccion) as\
    multas,interseccion from\
    contravencion group by interseccion order by multas desc) \
    as multaPorRadar order by multas desc limit 10"
    l = db.engine.execute(sql).fetchall()
    infraccionesPorRadar = [list(t) for t in zip(*l)]
    #pairs up the elements from all inputs
    print(infraccionesPorRadar)



    #db.session.query(User).filter_by(id=current_user.id).update({"matricula": form.matricula.data})
    #return render_template('data.html', top5)
    return render_template('data.html', lista=infraccionesPorRadar)
