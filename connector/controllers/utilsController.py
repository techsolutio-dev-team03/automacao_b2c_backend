from itsdangerous import json
from flask_restful import Resource, reqparse
from flask import jsonify, request
from probes import iptvProbe
import requests
from HGUmodels.main_session import MainSession

class utils(Resource):
    def post(self, method):
        flask_username = request.get_json()['flask_username']

        if method == "clear_cache":
            session = MainSession()
            try:
                session.clear_cache_by_user(flask_username)
            except Exception:
                return jsonify({'obs': 'main session cache clear error'})
            else:
                return jsonify({'obs':'ok'})