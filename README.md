
[![Build Status](https://travis-ci.org/dessHub/maintenance-tracker.svg?branch=api)](https://travis-ci.org/dessHub/maintenance-tracker)[![Coverage Status](https://coveralls.io/repos/github/dessHub/maintenance-tracker/badge.svg?branch=api)](https://coveralls.io/github/dessHub/maintenance-tracker?branch=api)

# maintenance-tracker

Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.

# Usage 

# API

FORMAT: 1A
HOST: http://mtracker28.herokuapp.com/api/v1/users/

# usage

Use #postman or #Curl

url: http://mtracker28.herokuapp.com/api/v1/users/

## User Registration [/register]

### Register a new user [POST]

You can create a user by sennding a json request with username, 
, password, and password confirmation. password must be atleast 6 characters long.

+ Request(application/json)

            {
                "username" : "sampleusername",
                "email" : "example@gmail.com",
                "password" : "password",
                "cnfpass" : "password"
            }

+ Response 201 (application/json)
            
            {
                "response" : "Registration successfull"
            }
            
+ Response 409 (application/json)

            {
                "response" : "Username already exists"
            }
            
+ Response 409 (application/json)

            {
                "response" : "Username can only contain alphanumeric characters"
            }
            
+ Response 409 (application/json)

            {
                "response" : "passwords do not match"
            }

## Login [/login]

### Login a user [POST]

you can login a user by sending their username and password

+ Request (application/json)

            {
                "username":"sampleusername",
                "password" : "password"
            }
            
+ Response 200 (application/json)

            {
                "response" : "login successful"
            }
            
+ Response 403 (application/json)

            {
                "response" : "wrong username or password"
            }

## requests [/requests]

### Create a request [POST]

You can create a request by sending request category, description, location, date and time 

+ Request (application/json)

            {
                "category":"category",
                "description" : "request description",
                "location":"location",
                "date":"2018-6-20",
                "time":"11:10 AM"
            }
            
+ Response 201 (application/json)

            {
                "response" : "Request send"
            }
            
+ Response 409 (application/json)

            {
                "response" : "Request exists"
            }
            
+ Response 409 (application/json)

            {
                "response" : "description too short or invalid"
            }
        

### Fetch all user requests [GET]

+ Request (application/json)

+ Response 200 (application/json)

        [
            {
                "category":"maintenance",
                "description" : "request description",
                "date":"2018-6-20",
                "time":"11:10 AM",
                "id" : "2be47f9a-d733-11e7-920a-bc8556ecad23",
                "location":"location",
                "userid": "2be47f4g-d733-11e7-920a-bc8556ecad23"
            },
            {
                "category":"Repair",
                "description" : "request description",
                "date":"2018-7-20",
                "time":"11:10 AM",
                "id" : "2be47f9a-d733-11e7-920a-bc8556ecad45",
                "location":"location",
                "userid": "2be47f4g-d733-11e7-920a-bc8556ecad23"
            }
        ]
        
## update request [/requests/<reqid>]

### update request [POST]

you can update a request by sending the request id together with the new category, description, location, date and time

+ Request (application/json)

            {
                "category":"category",
                "description" : "request description",
                "location":"location",
                "date":"2018-6-20",
                "time":"11:10 AM"
            }
            
+ Response 200 (application/json)

            {
                "response" : "update success"
            }
            
+ Response 409 (application/json)

            {
                "response" : "Request cannot be updated, a similar request exists"
            }
            
+ Response 409 (application/json)

            {
                "response" : "description too short or invalid"
            }
            
+ Response 404 (application/json)

            {
                "response" : "no request with given id"
            }


# UI

 Visit [Maintenance App](https://desshub.github.io/maintenance-tracker/ui/index.html)
 
## User Endpoints :
   1. [Request Form](https://desshub.github.io/maintenance-tracker/ui/templates/user/request-form.html)
   2. [User Requests](https://desshub.github.io/maintenance-tracker/ui/templates/user/my-requests.html)
   3. [Login Form](https://desshub.github.io/maintenance-tracker/ui/templates/auth/login.html)
   4. [Sign Up Form](https://desshub.github.io/maintenance-tracker/ui/templates/auth/signup.html)
 
## Admin Endpoints :
   1. [Admin Dashboard](https://desshub.github.io/maintenance-tracker/ui/templates/admin/dashboard.html)
   2. [Requests From Users](https://desshub.github.io/maintenance-tracker/ui/templates/admin/requests.html)
   3. [Single Request Page](https://desshub.github.io/maintenance-tracker/ui/templates/admin/request.html)
   4. [Users Page](https://desshub.github.io/maintenance-tracker/ui/templates/admin/users.html)

# How To Manually Test It:

  1. Clone the project to your local machine:
  
   `git clone https://github.com/dessHub/maintenance-tracker.git`
   
  2. Navigate to project directory:
   
   `cd maintenance-tracker`
    
  3. Change branch to `develop`:
  
     `git checkout develop`
     
  4. Open **ui** folder and click on `index.html` to view on the browser.
  
 # How To Contribute To This Project:
 
  1. Fork the project to your github account.
  2. Clone it to your local machine.
  3. Create a feature branch from `develop` branch :
  
     `git checkout -b ft-name-of-the-feature`
     
  4. Update and Push the changes to github.
   
     `git push origin ft-name-of-the-feature`
    
  5. Create Pull Request to my `develop` branch as base branch.
  
  
