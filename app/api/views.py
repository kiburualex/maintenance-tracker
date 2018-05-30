import uuid
from app.user import User_details
from flask import request, json , jsonify, url_for, session,abort

from . import api

user_object = User_details()

@api.route('/')
def index():
    """
    Index route test
    """
    return "hello"

@api.route('/register', methods=['GET','POST'])
def register():
	"""A route to handle user registration"""
	if request.method == 'POST':
		user_details = request.get_json()
		username = user_details['username']
		email = user_details['email']
		password = user_details['password']
		cnfpassword = user_details['cnfpass']
		#pass the details to the register method
		res = user_object.register(username,email, password, cnfpassword)
		if res == "Registration successfull":
			return jsonify(response = res), 201
		else:
			return jsonify(response = res),409
	return jsonify(response="Get request currently not allowed"),405

