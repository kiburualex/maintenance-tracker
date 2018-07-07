import unittest
import os
import json
from flask import url_for, abort, session
from flask_testing import TestCase
from app import create_app

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)

        return app

class TestViews(TestBase):


    def test_register_view(self):
        """
        Test for register
        """
        response = self.client.get(url_for('api.register'))
        self.assertEqual(response.status_code, 405)

    def test_registration(self):
        """ Test for user registration """
        resource = self.client.post('api/v2/auth/register', data=json.dumps(dict(username="dan",email='info@gmail.com', password='pass123', cnfpass='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Registered Successfully')

    def test_invalid_password(self):
        """ Test for invalid password """
        resource = self.client.post('api/v2/auth/register', data=json.dumps(dict(username="dan",email='info@gmail.com', password='pas', cnfpass='pas'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Password should have atleast 6 characters')

    def test_not_matching_password(self):
        """ Test for not matching password """
        resource = self.client.post('api/v2/auth/register', data=json.dumps(dict(username="dan",email='info@gmail.com', password='pass123', cnfpass='pass1234'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'passwords do not match')

    def test_valid_username(self):
        """ Test for valid usernames """
        resource = self.client.post('api/v2/auth/register', data=json.dumps(dict(username="232dess",email='info@gmail.com', password='pass123', cnfpass='pass1234'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 400)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'username must have atleast 3 letters before number or underscore')

    def test_login_view(self):
        """
        Test for login
        """
        response = self.client.get(url_for('api.login'))
        self.assertEqual(response.status_code, 405)

    def test_login(self):
        """"
        Test for login
        """
        resource = self.client.post('api/v2/auth/register', data=json.dumps(dict(username="dan",email='info@gmail.com', password='pass123', cnfpass='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Registered Successfully')

        resource = self.client.post('api/v2/auth/login', data=json.dumps(dict(username="dan", password='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Login Successfull.')

    def test_login_wrong_password(self):
        """"
        Test for wrong login credentials
        """
        # Register user
        resource = self.client.post('api/v2/auth/register', data=json.dumps(dict(username="dan",email='info@gmail.com', password='pass123', cnfpass='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Registered Successfully')

        # Login user
        resource = self.client.post('api/v2/auth/login', data=json.dumps(dict(username="dan", password='pass12'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 401)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'invalid username or password, \
            Please try again')

    def test_users_request(self):
        """
        Test users requests with no access token
        """
        request_resource = self.client.post('/api/v2/users/requests', data=json.dumps(dict(category="Maintenance", description="description goes here", location="repair"
                                                                                             )))
        data = json.loads(request_resource.data.decode())
        self.assertEqual(request_resource.content_type, 'application/json')
        self.assertEqual(request_resource.status_code, 400)

    def test_request_enpoints(self):
        """
        Test users requests with access token
        """
        # Register User
        resource = self.client.post('api/v2/auth/register', data=json.dumps(dict(username="dan",email='info@gmail.com', password='pass123', cnfpass='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'], 'Registered Successfully')
        # Login user
        resource = self.client.post('api/v2/auth/login', data=json.dumps(dict(username="dan", password='pass123'
                                                                                 )), content_type='application/json')

        data = json.loads(resource.data.decode())
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(resource.content_type, 'application/json')
        self.assertEqual(data['message'].strip(), 'Login Successfull.')
        access_token = data["Access_token"]
        Authorization='Bearer ' + access_token
        headers = {'content-type': 'application/json','Authorization': Authorization}
        # create requests
        """ Successfully created """
        request_resource = self.client.post('/api/v2/users/requests', data=json.dumps(dict(category="Maintenance", description="description goes here", location="Mombasa"
                                                                                             )),headers=headers)
        data = json.loads(request_resource.data.decode())
        self.assertEqual(request_resource.content_type, 'application/json')
        self.assertEqual(resource.status_code, 201)
        self.assertEqual(data["message"], "Successfully created")
       
        """ Invalid Category """
        request_resource = self.client.post('/api/v2/users/requests', data=json.dumps(dict(category="Other", description="description goes here", location="Mombasa"
                                                                                             )),headers=headers)
        data = json.loads(request_resource.data.decode())
        self.assertEqual(request_resource.content_type, 'application/json')
        self.assertEqual(data["resp"], "Category should either be Maintenance, maintenance, Repair or repair")
       
        """View a particular requests """
        request_resource = self.client.get(
            '/api/v2/users/requests/1', headers=headers)
        data = json.loads(request_resource.data.decode())
        requests = data["location"]
        self.assertEqual(request_resource.status_code, 200)
        self.assertEqual(data["user_id"], 1)
         
        """ Update someone requests """
        request_resource = self.client.put('/api/v2/users/requests/1', data=json.dumps(dict(category="Repair", description="description goes here", location="Mombasa"
                                                                                             )),headers=headers)
        data = json.loads(request_resource.data.decode())
        self.assertEqual(request_resource.content_type, 'application/json')
        self.assertEqual(data["message"], "Sorry you cant edit this request")
        
        """ Admin Requests """
        request_resource = self.client.get('/api/v2/requests', headers=headers)
        data = json.loads(request_resource.data.decode())
        self.assertEqual(data["response"], "Sorry you don't have enough \
        rights to view this resource")

        # Log out user
        resource = self.client.get('api/v2/auth/logout', headers=headers)

        data = json.loads(resource.data.decode())
        self.assertEqual(data['message'], 'logout successfuly.')


if __name__ == '__main__':
    unittest.main()