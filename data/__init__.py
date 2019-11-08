from flask import json
from okta import flask_app

class TestUsers(object):
    def __init__(self):
        with open(flask_app.config['CR_TEST_USERS'], 'r') as f:
            self.users = json.loads(f.read())

    def get_user(self, uid_or_email):
        ret = {v['id']: v for k, v in self.users.items()}.get(uid_or_email) or \
            {v['email']: v for k, v in self.users.items()}.get(uid_or_email)
        print('Ret:', ret)
        return ret


test_users = TestUsers()
