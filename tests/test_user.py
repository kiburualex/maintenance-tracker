"""This module defines tests for the user class and its methods"""
import unittest
import os

from flask import abort, url_for
from app.models import User
from flask_testing import TestCase
from app import create_app
from passlib.hash import sha256_crypt
from connect import conn
from migrate import create_users

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)

        return app


class UserTests(TestBase):
    """Define and setup testing class"""

    def setUp(self):
        """ Set up user object before each test"""
        self.user = User()
        create_users()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.user

    def test_isuccessful_registration(self):
        """Test is a user with correct credentials can register sucessfully"""
        res = User("desmond", "desmond@mail.com", "pass1234")
        user = res.add()
        self.assertEqual(user["username"], "desmond")
    
    def test_existing_user(self):
        """Test with an already existing user, try registering a user twice"""
        res = User("desmond", "desmond@mail.com", "pass1234")
        res.add()
        res2 = User("desmond", "desmond@mail.com", "pass1234")
        user = res2.add()
        self.assertEqual(user, "Username Is already taken")
    
    def test_view_all_users(self):
        """Test view all users"""
        res = User("desmond", "desmond@mail.com", "pass1234")
        res.add()
        res2 = User("desmond", "desmond@mail.com", "pass1234")
        user = res2.add()
        count = len(self.user.fetch_all())
        self.assertEqual(count, 2)

    def test_verify_password_match(self):
        """Test if password matching is working"""
        res = User("desmond", "desmond@mail.com", "pass1234")
        user = res.add()
        h_pass = self.user.verify_password("pass1234", user['password'])
        self.assertTrue(h_pass, True)

    def test_invalid_password(self):
        """Test if password is valid"""
        res = User("desmond", "desmond@mail.com", "pass1234")
        user = res.add()
        h_pass = self.user.verify_password("pass123", user['password'])
        self.assertFalse(h_pass, False)



