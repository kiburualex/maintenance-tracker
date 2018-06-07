# used to to validate event names
import re
from datetime import date, datetime
from connect import conn
import uuid
from flask import session


class Services(object):
    """ A class to handle actions related to requests"""

    def __init__(self):
        """define an empty list to hold all the requests objects"""
        self.request_lists = []

    def existing_request(self, category, user_id, date):
        """A method to check if a request has already been placed"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM requests WHERE category \
        = %s AND user_id = %s AND req_date = %s;", (category,
                                                    user_id, date,))
        cat = cur.fetchone()
        if cat:
            return True
        else:
            return False

    def valid_description(self, description):
        """check description length and special characters"""
        if len(description) < 10 or not re.match("^[a-zA-Z0-9_ ]*$",
                                                 description):
            return False
        else:
            return True

    def valid_category(self, category):
        """check category provided if maintenance or repair"""
        if category == "maintenance" or category == "repair" or \
                category == "Maintenance" or category == "Repair":
            return True
        else:
            return False

    def valid_date(self, re_date):
        """Check if the given date is less than the current date"""
        date = datetime.strptime(re_date, '%Y-%m-%d').date()
        if date < date.today():
            return False
        return True

    def create(self, category, description, location, date, time, userid):
        """A method for creating a new request"""
        self.request_details = {}
        if self.valid_category(category):
            if self.existing_request(category, userid, date):
                return "Request Already exists"
            else:
                # validate event name
                if not self.valid_description(description):
                    return "description too short or invalid"
                else:
                    status = "Pending"
                    user_id = userid
                    req_date = date
                    req_time = time
                    isresolved = False

                    cur = conn.cursor()
                    cur.execute("INSERT INTO requests(user_id, category,\
                     location, req_date, req_time, description, status,\
                      isresolved) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (user_id, category, location, req_date,
                                 req_time, description, status, isresolved))
                    conn.commit()
                    return "Request Sent"
        return "Invalid Category. Category should either \
        be maintenance or repair"

    def view_all(self, user_id, role):
        """ A method to return a list of all requests"""

        request_list = []
        cur = conn.cursor()
        if role == "Admin":
            cur.execute("SELECT * FROM requests ;")
            requests = cur.fetchall()
            for item in requests:
                request = dict(
                    id=item[0],
                    user_id=item[1],
                    category=item[2],
                    location=item[3],
                    date=item[4],
                    description=item[6],
                    status=item[7],
                    isresolved=item[8]
                )
                request_list.append(request)
            return request_list
        else:
            cur.execute(
                "SELECT * FROM requests WHERE user_id = %s;", (user_id,))
            requests = cur.fetchall()
            for item in requests:
                request = dict(
                    id=item[0],
                    user_id=item[1],
                    category=item[2],
                    location=item[3],
                    date=item[4],
                    description=item[6],
                    status=item[7],
                    isresolved=item[8]
                )
                request_list.append(request)
            return request_list

    def find_by_id(self, reqid):
        """A method to find a request given an id"""
        self.request_details = {}
        self.request_list = []
        cur = conn.cursor()
        cur.execute("SELECT * FROM requests WHERE id=%s;", (reqid,))
        item = cur.fetchone()
        if item:
            self.request_details['description'] = item[6]
            self.request_details['category'] = item[2]
            self.request_details['location'] = item[3]
            self.request_details['date'] = item[4].isoformat()
            self.request_details['time'] = item[5].isoformat()
            self.request_details['status'] = item[7]
            self.request_details['user_id'] = item[1]
            self.request_details['id'] = item[0]
            self.request_details['isresolved'] = item[8]
            self.request_list.append(self.request_details)
            return self.request_list
        return "Request Doesnt Exist"

    def update(self, reqid, category, description, location, date, time):
        """ Find a request with the given id and update its details"""

        if self.request_exist_by_id(reqid):
            cur = conn.cursor()
            cur.execute("UPDATE requests SET category = %s, description \
            = %s, location = %s, req_date = %s, req_time = %s WHERE id \
            = %s;", (category, description, location, date, time, reqid))
            conn.commit()
            return "update success"
        else:
            return "no request with given id"

    def request_exist_by_id(self, reqid):
        """A method to check if a request exists"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM requests WHERE id=%s;", (reqid,))
        req = cur.fetchone()
        if req:
            return True
        else:
            return False

    def is_resolved(self, reqid):
        """A method to check if a request has been resolved"""
        cur = conn.cursor()
        cur.execute("SELECT * FROM requests WHERE id=%s;", (reqid,))
        req = cur.fetchone()
        if req[8] is True:
            return True
        else:
            return False

    def resolve(self, reqid):
        """ A method to resolve requests """
        try:
            status = "Resolved"
            isresolved = True
            cur = conn.cursor()
            cur.execute("UPDATE requests SET status = %s, isresolved \
            = %s WHERE id = %s;", (status, isresolved, reqid))
            conn.commit()
            return True
        except Exception:
            return False

    def approve(self, reqid):
        """ A method to rApprove requests """
        try:
            status = "Approved"
            cur = conn.cursor()
            cur.execute(
                "UPDATE requests SET status = %s WHERE id \
                 = %s;", (status, reqid))
            conn.commit()
            return True
        except Exception:
            return False

    def disapprove(self, reqid):
        """ A method to disapprove requests """
        try:
            status = "Disapproved"
            isresolved = True
            cur = conn.cursor()
            cur.execute("UPDATE requests SET status = %s,\
             isresolved = %s WHERE id = %s;",
                        (status, isresolved, reqid))
            conn.commit()
            return True
        except Exception:
            return False
