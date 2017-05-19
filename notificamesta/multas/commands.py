#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""multas/views.py: Multas views."""

import click
import datetime
from notificamesta import db, create_app
from .models import Notificacion, Contravencion
from sqlalchemy import desc
import urllib.request
from bs4 import BeautifulSoup
from cgi import escape
from datetime import date

def _numero_notificacion_nueva():
    ultima_notificacion = Notificacion.query.order_by(desc('numero')).first()
    if ultima_notificacion is None:
        numero = 1
    else:
        numero = ultima_notificacion.numero + 1
    return numero

def _pagina_notificaciones_tiene_datos(data):
    return b"NOTIFICACION POR CONTRAVENCION A NORMAS DE TRANSITO" in data

@click.command()
def bajar():
    """
    Run the application
    """
    app = create_app('development')
    with app.app_context():
        numero = _numero_notificacion_nueva()
        current_year = date.today().year
        click.echo('Buscando notificacion numero: {}-{}'.format(numero,current_year))
        procesar = True
        while(procesar):
            url='http://impo.com.uy/bases/notificaciones-cgm/{}-{}'.format(numero,current_year)
            click.echo("Procesando: " + url)
            response = urllib.request.urlopen(url)
            data = response.read()

            if not _pagina_notificaciones_tiene_datos(data):
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
                url='http://impo.com.uy/bases/notificaciones-cgm/{}-{}'.format(numero,current_year)
                click.echo("Chequeando si %s tiene datos" % url)
                response = urllib.request.urlopen(url)
                data = response.read()

                
