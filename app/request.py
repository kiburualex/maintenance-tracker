"""This module defines a request class and methods associated to it"""
#used to validate names
import re
import uuid


class Request_details(object):
    """ A class to handle activities related to a request"""
    def __init__(self):
        # A list to hold all user objects
        self.request_list = []


      