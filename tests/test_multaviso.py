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
    ## app.get returns a class: http://flask.pocoo.org/docs/0.12/api/#flask.Response
    def setUp(self):

        # Config a temporary database
        # mkstemp() returns a tuple containing an OS-level handle to an open file (as would be returned by os.open()) and the absolute pathname of that file, in that order.
        self.db_fd, multaviso.app.config['DATABASE'] = tempfile.mkstemp()
        print(dir(multaviso))
        print("--------------------------")
        print(multaviso.app)
        multaviso.app.config['TESTING'] = True # disable the error catching during request handling
        #Creating a test client for the app
        self.app = multaviso.app.test_client()
        #self.app.testing = True 
        
        #with multaviso.app.app_context():
        #    multaviso.init_db()

    def tearDown(self):
        #os.close(self.db_fd)
        os.unlink(multaviso.app.config['DATABASE'])

    def test_empty_db(self):
        # with multaviso.app.test_client() as c:
        #     response = c.get('/')
        #     print("response:")
        #     print(response)
        #     self.assertEquals(response.status_code, 200)
        rv = self.app.get('/')
        self.assertIn(b'Sign in with twitter.', rv.data)

if __name__ == '__main__':
    unittest.main()
