import unittest
import os

from flask import url_for, abort, session
from flask_testing import TestCase
from app import create_app

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)

        return app

class TestViews(TestBase):

    def test_index_view(self):
        """
        Test that index is accessible without login
        """
        response = self.client.get(url_for('api.index'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test for login
        """
        response = self.client.get(url_for('api.login'))
        self.assertEqual(response.status_code, 405)

    def test_register_view(self):
        """
        Test for register
        """
        response = self.client.get(url_for('api.register'))
        self.assertEqual(response.status_code, 405)



class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("You do not have sufficient permissions to access this resources." in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("The server encountered an internal error." in response.data)

if __name__ == '__main__':
    unittest.main()