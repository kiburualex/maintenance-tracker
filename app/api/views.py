import uuid
import re
from app.user import User_details
from app.service import Services
from app.jwtfile import Jwt_details
from app.models import User, Store
from flask import request, json, jsonify, url_for, \
    session, abort, render_template, g

from . import api

request_object = Services()
user_object = User_details()
jwt_obj = Jwt_details()

@api.before_app_request
def before_request():
    """get the user bafore every request"""
    if request.endpoint and 'auth' not in request.url:
        try:
            auth_header = request.headers.get('Authorization')
            g.user = None
            access_token = auth_header.split(" ")[1]
            res = jwt_obj.decode_auth_token(access_token)
            if isinstance(res, int) and not jwt_obj.is_blacklisted(access_token):
                # check if no error in string format was returned
                # find the user with the id on the token
                print(res)
                user = User()             
                res = user.user_by_id(id=res)
                print(res['id'])
                g.userid = res['id']
                print(g.userid)
                g.role = res['role']
                return
            return jsonify({"message": "Please register or \
            login to continue"}), 401
        except Exception as e:
            return jsonify(response="Authorization header or \
            acess token is missing."), 400

def validdate_data(data):
    """validate user details"""
    try:
        #check if there are specil characters in the username
        if not re.match("^[a-zA-Z0-9_]*$", data['username'].strip()):
            return "username  can only contain alphanumeric characters"
        #check if the username is more than 3 characters
        elif len(data['username'].strip()) < 3:
            return "username must be more than 3 characters"
        #check if the name contains only numbers or underscore
        elif not re.match("[a-zA-Z]{3,}_*[0-9_]*[a-zA-Z]*_*", data['username'].strip()):
            return "username must have atleast 3 letters before number or underscore"
        elif not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data['email'].strip()):
            return "please provide a valid email"
        else:
            return "valid"
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

def validate_password(data):
    """validate the password and return appropriate response"""
    try:
        #chack for spaces in password
        if " " in data["password"]:
            return "password should be one word, no spaces"
        elif len(data['password'].strip()) < 6:
            return "Password should have atleast 6 characters"
        #check if the passwords mact
        elif  data['password'] != data['cnfpass']:
            return "passwords do not match"
        else:
            return "valid"
    #some data is missing and a keyError exception was raised
    except Exception as error:
        return "please provide all the fields, missing " + str(error)

@api.route('/') 
def index():
    """
    Index route test
    """
    return render_template('index.html'), 200


@api.route('/auth/register', methods=['POST'])
def register():
    """A route to handle user registration"""
    
    data = request.get_json()
    #validate the data
    res = validdate_data(data)
    check_pass = validate_password(data)
    if res is not "valid":
        return jsonify({"message" : res}), 400
    elif check_pass is not "valid":
        return jsonify({"message" : check_pass}), 400
    else:
        try:
            username = data['username']
            email = data['email']
            password = data['password']
            user = User(username, email, password)
            res = user.add()
            return jsonify(res), 201
        except Exception as error:
            #an error occured when trying to register the user
            response = {'messageu' : str(error)}
            return jsonify(response), 401


@api.route('/auth/login', methods=['POST'])
def login():
    """
    A route to handle user login
    """
    try:
        user_details = request.get_json()
        username = user_details['username']
        password = user_details['password']
    except (ValueError, KeyError, TypeError):
        return jsonify(response="Make sure you are passing all \
        the values and valid json data"), 400

    res = user_object.login(username, password)
    if res == "successful":
        user = user_object.serialiser_user(username)
        auth_token = jwt_obj.generate_auth_token(user["id"])
        return jsonify({"user": user, "message": "Login Successfull.\
         ", "Access token": auth_token}), 201
    elif res == "wrong password":
        return jsonify(response=res), 400
    else:
        return jsonify(response=res), 404

@api.route('/auth/logout')
def logout():
    """store the access_token in blacklist when a user logs out"""
    auth_header= request.headers.get('Authorization')
    access_token = auth_header.split(" ")[1]
    #check is the token is valid
    res = jwt_obj.decode_auth_token(access_token)
    if isinstance(res, int) and not jwt_obj.is_blacklisted(access_token):
        #the token is still valid and not in blasklist
        blasklisted_token = jwt_obj.blacklist_token(access_token)
        if blasklisted_token is True:
            return jsonify({"message" : "logout successfuly."}), 200
        else:
            return jsonify({"message" : "Error While loging out."}), 500
    return jsonify({"message" : "you are already logged out"}), 401

@api.route('/users/requests', methods=['GET', 'POST'])
def userrequests():
    userid = g.userid
    role = g.role
    if request.method == 'POST':
        try:
            request_details = request.get_json()
            category = request_details['category']
            description = request_details['description']
            location = request_details['location']
            date = request_details['date']
            time = request_details['time']
        except (ValueError, KeyError, TypeError) as error:
            return jsonify(response="Make sure you are passing all \
            the values and valid json data"), 400

        valid_category = request_object.valid_category(category)
        if valid_category is True:
            res = request_object.existing_request(
                category, userid, date)
            if res is False:
                try:
                    res = request_object.create(
                        category, description, location, date, time, userid)

                    return jsonify({"message": "Successfully Created",
                                    "Request": res}), 201
                except Exception:
                    return jsonify(response="Error Creating Request"), 501
            return jsonify(response="Request Already exists"), 409
        return jsonify(response="Invalid Category. Category should either \
        be maintenance or repair"), 400
    requests = request_object.view_all(userid, role)
    return jsonify(requests), 200


@api.route('/users/requests/<reqid>', methods=['GET', 'PUT'])
def get_request(reqid):
    if request.method == 'PUT':
        try:
            request_details = request.get_json()
            category = request_details['category']
            description = request_details['description']
            location = request_details['location']
            date = request_details['date']
            time = request_details['time']
        except (ValueError, KeyError, TypeError):
            return jsonify(response="Make sure you are passing all \
            the values and valid json data"), 400

        res = request_object.update(
            reqid, category, description, location, date, time)
        if res == "update success":
            requests = request_object.find_by_id(reqid)
            ress = jsonify({"message": res, "request": requests})
            return ress, 201
        elif res == "no request with given id":
            return jsonify(response=res), 404
        else:
            return jsonify(response=res), 409

    requests = request_object.find_by_id(reqid)
    return jsonify(requests), 200


@api.route('/requests')
def admin_requests():
    """ Admin endpoint to view all users requests"""
    if g.role == "Admin":
        res = request_object.view_all(g.userid, g.role)
        return jsonify(res), 200
    else:
        return jsonify(response="Sorry you don't have enough \
        rights to view this resource")


@api.route('/requests/<reqid>/approve')
def admin_approve(reqid):
    """ Admin endpoint to approve requests"""
    if g.role == "Admin":
        isexist = request_object.request_exist_by_id(reqid)
        if isexist:
            res = request_object.is_resolved(reqid)
            if res is False:
                resp = request_object.approve(reqid)
                if resp is True:
                    requests = request_object.find_by_id(reqid)
                    return jsonify(requests), 200
                else:
                    return jsonify(response="Error Approving \
                    the requests"), 304
            else:
                return jsonify(response="Request is already resolved"), 409
        else:
            return jsonify(response="Request doesnt exists"), 404
    else:
        return jsonify(response="Sorry you don't have enough \
        rights to view this resource"), 401


@api.route('/requests/<reqid>/disapprove')
def admin_disapprove(reqid):
    """ Admin endpoint to disapprove requests"""
    if g.role == "Admin":
        isexist = request_object.request_exist_by_id(reqid)
        if isexist:
            res = request_object.is_resolved(reqid)
            if res is False:
                resp = request_object.disapprove(reqid)
                if resp is True:
                    requests = request_object.find_by_id(reqid)
                    return jsonify(requests), 200
                else:
                    return jsonify(response="Error Disapproving \
                    the requests"), 304
            else:
                return jsonify(response="Request is already resolved"), 409
        else:
            return jsonify(response="Request doesnt exists"), 404
    else:
        return jsonify(response="Sorry you don't have enough \
        rights to view this resource"), 401


@api.route('/requests/<reqid>/resolve')
def admin_resolve(reqid):
    """ Admin endpoint to dresolve requests"""
    if g.role == "Admin":
        isexist = request_object.request_exist_by_id(reqid)
        if isexist:
            res = request_object.is_resolved(reqid)
            if res is False:
                resp = request_object.resolve(reqid)
                if resp is True:
                    requests = request_object.find_by_id(reqid)
                    return jsonify(requests), 200
                else:
                    return jsonify(response="Error Resolving\
                     the requests"), 304
            else:
                return jsonify(response="Request is already resolved"), 409
        else:
            return jsonify(response="Request doesnt exists"), 404
    else:
        return jsonify(response="Sorry you don't have enough \
        rights to view this resource"), 401
