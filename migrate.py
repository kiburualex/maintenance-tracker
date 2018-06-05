import psycopg2 
import os
from passlib.hash import sha256_crypt


def migrate():
    dbname = os.getenv("DBNAME", "testdb")
    dbuser = os.getenv("DBUSER", "postgres")
    dbpass = os.getenv("PASSWORD", "root123")
    dbhost = os.getenv("DBHOST", "localhost")

    
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("DROP TABLE IF EXISTS requests")
        cur.execute("CREATE TABLE users(id serial PRIMARY KEY, name varchar, username varchar, role varchar, password varchar);")
        cur.execute("CREATE TABLE requests(id serial PRIMARY KEY, user_id integer, category varchar, date date, time time, description varchar, status varchar);")
        password = sha256_crypt.encrypt("pass123")
        cur.execute("INSERT INTO users(name, username, role, password) VALUES (%s, %s, %s, %s)",("Desmond Korir", "dess", "Admin", password))
        cur.execute("SELECT * FROM users")
        items = cur.fetchall()
        print(items)
        conn.commit()

    except:
        print "I am unable to connect to the database"
    


migrate()