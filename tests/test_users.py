#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for oauth module."""

from mock import patch
from mock import MagicMock
from tests.test_base import BaseTestCase
from flask import url_for, session
from multaviso import create_app, db
from multaviso.users.models import User
from flask_login import current_user

class UsersTestCase(BaseTestCase):

    # logout
    def test_logout(self):
        """Test user can logout."""
        with self.client:
            self.login()
            response = self.client.get('/users/logout', follow_redirects=True)
            self.assertIn(b'You were logged out', response.data)

