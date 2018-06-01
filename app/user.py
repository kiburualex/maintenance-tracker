"""This module defines a user class and methods associated to it"""
#used to validate names
import re
import uuid


class User_details(object):
	""" A class to handle activities related to a user"""
	def __init__(self):
		# A list to hold all user objects
		self.user_list = []

	def register(self, username, email, password, cnfpassword):
		"""A method to register users with correct and valid details"""

		# empty dict to hold dgtails of the user to be created
		user_details = {}
		if not self.valid_username(username):
			return "Username Not Valid"
		else:
			# checkif a user with that username exists
			for user in self.user_list:
				if username == user['username']:
					return "Username already exists."
					break
			else:
				#validate password and username
				if not re.match("^[a-zA-Z0-9_]*$", username):
					return "Username can only contain alphanumeric characters"
				elif password != cnfpassword:
					return "passwords do not match"
				elif len(password) < 6:
					return "Password too short"     
				else:
					#register user if all the details are valid
					user_details['username'] = username
					user_details['email'] = email
					user_details['password'] = password
					user_details['id'] = uuid.uuid1()
					self.user_list.append(user_details)
					return "Registration successfull"

	def login(self, username, password):
		"""A method to login a user given valid user details"""
		if not self.valid_username(username):
			return "Username Not Valid"
		else:
			if not self.valid_password(password):
				return "Password Not Valid"
			else:
				for user in self.user_list:
					if username == user['username']:
						if password == user['password']:
							return "successful"
						else:
							return "wrong password"
							break
					return "user does not exist", 200



	def valid_username(self, username):
		"""check username length and special characters"""
		if len(username) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", username):
			return False
		else:
			return True

	def valid_password(self, password):
		"""check password length and special characters"""
		if len(password) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", password):
			return False
		else:
			return True


		