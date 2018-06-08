import psycopg2
import os


try:
    if os.getenv("FLASK_CONFIG") == "development":
        dbname = os.getenv("DBNAME", "testdb")
        dbuser = os.getenv("DBUSER", "postgres")
        dbpass = os.getenv("PASSWORD", "root123")
        dbhost = os.getenv("DBHOST", "localhost")
        conn = psycopg2.connect(
            dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    elif os.getenv("FLASK_CONFIG") == "testing":
        dbname = os.getenv("DBNAME", "testdb")
        dbuser = os.getenv("DBUSER", "postgres")
        dbpass = os.getenv("PASSWORD", "root123")
        dbhost = os.getenv("DBHOST", "localhost")
        conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpass)
    else:
        dbname = os.getenv("DBNAME", "mtracker")
        dbuser = os.getenv("DBUSER", "postgres")
        dbpass = os.getenv("PASSWORD", "root123")
        dbhost = os.getenv("DBHOST", "localhost")
        conn = psycopg2.connect(
            dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
except:
    print "I am unable to connect to the database"
