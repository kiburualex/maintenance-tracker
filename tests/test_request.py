"""This module defines tests for the request class and its methods"""
import pytest
import os

from flask_testing import TestCase

from app import create_app
from app.request import Request_details

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        return app

class RequestTests(TestCase):
    """Define and setup testing class"""

    def setUp(self):
        """ Set up request object before each test"""
        self.request = Request_details()

    def tearDown(self):
        """ Clear up objects after every test"""
        del self.request

    @pytest.fixture(scope='module')
    def test_isuccessful_created(self):
        """Test if request can create sucessfully with correct fields"""
        res = self.request.create("maintenance", "request descriptions", "location", "pending", "2018-6-5", "10:20 AM", "1",)
        self.assertEqual(res, "Created successfull")

    def test_create_existing_request(self):
    	""" Test if a request can be created twice"""
    	
    	self.request.request_list = [{"type" :'maintenance', "description" :'request descriptions',\
         "location":"CBD",  "status":'pending', \
         "date" : '2018-6-5', "time" : "10:20 AM", "userid":'1'}]
    	res = self.request.create("maintenance", "request descriptions",\
         "location", "pending", "2018-6-5", "10:20 AM", "1",)
    	self.assertEqual(res, "Request already exists")

    def test_request_filter(self):
    	"""Test if filter by userid works"""
    	self.request.create("maintenance", "request descriptions",\
         "location", "pending", "2018-6-5", "10:20 AM", "1",)
    	self.request.create("maintenance", "request descriptions",\
         "location", "pending", "2018-6-5", "10:20 AM", "2",)
    	res = self.request.request_filter("1")
    	request_description = res[0]['description']
    	self.assertIs(request_description, "request descriptions")
    