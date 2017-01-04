import os
from context import multaviso

import unittest
import tempfile

class MultavisoTestCase(unittest.TestCase):

    ## Called before each individual test function is run
    ## Two main tasks:
    ## - creates a new test client to have a simple interface to the application
    ##   - handles requests to the application, and
    ##   - keep track of cookies
    ## - initialize a new database.
    ##   - SQLite3 is filesystem-based we can use the tempfile module to create
    ##     a temporary database and initialize it.
    def setUp(self):
        self.db_fd, multaviso.app.config['DATABASE'] = tempfile.mkstemp()
        multaviso.app.config['TESTING'] = True # disable the error catching during request handling
        self.app = multaviso.app.test_client()
        with multaviso.app.app_context():
            multaviso.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(multaviso.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

if __name__ == '__main__':
    unittest.main()
