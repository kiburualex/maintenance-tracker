#used to to validate event names
import re
from datetime import date, datetime
import uuid

class Services(object):
	""" A class to handle actions related to events"""

	def __init__(self):
		"""define an empty list to hold all the event objects"""
		self.request_list = []

	def existing_request(self, category, userid, date):
		"""A method to check if a request has already been placed"""
		for request in self.request_list:
			#test to see if the user has already send simmilar requests 
			if request['category'] == category and request['userid'] == userid:
				if request['date'] == date:
					return True
					break
		else:
			return False

	def valid_description(self, description):
		"""check description length and special characters"""
		if len(description) < 10 or not re.match("^[a-zA-Z0-9_ ]*$", description):
			return False
		else:
			return True

	def valid_date(self, re_date):
		"""Check if the given date is less than the current date"""
		date = datetime.strptime(re_date, '%Y-%m-%d').date()
		if date < date.today():
			return False
		return True

	def create(self, category, description, location, date, time, userid):
		"""A method for creating a new event"""
		self.request_details = {}
		if self.existing_request(category, userid, date):
			return "Request Already exists"	
		else:
			#validate event name
			if not self.valid_description(description):
				return "description too short or invalid"
			else:
				self.request_details['description'] = description
				self.request_details['category'] = category
				self.request_details['location'] = location
				self.request_details['date'] = date
				self.request_details['time'] = time
				self.request_details['status'] = "New"
				self.request_details['userid'] = userid
				self.request_details['id'] = uuid.uuid1()
				self.request_list.append(self.request_details)
                return "Request Send"




