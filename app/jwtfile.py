import jwt
from flask import current_app
from datetime import datetime, timedelta

class Jwt_details(object):
	""" A class to handle activities related to a jwt"""
	def __init__(self):
		# A list to hold all user objects
		self.user_obj = []

	def generate_auth_token(self, userid):
		"""a method to generate the access token"""
		try:
			# set up a payload
			payload={
					'exp': datetime.utcnow() + timedelta(minutes=60),
					'iat': datetime.utcnow(),
					'sub': userid
			}
			# create the byte string token using the payload and the SECRET key
			jwt_string = jwt.encode(
					payload,
					current_app.config.get('SECRET_KEY'),
					algorithm='HS256'
			)
			return jwt_string

		except Exception as error:
			# return an error in string format if an exception occurs
			return str(error)
