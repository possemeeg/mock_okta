from flask import json
from okta import flask_app
import pandas
from itertools import count
import random
from time import sleep
import pprint


class TestUsers(object):
    def __init__(self):
        memcsv = pandas.read_csv(flask_app.config['CR_TEST_USERS'])
        keys = {k:ind for k, ind in zip(memcsv.keys(), count(1))}
        def make_user(row, ind):
            def get(key):
                return row[keys[key]]

            uid = get('id')
            email = get('email')
            firstname = get('firstname')
            lastname = get('lastname')
            return {
                'active': True,
                'scopes': '',
                'uid': uid,
                'sub': uid,
                'id': uid,
                'username': email,
                'email': email,
                'firstName': firstname,
                'lastName': lastname,
                'profile': {
                    'firstName': firstname,
                    'lastName': lastname,
                    'email': email,
                    'login': email,
                    'clubResultsAdmin': get('admin') == 'true'
                }
            }

        self.users = {u['uid']: u for u in map(lambda t : make_user(t[0], t[1]), zip(memcsv.itertuples(), count()))}

    def get_user(self, uid_or_email):
        ret = {v['id']: v for k, v in self.users.items()}.get(uid_or_email) or \
            {v['profile']['email'].lower(): v for k, v in self.users.items()}.get(uid_or_email.lower())
        pprint.pprint(ret)
        sleep(0.1)
        return ret


test_users = TestUsers()
