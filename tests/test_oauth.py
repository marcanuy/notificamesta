#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for oauth module."""

import unittest
from mock import patch
from mock import MagicMock
from flask_oauthlib.client import OAuthRemoteApp
from tests.test_base import BaseTestCase
from flask import url_for, session
from notificamesta import create_app, db
from notificamesta.oauth.model import OAuthSignIn
from notificamesta.users.models import User
from flask_login import current_user

class OauthTestCase(BaseTestCase):

    def test_twitter_subclass(self):
        oauth = OAuthSignIn.get_provider('twitter')
        self.assertEqual('TwitterSignIn', oauth.__class__.__name__)

    def test_twitter_get_callback_url(self):
        oauth = OAuthSignIn.get_provider('twitter')
        self.assertEqual(
            url_for('oauth.authorized', provider='twitter', _external=True),
            oauth.get_callback_url()
        )

    @patch.object(OAuthRemoteApp, 'authorized_response')
    def test_authorized_response(self, authorized_response_mock):
        """ OauthSignIn.authorized_response() should return a dict """
        authorized_response_mock.return_value = {'test': 'dict'}
        oauth = OAuthSignIn.get_provider('twitter')
        response = oauth.authorized_response()
        self.assertEqual({'test': 'dict'}, response)

    def test_get_token(self):
        """ 
        OAuthSignIn.get_token() should return the oauth_token key in
        current session dict 
        """
        session['oauth_token'] = 'test token'
        self.assertEqual('test token', OAuthSignIn.get_token())

    # def test_twitter_authorize(self):
    #     oauth = OAuthSignIn.get_provider('twitter')
    #     response = oauth.authorize()
    #     self.assertEqual(302, response.status_code)

    def test_oauth_login_route_redirects_to_twitter(self):
        response = self.client.get(
            url_for('oauth.login', provider='twitter'),
            follow_redirects=False
        )
        self.assertIn('twitter', response.location)

    def test_get_session_data(self):
        oauth = OAuthSignIn.get_provider('twitter')
        data = {'oauth_token': 'test',
                'oauth_token_secret': 'secret'}
        session_data = oauth.get_session_data(data)
        self.assertEqual(('test', 'secret'), session_data)
        
    def test_get_twitter_user_data(self):
        test_id, test_name = '1234', 'marcanuy'
        oauth = OAuthSignIn.get_provider('twitter')
        data = {'user_id': test_id,
                'screen_name': test_name}
        #session['oauth_token'] = 'test'

        user_data = oauth.get_user_data(data)

        self.assertEqual((test_id, test_name), user_data)

    def test_get_user_creates_new_and_logs_in(self):
        # check user does not exists
        test_user_id = '1234'
        user = User.query.filter_by(twitter_user_id=test_user_id).first()
        self.assertIsNone(user)

        session['oauth_token'] = 'test'
        session['user_id'] = test_user_id
        session['screen_name'] = 'foobar'
        oauth = OAuthSignIn.get_provider('twitter')
        oauth.get_user()
        user = User.query.filter_by(twitter_user_id=test_user_id).first()
        self.assertTrue(user)
        self.assertTrue(current_user.is_authenticated)

    @patch.object(OAuthRemoteApp, 'get')
    def test_get_user_logins_in(self, get_mock):
        test_user_id='1234'
        test_screen_name='foobar'
        user = User(twitter_user_id=test_user_id,
                    twitter_screen_name=test_screen_name)
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = test_user_id
        session['screen_name'] = test_screen_name
        session['oauth_token'] = 'test'

        oauth = OAuthSignIn.get_provider('twitter')
        oauth.get_user()
        self.assertTrue(current_user.is_authenticated)

    @patch.object(OAuthRemoteApp, 'authorized_response')
    def test_authorized_can_log_in(self, authorized_response_mock):
        test_user_id='1234'
        test_screen_name='jr'
        authorized_response_mock.return_value = {
            'user_id':test_user_id,
            'screen_name': test_screen_name,
            'oauth_token': 'test',
            'oauth_token_secret': 'secret'
        }

        with self.client:
            response = self.client.get(
                url_for('oauth.authorized', provider='twitter'),
                follow_redirects=True
            )
            self.assertRedirects(response, url_for('pages.home'))

    @patch.object(OAuthRemoteApp, 'authorized_response')
    def test_cant_log_in(self, authorized_response_mock):
        authorized_response_mock.return_value = None

        with self.client:
            response = self.client.get(
                url_for('oauth.authorized', provider='twitter'),
                follow_redirects=True
            )
            self.assertIn('No pudimos iniciarte una sesión',
                          str(response.data.decode('utf8')))

    def test_logout(self):
        with self.client:
            session['oauth_token'] = 'test token'
            self.client.get(url_for('oauth.logout'))
            self.assertNotIn('auth_token', session)

    # @patch.object(OAuthRemoteApp, 'get')
    # def test_is_google_in_db(self, get_mock):

    #     get_mock.return_value = mock_get_response = MagicMock()
    #     mock_get_response.data = {'name': 'Test Name',
    #                               'email': 'test@gmail.com'}
    #     session['oauth_token'] = 'test'

    #     oauth = OAuthSignIn.get_provider('google')
    #     oauth.get_user()
    #     user = User.query.filter_by(email='test@gmail.com').first()
    #     self.assertTrue(user.google)

    # @patch.object(OAuthRemoteApp, 'get')
    # def test_is_not_facebook_in_db(self, get_mock):

    #     get_mock.return_value = mock_get_response = MagicMock()
    #     mock_get_response.data = {'name': 'Test Name',
    #                               'email': 'test@gmail.com'}
    #     session['oauth_token'] = 'test'

    #     oauth = OAuthSignIn.get_provider('google')
    #     oauth.get_user()
    #     user = User.query.filter_by(email='test@gmail.com').first()
    #     self.assertFalse(user.facebook)

    # @patch.object(OAuthRemoteApp, 'get')
    # def test_user_cant_edit_email(self, get_mock):
    #     password = random_str(30)
    #     user = User('Testname', 'test_1@gmail.com', password, None,
    #                 True)
    #     db.session.add(user)
    #     db.session.commit()
    #     with self.client:
    #         self.login('test_1@gmail.com', password)
    #         response = self.client.get(url_for('users.edit'))
    #         self.assertIn(
    #             '<input type="hidden" name="email" '
    #             'value="test_1@gmail.com" />',
    #             str(response.data)
    #         )
    #         self.assertNotIn(
    #             'Password',
    #             str(response.data)
    #         )

if __name__ == "__main__":
    unittest.main()
