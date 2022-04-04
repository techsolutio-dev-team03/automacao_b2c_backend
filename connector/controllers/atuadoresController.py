from flask_restful import Resource
from probes import atuadoresProbe
from flask import jsonify, request
import requests


class atuadores(Resource):
    def post(self, method):
        if method == "arduinoReguaLigaDesliga":
            ip_arduino = request.json['ip_arduino']
            rele = request.json['rele']
            tempo_desligado = request.json['tempo_desligado']
            tempo_ligado = request.json['tempo_ligado']
            repeticoes = request.json['repeticoes']
            obj = atuadoresProbe.atuadores()
            ans = obj.arduinoReguaLigaDesliga(ip_arduino,rele,tempo_desligado,tempo_ligado,repeticoes)
            return jsonify(ans)
        elif method == "arduinoPressionaSimultaneo":
            ip_arduino = request.json['ip_arduino']
            rele1 = request.json['rele1']
            rele2 = request.json['rele2']
            rele3 = request.json['rele3']
            tempo = request.json['tempo']
            obj = atuadoresProbe.atuadores()
            ans = obj.arduinoPressionaSimultaneo(ip_arduino,rele1,rele2,rele3,tempo)
            return jsonify(ans)
        elif method == "arduinoMedeFreqIntermitenciaLED":
            ip_arduino = request.json['ip_arduino']
            portaAnalogica = request.json['portaAnalogica']
            medirTempoMax = request.json['medirTempoMax']
            obj = atuadoresProbe.atuadores()
            ans = obj.arduinoMedeFreqIntermitenciaLED(ip_arduino,portaAnalogica,medirTempoMax)
            return jsonify(ans)
        elif method == "arduinoMedeTempoIntermitenciaLED":
            ip_arduino = request.json['ip_arduino']
            portaAnalogica = request.json['portaAnalogica']
            tempoEsperado = request.json['tempoEsperado']
            tempoTolerancia = request.json['tempoTolerancia']
            obj = atuadoresProbe.atuadores()
            ans = obj.arduinoMedeTempoIntermitenciaLED(ip_arduino,portaAnalogica,tempoEsperado,tempoTolerancia)
            return jsonify(ans)
        elif method == "reguaAPCLigaDesliga":
            # Objetivo: liga, desliga ou verifica status da régua de alimentação. Comando executado por tomada.
            # comando: liga, desliga, status
            # tomada da régua: 1 à 8
            
            ip_regua = request.json['ip_regua']
            tomada = request.json['tomada']
            comando = request.json['comando']
            obj = atuadoresProbe.atuadores()
            ans = obj.reguaAPCLigaDesliga(ip_regua,tomada,comando)
            return jsonify(ans)
        else:
            return {"name_teste": "Doesn't Exist", "response": "none"}