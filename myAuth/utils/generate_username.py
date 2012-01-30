# coding: utf-8
import hashlib
import datetime, time  

# creates a random username based on the email, since the field can't be empty and must be unique    
def generate_username(email):         
    _time = str(time.mktime(datetime.datetime.now().timetuple()))
    username = hashlib.sha224(email + _time).hexdigest()[0:30]

    return username