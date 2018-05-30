"""This module defines a request class and methods associated to it"""
#used to validate names
import re
import uuid


class Requests(object):
    """ A class to handle activities related to a request"""
    def __init__(self):
        # A list to hold all user objects
        self.request_list = []

	def create(self, category, description, location, date, time, status, userid):
		"""A method for creating a new event"""
		self.request_details = {}
		if self.existing_request(category, userid, date):
			return "Request Already exists"	
		else:
			#validate event name
			if not self.valid_description(description):
				return "description too short or invalid"
			#validate event date
			elif not self.valid_date(date):
				return "event can only have a future date"
			else:
				self.event_details['description'] = description
				self.event_details['category'] = category
				self.event_details['location'] = location
				self.event_details['date'] = date
				self.event_details['time'] = time
				self.event_details['status'] = status
				self.event_details['date_created'] = date.today().isoformat()
				self.event_details['userid'] = userid
				self.event_details['id'] = uuid.uuid1()
				self.event_list.append(self.event_details)
				return "Reuest Send"

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

	def valid_date(self, date):
		"""Check if the given date is less than the current date"""
		date = datetime.strptime(date, '%Y-%m-%d').date()
		if date < date.today():
			return False
		return True


      