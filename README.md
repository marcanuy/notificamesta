
# Datos

## Consulta de infracciones

Fiscalización electrónica de infracciones de
tránsito
<http://www.montevideo.gub.uy/fiscalizacion-electronica-de-infracciones-de-transito>

### Cómo saber si me aplicaron una multa

> Para vehículos empadronados en Montevideo con domicilio registrado, se
> remitirán notificaciones y resoluciones a dicho domicilio por medio
> del Correo.
> 
> Para vehículos empadronados en Montevideo sin domicilio registrado,
> con domicilio incorrecto y vehículos empadronados en el interior del
> país, se publicarán notificaciones y resoluciones en la página web de
> IMPO.
> 
> Multas disponibles a partir de transcurridas 72 horas hábiles de
> cometida la infracción
> en <http://www.montevideo.gub.uy/consultainfracciones>.

> La visualización de archivos fotográficos no debe considerarse como
> notificación de multa por infracción. Los descargos o apelaciones no
> pueden presentarse hasta no recibir notificación formal por el Correo
> o en la web del Diario Oficial IMPO. 

# Commands

Config to load the application:

    $ export FLASK_APP=multaviso.py	
	$ export FLASK_DEBUG=1 #dev


## Testing

## Deploy local server


# Pendientes

- hacer modelo
  
  screen_name': 'marcanuy', 'user_id': '175838359', 
  twitter_screen_name, twitter_user_id, correo:'', matricula:''

- Para el deployment cambiar:
  - app.secret_key = 'development'
  - consumer_key
  - consumer_secret

- cambiar pedido de correo en configuracion de apps.twitter.com
  
> Additional Permissions
> These additional permissions require that you provide URLs to your application or service's privacy policy and terms of service. You can configure these fields in your Application Settings.
> Request email addresses from users
> https://apps.twitter.com/app/*****/permissions

# Modules used

## Twitter oauth

- <https://github.com/lepture/flask-oauthlib/>
  - <https://github.com/lepture/flask-oauthlib/blob/master/example/twitter.py>

## Database

- Flask-sqlalchemy <http://flask-sqlalchemy.pocoo.org/2.1/>
- SQLAlchemy in Flask <http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/>
  
## Testing

- unittest — Unit testing framework <https://docs.python.org/3.5/library/unittest.html>
- Flask-testing <https://pythonhosted.org/Flask-Testing/>
  - Utils.py TestCase <https://github.com/jarus/flask-testing/blob/master/flask_testing/utils.py>

# Resources

- Python 3 unittest <https://docs.python.org/3/library/unittest.html#module-unittest> 
- 
