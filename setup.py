from setuptools import setup

setup(
    name='flask-my-extension',
    entry_points='''
        [flask.commands]
        bajarnotificaciones=notificamesta.multas.commands:bajar
    ''',
)
