import uuid
from app.user import User_details
from app.service import Services
from app.jwtfile import Jwt_details
from flask import request, json , jsonify, url_for, session, abort, render_template

from . import api

request_object = Services()
user_object = User_details()
jwt_obj = Jwt_details()

@api.before_app_request
def before_request():
    """get the user bafore every request"""
    if request.endpoint and 'auth' not in request.url:
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            access_token = auth_header.split(" ")[1]
            if access_token:
                #try decoding the token and get the user_id
                res = jwt_obj.decode_auth_token(access_token)
                if isinstance(res, int) :
                    #check if no error in string format was returned
                    #find the user with the id on the token
                    
                    return
                return jsonify({"message" : "Please register or login to continue"}), 401
            return jsonify({"message" : "acess token is missing"}), 401
        return jsonify({"message" : "Authorization header is missing"}), 401

@api.route('/')
def index():
	""" 
	Index route test
	"""
	return render_template('index.html'), 200

@api.route('/auth/register', methods=['POST'])
def register():
	"""A route to handle user registration"""
	
	user_details = request.get_json()
	username = user_details['username']
	name = user_details['name']
	password = user_details['password']
	cnfpassword = user_details['cnfpass']
	#pass the details to the register method
	res = user_object.register(username, name, password, cnfpassword)
	if res == "Registration successfull":
		res = user_object.serialiser_user(username)

		return jsonify({"user": res, "message" : "Registration Successfull. You can login now at /api/v2/auth/login"}), 201
	else:
		return jsonify(response = res),409

@api.route('/auth/login', methods=['POST'])
def login():
	"""
	A route to handle user login
	"""
	user_details = request.get_json()
	username = user_details['username']
	password = user_details['password']
	res = user_object.login(username, password)
	if res == "successful":
		user = user_object.serialiser_user(username)
		auth_token = jwt_obj.generate_auth_token(user["id"])
		session['userid'] = user['id']
		return jsonify({"user": user, "message" : "Login Successfull. ", "Access token" : auth_token}), 201
	return res


@api.route('/users/requests', methods = ['GET', 'POST'])
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

@api.route('/users/requests/<reqid>', methods = ['GET', 'PUT'])
def get_request(reqid):
	if request.method == 'PUT':
		request_details = request.get_json()
		category = request_details['category']
		description = request_details['description']
		location = request_details['location']
		date = request_details['date']
		time = request_details['time']
		res = request_object.update(reqid, category, description, location, date, time)
		if res == "update success":
			requests = request_object.find_by_id(reqid)
			ress = jsonify({"message": res, "request": requests})
			return ress, 200
		elif res == "no request with given id":
			return jsonify(response = res), 404
		else:
			return jsonify(response = res), 409

	requests = request_object.find_by_id(reqid)
	return jsonify(requests), 200

