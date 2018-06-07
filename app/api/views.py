import uuid
from app.user import User_details
from app.service import Services
from app.jwtfile import Jwt_details
from flask import request, json, jsonify, url_for, session, abort, render_template, g

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
            if isinstance(res, int):
                # check if no error in string format was returned
                # find the user with the id on the token
                user = user_object.user_by_id(id=res)
                g.userid = user['id']
                g.role = user['role']
                return
            return jsonify({"message": "Please register or login to continue"}), 401
        except Exception as e:
            return jsonify(response="Authorization header or acess token is missing."), 400


@api.route('/')
def index():
    """
    Index route test
    """
    return render_template('index.html'), 200


@api.route('/auth/register', methods=['POST'])
def register():
    """A route to handle user registration"""
    try:
        user_details = request.get_json()
        username = user_details['username']
        name = user_details['name']
        password = user_details['password']
        cnfpassword = user_details['cnfpass']
    except (ValueError, KeyError, TypeError) as error:
        return jsonify(response="Make sure you are passing all the values and valid json data"), 400
    # pass the details to the register method
    res = user_object.register(username, name, password, cnfpassword)
    if res == "Registration successfull":
        res = user_object.serialiser_user(username)

        return jsonify({"user": res, "message": "Registration Successfull. You can login now at /api/v2/auth/login"}), 201
    else:
        return jsonify(response=res), 409




@api.route('/auth/login', methods=['POST'])
def login():
    """
    A route to handle user login
    """
    try:
        user_details = request.get_json()
        username = user_details['username']
        password = user_details['password']
    except (ValueError, KeyError, TypeError) as error:
        return jsonify(response="Make sure you are passing all the values and valid json data"), 400

    res = user_object.login(username, password)
    if res == "successful":
        user = user_object.serialiser_user(username)
        auth_token = jwt_obj.generate_auth_token(user["id"])
        return jsonify({"user": user, "message": "Login Successfull. ", "Access token": auth_token}), 201
    return jsonify(response=res), 400


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
            return jsonify(response="Make sure you are passing all the values and valid json data"), 400

        res = request_object.create(
            category, description, location, date, time, userid=session['userid'])
        if res == "Request created":
            return jsonify(response=res), 201
        else:
            return jsonify(response=res), 409
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
        except (ValueError, KeyError, TypeError) as error:
            return jsonify(response="Make sure you are passing all the values and valid json data"), 400

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
        return jsonify(response="Sorry you don't have enough rights to view this resource")


@api.route('/requests/<reqid>/approve')
def admin_approve(reqid):
    """ Admin endpoint to approve requests"""
    if g.role == "Admin":
        isexist = request_object.request_exist_by_id(reqid)
        if isexist:
            res = request_object.is_resolved(reqid)
            if res == False:
                resp = request_object.approve(reqid)
                if resp == True:
                    requests = request_object.find_by_id(reqid)
                    return jsonify(requests), 200
                else:
                    return jsonify(response="Error Approving the requests"), 304
            else:
                return jsonify(response="Request is already resolved"), 409
        else:
            return jsonify(response="Request doesnt exists"), 404
    else:
        return jsonify(response="Sorry you don't have enough rights to view this resource"), 401


@api.route('/requests/<reqid>/disapprove')
def admin_disapprove(reqid):
    """ Admin endpoint to disapprove requests"""
    if g.role == "Admin":
        isexist = request_object.request_exist_by_id(reqid)
        if isexist:
            res = request_object.is_resolved(reqid)
            if res == False:
                resp = request_object.disapprove(reqid)
                if resp == True:
                    requests = request_object.find_by_id(reqid)
                    return jsonify(requests), 200
                else:
                    return jsonify(response="Error Disapproving the requests"), 304
            else:
                return jsonify(response="Request is already resolved"), 409
        else:
            return jsonify(response="Request doesnt exists"), 404
    else:
        return jsonify(response="Sorry you don't have enough rights to view this resource"), 401


@api.route('/requests/<reqid>/resolve')
def admin_resolve(reqid):
    """ Admin endpoint to dresolve requests"""
    if g.role == "Admin":
        isexist = request_object.request_exist_by_id(reqid)
        if isexist:
            res = request_object.is_resolved(reqid)
            if res == False:
                resp = request_object.resolve(reqid)
                if resp == True:
                    requests = request_object.find_by_id(reqid)
                    return jsonify(requests), 200
                else:
                    return jsonify(response="Error Resolving the requests"), 304
            else:
                return jsonify(response="Request is already resolved"), 409
        else:
            return jsonify(response="Request doesnt exists"), 404
    else:
        return jsonify(response="Sorry you don't have enough rights to view this resource"), 401
