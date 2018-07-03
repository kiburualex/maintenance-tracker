import psycopg2
import os
import re
from datetime import date, datetime
from connect import conn
from passlib.hash import sha256_crypt
cur = conn.cursor()

class User(object):
    def __init__(self,username=None, email=None, password=None):
        super(User, self).__init__()
        self.role = "Normal"
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        conn.commit()

    def create(self):
        self.create_table("CREATE TABLE users(id serial PRIMARY KEY, email varchar\
          NOT NULL UNIQUE, username varchar NOT NULL UNIQUE, role varchar NOT NULL,\
           password varchar NOT NULL);"
        )

    def add(self):
        if self.username_exist(self.username) is False:
            hash_pass = self.hash_password(self.password)
            cur.execute(
                """
                INSERT INTO users (username, email, role, password)
                VALUES (%s , %s, %s, %s) RETURNING id;
                """,
                (self.username, self.email, self.role, hash_pass))
            userid = cur.fetchone()[0]
            self.save()

            return self.user_by_id(userid)
        return "Username Is already taken"

    def fetch_all(self):
        cur.execute("SELECT * FROM users")
        users_tuple = cur.fetchall()
        users = []

        for user in users_tuple:
            users.append(self.serializer(user))

        return users


    def find_by_username(self, username):
        cur.execute(
            "SELECT * FROM users where username=%s", (username, ))

        user = cur.fetchone()

        if user:
            return self.serializer(user)
        return False

    def make_admin(self, username, role):
        cur.execute("UPDATE users SET role = %s\
         WHERE username = %s;", (role, username)
        )
        item = self.find_by_username(username)
        self.save()
        return item

    def serializer(self, user):
        return dict(
            id=user[0],
            username=user[1],
            email=user[2],
            role=user[3],
            password=user[4]
        )

    def username_exist(self, username):
        """ check if user with the same username already exist """
        cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
        user = cur.fetchone()
        if user:
            return True
        else:
            return False

    def hash_password(self, password):
        """Hash Password """
        h_pass = sha256_crypt.encrypt(password)
        return h_pass

    def verify_password(self, password, h_pass):
        """ Verify Password"""
        h_pass = sha256_crypt.verify(password, h_pass)
        return h_pass

    def serialiser_user(self, user):
        """ Serialize tuple into dictionary """
        print()
        user_details = dict(
            id=user[0],
            username=user[1],
            email=user[2],
            role=user[3],
            password=user[4]
        )
        return user_details

    def user_by_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM users WHERE id = %s;", (id,))
        user = cur.fetchone()

        return self.serialiser_user(user)

class Service(object):
    def __init__(
            self, category=None, description=None, \
            location=None, userid=None):
        super(Service, self).__init__()
        self.userid = userid
        self.category = category
        self.description = description
        self.location = location
        self.status = "Pending"
        self.isresolved = False
        self.req_date = date.today()

    def save(self):
        conn.commit()

    def create(self):
        self.create_table("CREATE TABLE requests(id serial PRIMARY KEY, user_id integer, \
        category varchar, location varchar, req_date date, description varchar, \
        status varchar, isresolved boolean);")

    def add(self):
        cur.execute("INSERT INTO requests(user_id, category,\
        location, req_date, description, status,\
        isresolved) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                    (self.userid, self.category, self.location, self.req_date,
                     self.description, self.status, self.isresolved))
        item = cur.fetchone()[0]
        self.save()
        return self.fetch_by_id(item)

    def valid_category(self, category):
        """check category provided if maintenance or repair"""
        if category == "maintenance" or category == "repair" or \
                category == "Maintenance" or category == "Repair":
            return True
        else:
            return False

    def view_all(self):
        cur.execute("SELECT * FROM requests")
        requests_tuple = cur.fetchall()
        requests = [self.serializer(request) for request in requests_tuple]
        return requests

    def fetch_by_id(self, reqid):
        cur.execute(
            "SELECT * FROM requests WHERE id=%s", (reqid, ))
        request_tuple = cur.fetchone()
        if request_tuple:
            return self.serializer(request_tuple)
        return False

    def is_owner(self, reqid, userid):
        """To check if request belong to the user"""
        cur.execute(
            "SELECT * FROM requests WHERE id=%s", (reqid, ))
        request_tuple = cur.fetchone()
        if request_tuple[1] == userid:
            return True
        return False

    def fetch_by_userid(self, user_id):
        cur.execute(
            "SELECT * FROM requests WHERE user_id=%s", (user_id, ))
        requests_tuple = cur.fetchall()
        if requests_tuple:
            return [self.serializer(request) for request in requests_tuple]
        return "You have no requests yet"

    def fetch_by_status(self, status):
        cur.execute(
            "SELECT * FROM requests WHERE status=%s", (status, ))
        requests_tuple = cur.fetchall()
        if requests_tuple:
            return [self.serializer(request) for request in requests_tuple]
        return []

    def update(self, reqid):
        cur.execute("UPDATE requests SET category = %s, description \
            = %s, location = %s, req_date = %s WHERE id \
            = %s;", (self.category, self.description, self.location, self.req_date, reqid)
        )
        item = self.fetch_by_id(reqid)
        self.save()
        return item

    def delete(self, reqid):
        cur.execute(
            "DELETE FROM requests WHERE id=%s", (reqid, ))
        self.save()
        return "Deleted Successfully"

    def approve(self, reqid):
        """ A method to Approve requests """
        status = "Approved"
        cur.execute(
            "UPDATE requests SET status = %s WHERE id \
                = %s;", (status, reqid))
        self.save()
        return self.fetch_by_id(reqid)

    def disapprove(self, reqid):
        """ A method to Disapprove requests """
        status = "Disapproved"
        cur.execute(
            "UPDATE requests SET status = %s WHERE id \
                = %s;", (status, reqid))
        self.save()
        return self.fetch_by_id(reqid)

    def resolve(self, reqid):
        """ A method to Disapprove requests """
        status = "Resolved"
        isresolved = True
        cur.execute(
            "UPDATE requests SET status = %s, isresolved = %s WHERE id \
                = %s;", (status, isresolved, reqid))
        self.save()
        return self.fetch_by_id(reqid)

    def serializer(self, item):
        return dict(
            id=item[0],
            user_id=item[1],
            category=item[2],
            location=item[5],
            date=item[4],
            description=item[3],
            status=item[6],
            isresolved=item[7]
        )