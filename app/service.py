#used to to validate event names
import re
from datetime import date, datetime
from connect import conn
import uuid
from flask import session

class Services(object):
	""" A class to handle actions related to requests"""

	def __init__(self):
		"""define an empty list to hold all the requests objects"""
		self.request_lists = []

	def existing_request(self, category, user_id, date):
		"""A method to check if a request has already been placed"""
		cur = conn.cursor()
		cur.execute("SELECT * FROM requests WHERE category = %s AND user_id = %s AND \
		 req_date = %s;", (category,user_id, date,))
		cat = cur.fetchone()
		if cat:
			return True
		else:
			return False

	def valid_description(self, description):
		"""check description length and special characters"""
		if len(description) < 10 or not re.match("^[a-zA-Z0-9_ ]*$", description):
			return False
		else:
			return True

	def valid_category(self, category):
		"""check category provided if maintenance or repair"""
		if category == "maintenance" or category == "repair" or category == "Maintenance" or category == "Repair":
			return True
		else:
			return False

	def valid_date(self, re_date):
		"""Check if the given date is less than the current date"""
		date = datetime.strptime(re_date, '%Y-%m-%d').date()
		if date < date.today():
			return False
		return True

	def create(self, category, description, location, date, time, userid):
		"""A method for creating a new request"""
		self.request_details = {}
		if self.valid_category(category):
			if self.existing_request(category, userid, date):
				return "Request Already exists"	
			else:
				#validate event name
				if not self.valid_description(description):
					return "description too short or invalid"
				else:
					status = "New"
					user_id = userid
					req_date = date
					req_time = time
					isresolved = False

					cur = conn.cursor()
					cur.execute("INSERT INTO requests(user_id, category, location, req_date,\
					 req_time, description, status, isresolved)\
					  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(user_id, category, location, req_date,\
					  req_time, description, status, isresolved))
					conn.commit()
					return "Request Sent"
		return "Invalid Category. Category should either be maintenance or repair"

	def view_all(self, user_id):
		""" A method to return a list of all requests"""
		self.request_details = {}
		self.request_list = []
		cur = conn.cursor()
		cur.execute("SELECT * FROM requests WHERE user_id = %s;", (user_id,))
		requests = cur.fetchall()
		for item in requests:
			self.request_details['description'] = item[6]
			self.request_details['category'] = item[2]
			self.request_details['location'] = item[3]
			self.request_details['date'] = item[4].isoformat()
			self.request_details['time'] = item[5].isoformat() 
			self.request_details['status'] = item[7]
			self.request_details['user_id'] = item[1]
			self.request_details['id'] = item[0]
			self.request_details['isresolved'] = item[8]
			self.request_list.append(self.request_details)
		return self.request_list

	def find_by_id(self, reqid):
		"""A method to find a request given an id"""
		for request in self.request_list:
			if request['id'] == reqid:
				return request
		return "Request Doesnt Exist"

	def update(self, reqid, category, description, location, date, time, userid):
		""" Find a request with the given id and update its details"""
		for request in self. request_list:
			if request['id'] == reqid:
				self.request_list.remove(request)
				if self.existing_request(category, userid, date):
					return "Request cannot be updated, a similar Request exists"
				else:
					if not self.valid_description(description):
						return "name too short or invalid"
					else:
						request['description'] = description
						request['category'] = category
						request['location'] = location
						request['date'] = date
						request['time'] = time
						request['status'] = "New"
						request['userid'] = userid
						request['id'] = reqid
						self.request_list.append(self.request_details)
						return "update success"
						break
		else:
			return "no request with given id"




