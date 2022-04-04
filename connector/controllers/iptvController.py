from flask_restful import Resource, reqparse
from flask import jsonify, request
from probes import iptvProbe
import requests


class iptv(Resource):
    def post(self, method):
        if method == "checkSTBIPPool":
            cenario = request.json['cenario']
            stb = request.json['stb']
            obj = iptvProbe.iptv()
            ans = obj.checkSTBIPPool(cenario, stb)
            return jsonify(ans)

        elif method == "timeToService":
            # test cases: 681, 682, 683, 685, 686, 688, 689, 691, 693, 700, 701,
            cenario = request.json['cenario']
            elementoEmTeste = request.json['elementoEmTeste']
            elementoId = request.json['elementoId']
            evento = request.json['evento']
            tempo_maximo = request.json['tempo_maximo']
            obj = iptvProbe.iptv()
            ans = obj.timeToService(cenario, elementoEmTeste, elementoId, evento, tempo_maximo)
            return jsonify(ans)