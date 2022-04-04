from flask_restful import Resource
from flask import jsonify
from flask import jsonify, request
from probes import networkProbe


class network(Resource):
    def post(self, method):
        if method == 'ping':
            ip_hgu = request.json['ip']
            obj = networkProbe.network()
            ans = obj.ping(ip_hgu)
            return jsonify(ans)
        elif method == 'downloadFile':
            obj = networkProbe.network()
            ans = obj.downloadFile()
            return jsonify(ans)
        elif method == 'listConnections':
            obj = networkProbe.network()
            ans = obj.listConnections()
            return jsonify(ans)
        elif method == 'deleteConnection':
            ssid = request.json['ssid']
            obj = networkProbe.network()
            ans = obj.deleteConnection(ssid)
            return jsonify(ans)
        elif method == 'execConnection':
            ssid = request.json['ssid']
            password = request.json['password']
            obj = networkProbe.network()
            ans = obj.execConnection(ssid, password)
            return jsonify(ans)
        elif method == 'deviceShow':
            iface = request.json['interface']
            obj = networkProbe.network()
            ans = obj.deviceShow(iface)
            return jsonify(ans)
        elif method == 'listAPs':
            obj = networkProbe.network()
            ans = obj.listAPs()
            return jsonify(ans)
        elif method == 'portMirrorHPE':
            ip_switch = request.json['ip_switch']
            usuario = request.json['usuario']
            senha = request.json['senha']
            porta_origem = request.json['porta_origem']
            porta_destino = request.json['porta_destino']
            acao = request.json['acao']
            obj = networkProbe.network()
            ans = obj.portMirrorHPE(ip_switch,usuario,senha,porta_origem,porta_destino,acao)
            return jsonify(ans)
        elif method == 'portChangeVLANHPE':
            ip_switch = request.json['ip_switch']
            usuario = request.json['usuario']
            senha = request.json['senha']
            porta = request.json['porta']
            vlan = request.json['vlan']
            obj = networkProbe.network()
            ans = obj.portChangeVLANHPE(ip_switch,usuario,senha,porta,vlan)
            return jsonify(ans)
        elif method == 'execIperf':
            server = request.json['server']
            port = request.json['port']
            duration = request.json['duration']
            num_streams = request.json['num_streams']
            protocol = request.json['protocol']
            obj = networkProbe.network()
            ans = obj.execIperf(server, port, duration, num_streams, protocol)
            return jsonify(ans)
        else:
            return {"name_teste": "Doesnt Exist", "response": "none"}