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


if __name__ == '__main__':
    unittest.main()