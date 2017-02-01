#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Unit tests for pages module."""

import unittest
from tests.test_base import BaseTestCase
from flask import url_for

class PagesTestCase(BaseTestCase):

    """Application wide tests."""
    
    def test_home_page(self):
        """General 200 test."""
        response = self.client.get(url_for('pages.home'))
        self.assert200(response)
        self.assertTemplateUsed('home.html')


if __name__ == "__main__":
    unittest.main()
