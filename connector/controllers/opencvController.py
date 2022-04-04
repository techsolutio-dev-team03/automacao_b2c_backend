from flask_restful import Resource, reqparse
from flask import jsonify, request
from probes import opencvProbe

class opencv(Resource):
    def post(self, method):
        if method == "aguardaTela":
            stbID = request.json['stbID']
            criterio = request.json['criterio']
            tempo_maximo = request.json['tempo_maximo']
            obj = opencvProbe.opencv()
            ans = obj.aguardaTela(stbID, criterio, tempo_maximo)
            return jsonify(ans)

