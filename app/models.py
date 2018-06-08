import psycopg2
import os
import re
from urlparse import urlparse
from connect import conn
from passlib.hash import sha256_crypt

class Store(object):
    def __init__(self):
        self.conn = conn
        self.cur = self.conn.cursor()

    def create_table(self, script):
        self.cur.execute(script)
        self.save()

    def drop_table(self, table_name):
        self.cur.execute('DROP TABLE IF EXISTS ' + table_name)
        self.save()

    def save(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

class User(Store):
    def __init__(self,username=None, email=None, password=None):
        super(User, self).__init__()
        self.role = "Normal"
        self.username = username
        self.email = email
        self.password = password

    def create(self):
        self.create_table("CREATE TABLE users(id serial PRIMARY KEY, email varchar\
          NOT NULL UNIQUE, username varchar NOT NULL UNIQUE, role varchar NOT NULL,\
           password varchar NOT NULL);"
        )

    def add(self):
        if self.username_exist(self.username) is False:
            hash_pass = self.hash_password(self.password)
            self.cur.execute(
                """
                INSERT INTO users (username, email, role, password)
                VALUES (%s , %s, %s, %s) RETURNING id;
                """,
                (self.username, self.email, self.role, hash_pass))
            id = self.cur.fetchone()[0]
            self.save()
            
            return self.user_by_id(id)
        return "Username Is already taken"

    def fetch_all(self):
        self.cur.execute("SELECT * FROM users")
        users_tuple = self.cur.fetchall()
        users = []

        for user in users_tuple:
            users.append(self.serializer(user))

        return users


    def find_by_username(self, username):
        self.cur.execute(
            "SELECT * FROM users where username=%s", (username, ))

        user = self.cur.fetchone()

        if user:
            return self.serializer(user)
        return False

    def serializer(self, user):
        return dict(
            id=user[0],
            username=user[1],
            name=user[2],
            email=user[3],
            password=user[4]
        )

    def username_exist(self, username):
        """ check if user with the same username already exist """
        self.cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
        user = self.cur.fetchone()
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
        self.cur.execute("SELECT * FROM users WHERE id = %s;", (id,))
        user = self.cur.fetchone()
        
        return self.serialiser_user(user)

