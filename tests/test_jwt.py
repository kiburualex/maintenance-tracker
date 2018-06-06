"""This module defines tests for the jwt class and its methods"""
import unittest
import os
from app import create_app

from flask import abort, url_for, Flask
from app.jwtfile import Jwt_details

app = Flask(__name__)

class UserTests(unittest.TestCase):
    """Define and setup testing class"""

    def setUp(self):
        """ Set up jwt object before each test"""
        self.jwtobj = Jwt_details()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.jwtobj

    def test_isuccessful_generate_auth_token(self):
        """a method to generate the access token"""
        auth_token = self.jwtobj.generate_auth_token(1)
        self.assertTrue(isinstance(auth_token, bytes))

    # def test_decode_auth_token(self):
    #     """Test Decodes the access token from the Authorization header"""
    #     with app.app_context():
    #         auth_token = self.jwtobj.generate_auth_token(1)
    #         self.assertTrue(isinstance(auth_token, bytes))
    #         self.assertTrue(self.jwtobj.decode_auth_token(auth_token) == 1)