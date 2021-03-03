from flask import make_response, request, session
from datetime import date, datetime, timedelta
from .db import db
import time
import random
import string

class security :
    def __init__(self):
        self.table = 'security'
        self.valid_duration = 60 * 10

    def get_hash(self) :
        obj_database = db()
        security_hash = self.hash_generator()
        query = ('INSERT INTO ' + self.table + ' (security_hash, security_time, security_used) VALUES (%s, %s, %s)')
        data = (security_hash, time.strftime('%Y-%m-%d %H:%M:%S'), 0)

        if obj_database.insert(query, data) != False :
            return security_hash
        else :
            return False

    def check_hash(self, hash='') :
        obj_database = db()
        query = ('SELECT * FROM ' + self.table + ' WHERE security_hash=%s AND security_used!=%s')
        data = (hash, 1, )
        security_records = obj_database.select(query, data)

        if len(security_records) > 0 :
            if int(datetime.now().timestamp()) - int(datetime.timestamp(security_records[0]['security_time'])) < self.valid_duration :
                query = ('UPDATE ' + self.table + ' SET security_used=%s WHERE security_hash=%s')
                data = (1, hash)
                obj_database.update(query, data)

                return True
            else :
                return False
        else :
            return False

    def hash_generator(self) :
        letters = string.ascii_lowercase + '1234567890'
        return ''.join(random.choice(letters) for i in range(32))
