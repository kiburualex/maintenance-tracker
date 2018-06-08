import psycopg2 
import os
from passlib.hash import sha256_crypt
from connect import conn


def migrate():

    
    try:
        
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS requests")
        cur.execute("CREATE TABLE users(id serial PRIMARY KEY, email varchar,\
         username varchar, role varchar, password varchar);")
        cur.execute("CREATE TABLE requests(id serial PRIMARY KEY, user_id integer, \
        category varchar, location varchar, req_date date, req_time time, description varchar, \
        status varchar, isresolved boolean);")
        password = sha256_crypt.encrypt("pass123")
        cur.execute("INSERT INTO users(email, username, role, password) VALUES (%s, %s, %s, %s)",\
        ("root@gmail.com", "dess", "Admin", password))
        cur.execute("SELECT * FROM users")
        items = cur.fetchall()
        print(items)
        conn.commit()

    except:
        print "I am unable to connect to the database here"
    


migrate()