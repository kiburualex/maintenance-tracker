import jwt
import os
from flask import current_app
from datetime import datetime, timedelta
from connect import conn


class Jwt_details(object):

    @staticmethod
    def generate_auth_token(userid):
        """a method to generate the access token"""
        try:
            # set up a payload
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': userid
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                os.environ.get('SECRET_KEY', "itsasecret"),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as error:
            # return an error in string format if an exception occurs
            return str(error)

    @staticmethod
    def decode_auth_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error message
            return "You were logged out. Please login"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error message
            return "Please register or login"

    @staticmethod 
    def blacklist_token(token):
        """Blacklist tokens"""
        try:
            blacklisted_on = datetime.now()
            cur = conn.cursor()
            cur.execute("INSERT INTO blacklist_tokens(token, blacklisted_on)\
            VALUES (%s, %s) RETURNING id;",
                        (token, blacklisted_on))
            conn.commit()
            return True
        except Exception as e:
            return e

    @staticmethod
    def is_blacklisted(token):
        """Check if is blacklisted """
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM blacklist_tokens WHERE token = %s;",
                (token,))
            items = cur.fetchone()
            if items:
               return True
            else: 
                return False
        except Exception:
            return False                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           