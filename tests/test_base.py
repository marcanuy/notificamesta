import os
import unittest
import tempfile

import sys

from notificamesta import create_app, db
from flask_testing import TestCase # flask-testing
#from notificamesta.users.models import User

class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app('testing')
        return app

    def setUp(self):
        # Config a temporary database
        # mkstemp() returns a tuple containing an OS-level handle 
        # to an open file (as would be returned by os.open()) and
        # the absolute pathname of that file, in that order.

        self.db_fd, self.app.config['DATABASE'] = tempfile.mkstemp()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
           self.app.config['DATABASE']
        #self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///testing.sqlite3"

        #lm = LoginManager(self.app)
        #lm.login_view = 'index'
        db.drop_all()
        db.create_all()
        #self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_create_user_create_if_not_exists(self):
    #     user = User("tstname","12345")
    #     retrievedUser = User.query.filter_by(twitter_user_id=user.twitter_user_id).first()
    #     self.assertIsNone(retrievedUser)

    #     get_or_create_user(db.session, User, twitter_screen_name=user.twitter_screen_name, twitter_user_id=user.twitter_user_id)

    #     retrievedUser = User.query.filter_by(twitter_user_id=user.twitter_user_id).first()
    #     self.assertEqual(user.twitter_user_id, retrievedUser.twitter_user_id)

    # def test_create_user_create_retrieves_user(self):
    #     user = User("tstname","12345")
    #     retrievedUser = User.query.filter_by(twitter_user_id=user.twitter_user_id).first()
    #     self.assertIsNone(retrievedUser)

    #     get_or_create_user(db.session, User, twitter_screen_name=user.twitter_screen_name, twitter_user_id=user.twitter_user_id)

    #     retrievedUser = User.query.filter_by(twitter_user_id=user.twitter_user_id).first()
    #     self.assertEqual(user.twitter_user_id, retrievedUser.twitter_user_id)

    # def test_anonymous_user_cant_access_user_route(self):
    #     with app.test_request_context():
    #         user_path = url_for('usuario')
    #         expected_path = url_for('index')

    #         response = self.app.get(user_path, follow_redirects=False)

    #         #assert response.request.path == expected_path
    #         self.assertEqual(response.status_code, 302)
    #         self.assertEqual(urlparse(response.location).path, expected_path)

    # def test_anonymous_user_cant_access_logout_route(self):
    #     with app.test_request_context():
    #         logout_path = url_for('logout')
    #         expected_path = url_for('index')

    #         response = self.app.get(logout_path, follow_redirects=False)

    #         #assert response.request.path == expected_path
    #         self.assertEqual(response.status_code, 302)
    #         self.assertEqual(urlparse(response.location).path, expected_path)
        
    # # def test_logged_user_can_access_user_route(self):
    # #     #with app.test_request_context():
    # #     with self.app as app:
    # #         user = User("tstname","12345")
    # #         login_user(user,True)
    # #         print("is authenticated:")
    # #         print(user.is_authenticated)
    # #         print("current_user:")
    # #         print(current_user)
    # #         user_path = url_for('usuario')
    # #         expected_path = url_for('usuario')

    # #         response = self.app.get(user_path, follow_redirects=False)
    # #         print(dir(self.app))
    # #         #assert response.request.path == expected_path
    # #         self.assertEqual(response.status_code, 302)
    # #         self.assertEqual(urlparse(response.location).path, expected_path)        

    # def test_numero_notificacion_nueva_primera_vez(self):
    #     numero = numero_notificacion_nueva() 
    #     self.assertEqual(1, numero)

    # def test_numero_notificacion_nueva_con_datos(self):
    #     notificacion1 = Notificacion(numero=1,url="http://example.com/1",html="")
    #     notificacion2 = Notificacion(numero=2,url="http://example.com/2",html="")
    #     db.session.add(notificacion1)
    #     db.session.add(notificacion2)
    #     db.session.commit()
    #     expected_numero = 3

    #     numero = numero_notificacion_nueva()
        
    #     self.assertEqual(expected_numero, numero)

    # def test_multas_sin_tuitear_con_una_multa(self):
    #     matricula = "ABC1234"
    #     user=User(twitter_screen_name="foobar", twitter_user_id=1234,matricula=matricula)
    #     fecha_vieja= date(2015, 1, 5)
    #     user.created_at=fecha_vieja
    #     fecha_nueva = date(2016, 12, 8)
    #     noti=Notificacion(numero=1,url="",html="")
    #     cont=Contravencion(noti, fecha=fecha_nueva,matricula=matricula)
    #     db.session.add(user)
    #     db.session.add(cont)
        
    #     multas=user.multas_sin_tuitear()
    
    #     self.assertEqual(1,len(multas))

if __name__ == "__main__":
    unittest.main()
