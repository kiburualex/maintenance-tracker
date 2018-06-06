import psycopg2 
import os

dbname = os.getenv("DBNAME", "testdb")
dbuser = os.getenv("DBUSER", "postgres")
dbpass = os.getenv("PASSWORD", "root123")
dbhost = os.getenv("DBHOST", "localhost")
try:
    conn = psycopg2.connect(dbname=dbname, user=dbuser, host=dbhost, password=dbpass)
except:
    print "I am unable to connect to the database"

