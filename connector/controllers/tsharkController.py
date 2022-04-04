from flask_restful import Resource
from flask import jsonify, request
from probes import tsharkProbe


class captura(Resource):

    def post(self, method):
        if method == 'captureIface':
            time = request.json['time']
            interface = request.json['interface']
            path = request.json['path']
            file = request.json['file']
            obj = tsharkProbe.tsharkCapture()
            ans = obj.capture(time, interface, path, file)
            return jsonify(ans)
        elif method == 'captureCustom':
            time = request.json['time']
            interface = request.json['interface']
            path = request.json['path']
            file = request.json['file']
            filter = request.json['filter']
            obj = tsharkProbe.tsharkCapture()
            ans = obj.captureCustom(time, interface, path, file, filter)
            return jsonify(ans)
        else:
            return {"name_teste": "Doesnt Exist", "response": "none"}