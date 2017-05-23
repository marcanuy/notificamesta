#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""multas/views.py: Multas views."""

import click
from notificamesta import db
from notificamesta.multas.models import Contravencion
from flask import Blueprint, session, flash, redirect, url_for, render_template
#from .models import User
from flask import current_app as app
import json

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
    as multaPorRadar order by multas desc limit 5"
    l = db.engine.execute(sql).fetchall()
    infraccionesPorRadar = [list(t) for t in zip(*l)]
    #pairs up the elements from all inputs

    sql_tipo_multa = "select count(*), valor, trim(articulo) from contravencion where valor!=0 group by valor, trim(articulo)"
    l = db.engine.execute(sql_tipo_multa).fetchall()
    tipo_multa = [list(t) for t in zip(*l)]
    
    sql_multas_por_radar = "select * from (Select count(interseccion) as multas, r.latitud,r.longitud from contravencion as c \
    left join radar as r on r.id=c.radar_id \
    group by c.interseccion, r.id) as result where latitud!=''"
    multas_por_radar = db.engine.execute(sql_multas_por_radar).fetchall()

    sql_recaudado = "select sum(valor) from contravencion"
    recaudado_urs = db.engine.execute(sql_recaudado).fetchall()[0][0]
    print(recaudado_urs)
    print("---------------")
    unidad_reajustable = 988
    recaudado = recaudado_urs * unidad_reajustable
    print("recaudad")
    print(recaudado)
    #db.session.query(User).filter_by(id=current_user.id).update({"matricula": form.matricula.data})
    #return render_template('data.html', top5)
    maps_key=app.config['GOOGLE_MAPS_API_KEY']
    return render_template('data.html', lista=infraccionesPorRadar, google_maps_api_key=maps_key, multas_por_radar=multas_por_radar, recaudado=recaudado, tipo_multa=tipo_multa, unidad_reajustable=unidad_reajustable)
