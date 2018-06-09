
[![Build Status](https://travis-ci.org/dessHub/maintenance-tracker.svg?branch=api)](https://travis-ci.org/dessHub/maintenance-tracker) [![Coverage Status](https://coveralls.io/repos/github/dessHub/maintenance-tracker/badge.svg?branch=develop)](https://coveralls.io/github/dessHub/maintenance-tracker?branch=develop) <a href="https://codeclimate.com/github/dessHub/maintenance-tracker/maintainability"><img src="https://api.codeclimate.com/v1/badges/82045ce49fe33c89b431/maintainability" /></a> [![Codacy Badge](https://api.codacy.com/project/badge/Grade/196440f843684fb5b333c49774ff0d0f)](https://www.codacy.com/app/dessHub/maintenance-tracker?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dessHub/maintenance-tracker&amp;utm_campaign=Badge_Grade)

# maintenance-tracker

Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.


**Application Features**

* Creating Services Requests
* Keeping Track of requests status 


A user can perform the following :

* create a request
* view his/her requests
* edit and update the request. 
* delete the request created.

**Usage**

* On the browser,visit the following url
    
     * [Mtracker](http://mtracker28.herokuapp.com/api/v1/users/)
    
* To interact with the API via Postman, use the link below
    
    * http://mtracker28.herokuapp.com/api/v1/users/

    then use the following endpoints to perform the specified tasks
    
    EndPoint                            | Functionality
    ------------------------            | ----------------------
    POST /register                      | Create a user account
    POST /login                         | Log in a user
    POST /requests                      | Create a request
    GET /requests                       | Retrieve existing user's requests
    PUT /requests/< reqid >             | Update a requests 
    GET  /requests/< reqid >            | Retrieve a requests


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
  
  
