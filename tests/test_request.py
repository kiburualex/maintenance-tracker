"""This module defines tests for the request class and its methods"""
import unittest
import os
from datetime import date, datetime

from flask import abort, url_for

from app import create_app
from app.models import Service
from flask_testing import TestCase
from app import create_app
from migrate import create_requests

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)

        return app

class RequestTests(TestBase):
    """Define and setup testing class"""

    def setUp(self):
        """ Set up request object before each test"""
        self.request = Service()
        create_requests()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.request

    def test_isuccessful_created(self):
        """Test if request can create sucessfully with correct fields"""
        res = Service("maintenance", "request descriptions", "location", "1")
        req = res.add()
        request_d = dict(
            id=1
            )
        self.assertEqual(req['id'], request_d['id'])

    def test_fetch_by_userid(self):
    	"""Test if filter by userid works"""
        res1 = Service("maintenance", "request descriptions", "location", "1")
        req = res1.add()
        res2 = Service("maintenance", "request descriptions", "location", "1")
        req = res2.add()
    	res = self.request.fetch_by_userid("1")
    	request_description = len(res)
    	self.assertEqual(request_description, 2)

    def test_fetch_by_id(self):
        """Test if the method finds the exactly specified id"""        
        res = Service("maintenance", "request descriptions", "location", "1")
        req = res.add()
        foundrequest = self.request.fetch_by_id(1)
        self.assertEqual(foundrequest['id'], 1)
        self.assertFalse(self.request.fetch_by_id(4), False)

    def test_view_all(self):
    	"""Test if view all works"""
        res1 = Service("maintenance", "request descriptions", "location", "1")
        res1.add()
        res2 = Service("maintenance", "request descriptions", "location", "1")
        res2.add()
    	res = self.request.view_all()
    	count = len(res)
    	self.assertEqual(count, 2)

    def test_is_owner(self):
        """Test if reuest belong to a user"""        
        res = Service("maintenance", "request descriptions", "location", "1")
        req = res.add()
        foundrequest = self.request.is_owner(1, 1)
        self.assertEqual(foundrequest, True)
        self.assertFalse(self.request.is_owner(1, 2), False)

    
    def test_valid_category(self):
        """Test if the method can detect valid category"""
        res = self.request.valid_category("maintenance")
        self.assertEqual(res, True)

    def test_invalid_category(self):
        """Test if the method can detect invalid category"""
        res = self.request.valid_category("other")
        self.assertEqual(res, False)
     