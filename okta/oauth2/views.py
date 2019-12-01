from flask import Blueprint, redirect, request, make_response, jsonify
from flask_restful import Resource
import urllib.parse as urlp
from data import test_users
from okta import flask_api, flask_app, logged_in_users
import jwt
import time
import re

TOK_PREFIX = 'ac_toc_'
TOK_RE = re.compile(f'^{TOK_PREFIX}(.*)')
def _sess_from_tok(sess):
    token_match = TOK_RE.match(sess)
    return token_match and token_match.group(1)

oauth2 = Blueprint('oauth2', __name__)

@oauth2.route('/v1/authorize')
def authorize():
    session_token = request.args['sessionToken']
    user = logged_in_users[session_token]
    state = request.args['state']
    red_url = request.args['redirect_uri'] + f'?{urlp.urlencode({"code":session_token, "state":state})}'
    return redirect(red_url)

@oauth2.route('/v1/token', methods=['POST',])
def token():
    session_token = request.form.get('code')
    user_rec = logged_in_users[session_token]
    resp = user_rec['user'].copy()
    resp['access_token'] = f'{TOK_PREFIX}{session_token}'
    token = {
            'hd': 'stuff',
            'sub': resp['uid'],
            'iss': 'http://localhost:5003/oauth2/default',
            'aud': ['dummy'],
            'azp': 'dummy',
            'exp': time.time() + 60*60*60,
            'iat': time.time()
            }
    resp['id_token'] = jwt.encode(token, 'sdssd', algorithm='HS256').decode()
    user_rec['token'] = token
    return jsonify(resp)

@oauth2.route('/v1/introspect', methods=['POST',])
def tokeintrospection():
    session_token = _sess_from_tok(request.form['token'])
    user_rec = logged_in_users[session_token]
    token = user_rec['token']
    resp = {
            'active': True,
            'token_type': 'Bearer',
            'scope': 'openid profile',
            'client_id': 'dummy',
            'username': user_rec['user']['profile']['email'],
            'exp': token['exp'],
            'iat': token['iat'],
            'sub': token['sub'],
            'aud': token['aud'][0],
            'iss': token['iss'],
            'jti': 'AT.7P4KlczBYVcWLkxduEuKeZfeiNYkZIC9uGJ28Cc-YaI',
            'uid': token['sub'],
            }
    return jsonify(resp)


@oauth2.route('/v1/userinfo')
def userinfo():
    session_tokens = request.headers['Authorization'].split()
    if len(session_tokens) < 2:
        return make_response(jsonify({}), 401)

    session_token = _sess_from_tok(session_tokens[1])
    user_rec = logged_in_users[session_token]

    return jsonify(user_rec['user'])

