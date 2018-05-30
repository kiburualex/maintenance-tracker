import uuid
from app.user import User_details
from app.service import Services
from flask import request, json , jsonify, url_for, session, abort

from . import api

request_object = Services()
user_object = User_details()


@api.route('/')
def index():
    """
    Index route test
    """
    return "hello"

@api.route('/register', methods=['POST'])
def register():
	"""A route to handle user registration"""
	
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

@api.route('/login', methods=['POST'])
def login():
    """
    A route to handle user login
    """
    user_details = request.get_json()
    username = user_details['username']
    password = user_details['password']
    res = user_object.login(username, password)
    if res == "successful":
		for user in user_object.user_list:
			if user['username'] == username:
				session['userid'] = user['id']
				return jsonify(response ="login successful"), 200
    return res


@api.route('/requests', methods = ['GET', 'POST'])
def userrequests():
	userid = session['userid']
	if request.method == 'POST':
        
		request_details = request.get_json()
		category = request_details['category']
		description = request_details['description']
		location = request_details['location']
		date = request_details['date']
		time = request_details['time']
		res = request_object.create(category, description, location, date, time, userid= session['userid'])
		if res == "Request created":
			return jsonify(response=res), 201
		else:
			return jsonify(response = res), 409
	requests = request_object.view_all(userid)
	return jsonify(requests), 200
