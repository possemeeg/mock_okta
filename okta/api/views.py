from flask import Blueprint, request, Response
from flask_restful import Resource
from flask import jsonify
import json
from okta import flask_api, flask_app, logged_in_users
from data import test_users
import secrets

api = Blueprint('api', __name__)

@api.route('/v1/authn', methods=['POST', 'OPTIONS', ])
def authn():
    if request.method == 'OPTIONS':
        opt_resp = flask_app.make_default_options_response()
        opt_resp.headers['Access-Control-Allow-Credentials'] = 'true'
        return opt_resp

    req_obj = request.get_json(True)

    user = test_users.get_user(req_obj['username'])
    session_token = secrets.token_urlsafe(32)
    logged_in_users[session_token] = {'user': user}

    resp_obj = {
            'expiresAt': '2015-11-03T10:15:57.000Z',
            'status': 'SUCCESS',
            'relayState': '/myapp/some/deep/link/i/want/to/return/to',
            'sessionToken': session_token,
            '_embedded': {
                'user': {
                    'id': user['uid'],
                    'passwordChanged': '2015-09-08T20:14:45.000Z',
                    'profile': {
                        'login': req_obj['username'],
                        'firstName': user['firstName'],
                        'lastName': user['lastName'],
                        'locale': 'en_GB',
                        'timeZone': 'Europe/London'
                        }
                    }
                }
            }
    resp = flask_app.make_response(jsonify(resp_obj))
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp


@api.route('v1/users/<uid_or_email>')
def users_get(uid_or_email):
    return jsonify(test_users.get_user(uid_or_email))

@api.route('v1/users/<uid_or_email>', methods=['DELETE'])
def users_del(uid_or_email):
    # fake it
    return jsonify({})

@api.route('v1/users/<uid_or_email>/lifecycle/deactivate', methods=['POST'])
def users_deactivate(uid_or_email):
    # fake it
    return jsonify({})
