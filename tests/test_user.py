"""This module defines tests for the user class and its methods"""
import pytest
import os

from flask_testing import TestCase

from app import create_app
from app.user import User_details

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        return app

class UserTests(TestCase):
    """Define and setup testing class"""

    def setUp(self):
        """ Set up user object before each test"""
        self.user = User_details()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.user

    @pytest.fixture(scope='module')
    def test_isuccessful_registration(self):
        """Test is a user with correct credentials can register sucessfully"""
        res = self.user.register("desmond", "desmond@mail.com", "pass1234", "pass1234")
        self.assertEqual(res, "Registration successfull")
    
    @pytest.fixture(scope='module')
    def test_existing_user(self):
        """Test with an already existing user, try registering a user twice"""
        self.user.register("desmond", "desmond@mail.com", "pass1234", "pass1234")
        res = self.user.register("desmond", "desmond@mail.com", "pass1234", "pass1234")
        self.assertEqual(res, "Username already exists.")

