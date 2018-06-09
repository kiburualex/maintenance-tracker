import psycopg2
import os
from urlparse import urlparse

dbname = os.getenv("DBNAME", "testdb")
dbuser = os.getenv("DBUSER", "postgres")
dbpass = os.getenv("PASSWORD", "root123")
dbhost = os.getenv("DBHOST", "localhost")
DATABASE_URL = os.getenv('DATABASE_URL')

try:
    if os.getenv("FLASK_CONFIG") == "development":
        conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
    elif os.getenv("FLASK_CONFIG") == "production":
        conn = psycopg2.connect(DATABASE_URL)
    else:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpass)

except:
    print "I am unable to connect to the database"
