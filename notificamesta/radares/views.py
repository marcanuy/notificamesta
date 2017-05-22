#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""radares/views.py: Radares views."""

import click
from notificamesta import db
from notificamesta.multas.models import Contravencion
from notificamesta.radares.models import Radar
from flask import Blueprint, session, flash, redirect, url_for, render_template
from flask import current_app as app
#from .models import User


radares_blueprint = Blueprint(
    'radares', __name__,
    template_folder='templates'
)

@radares_blueprint.route('/<int:radar_id>', methods=['GET'])
def radar(radar_id):
    radar = Radar.query.get(radar_id)
    if radar == None:
        abort(404)
    return render_template('radar.html', radar=radar)


@radares_blueprint.route('/')
def data():
    sql="select * from (\
    Select count(interseccion) as\
    multas,interseccion from\
    contravencion group by interseccion order by multas desc) \
    as multaPorRadar order by multas desc limit 10"
    l = db.engine.execute(sql).fetchall()
    infraccionesPorRadar = [list(t) for t in zip(*l)]
    #pairs up the elements from all inputs
    #db.session.query(User).filter_by(id=current_user.id).update({"matricula": form.matricula.data})
    #return render_template('data.html', top5)
    maps_key=app.config['GOOGLE_MAPS_API_KEY']
    radares=Radar.query.all()
    return render_template('lista.html', lista=infraccionesPorRadar, google_maps_api_key=maps_key, radares=radares)
