"""This module defines tests for the user class and its methods"""
import unittest
import os

from flask import abort, url_for
from app.user import User_details
from flask_testing import TestCase
from app import create_app
from passlib.hash import sha256_crypt
from connect import conn

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
        self.user = User_details()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS requests")        
        cur.execute("CREATE TABLE users(id serial PRIMARY KEY, email varchar,\
         username varchar, role varchar, password varchar);")
        cur.execute("CREATE TABLE requests(id serial PRIMARY KEY, user_id integer, \
        category varchar, location varchar, req_date date, req_time time, description varchar, \
        status varchar, isresolved boolean);")
        conn.commit()

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
        res = self.user.username_exist("desmond")
        self.assertEqual(res, True)

    def test_password_length(self):
        """Test to ensure that a user has a strong password"""
        res = self.user.register("desmond", "desmond@mail.com", "pass", "pass")
        self.assertEqual(res, "Password too short")

    def test_password_match(self):
        """Test if password matching is working"""
        res = self.user.register("desmond", "desmond@mail.com", "pass1234", "patyt1233")
        self.assertEqual(res, "passwords do not match")

    def test_invalid_password(self):
        """Test if password is valid"""
        res = self.user.login("dessmond", "")
        self.assertEqual(res, "Password Not Valid")

    def test_invalid_username_register(self):
        """Test if username is valid"""
        res = self.user.register("", "desmond@mail.com", "pass1234", "pass1234")
        self.assertEqual(res, "Username Not Valid")

    def test_invalid_username_login(self):
        """Test if username is valid"""
        res = self.user.login("", "pass1234")
        self.assertEqual(res, "Username Not Valid")



