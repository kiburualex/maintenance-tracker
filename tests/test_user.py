"""This module defines tests for the user class and its methods"""
import unittest
import os

from flask import abort, url_for
from app.user import User_details

class UserTests(unittest.TestCase):
    """Define and setup testing class"""

    def setUp(self):
        """ Set up user object before each test"""
        self.user = User_details()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.user

    def test_isuccessful_registration(self):
        """Test is a user with correct credentials can register sucessfully"""
        res = self.user.register("desmond", "desmond@mail.com", "pass1234", "pass1234")
        self.assertEqual(res, "Registration successfull")
    
    def test_existing_user(self):
        """Test with an already existing user, try registering a user twice"""
        self.user.register("desmond", "desmond@mail.com", "pass1234", "pass1234")
        res = self.user.register("desmond", "desmond@mail.com", "pass1234", "pass1234")
        self.assertEqual(res, "Username already exists.")

    def test_password_length(self):
        """Test to ensure that a user has a strong password"""
        res = self.user.register("desmond", "desmond@mail.com", "pass", "pass")
        self.assertEqual(res, "Password too short")

    def test_password_match(self):
        """Test if password matching is working"""
        res = self.user.register("desmond", "desmond@mail.com", "pass1234", "patyt1233")
        self.assertEqual(res, "passwords do not match")


