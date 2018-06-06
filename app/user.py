"""This module defines a user class and methods associated to it"""
#used to validate names
import re
import uuid
from connect import conn
from passlib.hash import sha256_crypt

class User_details(object):
	""" A class to handle activities related to a user"""
	def __init__(self):
		# A list to hold all user objects
		self.user_list = []
	
	def register(self, username, name, password, cnfpassword):
		"""A method to register users with correct and valid details"""

		# empty dict to hold dgtails of the user to be created
		
		if not self.valid_username(username):
			return "Username Not Valid"
		else:
			# checkif a user with that username exists
			if self.username_exist(username):
				return "User Already Exists"
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
					h_pass = sha256_crypt.encrypt(password)
					role = "Normal"
					cur = conn.cursor()
					cur.execute("INSERT INTO users(name, username, role, password) VALUES (%s, %s, %s, %s)",(name, username, role, h_pass))
					cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
					items = cur.fetchone()
					conn.commit()
					return "Registration successfull"

	def login(self, username, password):
		"""A method to login a user given valid user details"""
		if not self.valid_username(username):
			return "Username Not Valid"
		else:
			if not self.valid_password(password):
				return "Password Not Valid"
			else:
				if self.username_exist(username):
					user = self.serialiser_user(username)
					h_pass = sha256_crypt.verify(password, user['password'])
					if h_pass:
						return "successful"
					else:
						return "wrong password"
				return "user does not exist", 200

	def valid_username(self, username):
		"""check username length and special characters"""
		if len(username) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", username):
			return False
		else:
			return True

	def username_exist(self, username):
		""" check if user with the same username already exist """
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
		user = cur.fetchone()
		if user:
			return True
		else:
			return False

	def valid_password(self, password):
		"""check password length and special characters"""
		if len(password) < 3 or not re.match("^[a-zA-Z0-9_ ]*$", password):
			return False
		else:
			return True

	def serialiser_user(self, username):
		""" Serialize tuple into dictionary """
		user_details = {}
		cur = conn.cursor()
		cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
		items = cur.fetchone()
		conn.commit()
		user_details['id'] = items[0]
		user_details['name'] = items[1]
		user_details['username'] = items[2]
		user_details['role'] = items[3]
		user_details['password'] = items[4]
		return user_details 

		