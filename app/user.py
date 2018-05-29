"""This module defines a user class and methods associated to it"""
#used to validate names
import re
import uuid


class User_details(object):
    """ A class to handle activities related to a user"""
    def __init__(self):
        # A list to hold all user objects
        self.user_list = []


        