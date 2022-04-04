from flask_restful import Resource
from probes import cliProbe
from flask import jsonify, request
from daos.mongo_dao import MongoConnSigleton

mongo_conn = MongoConnSigleton()

class cli(Resource):
    

    def post(self, method):

        obj = cliProbe.cli()

        #temporary fix
        username = request.get_json()['username']
        password = request.get_json()['password']
        ip = request.get_json()['ip']
        
        #Get all variables
        user_dict = {
            "username" : request.get_json()['username'],
            "password" : request.get_json()['password'],
            "ip" : request.get_json()['ip'],
            "model_name" : request.get_json()['modelo'],
            "flask_username" : request.get_json()['flask_username']
        }
       
        mongo_dict = {
            "test_battery_id" : request.get_json()['test_battery_id'],
            "caderno" : request.get_json()['caderno'],
            "test_num" : request.get_json()['test_num'],
            "test_name" : request.get_json()['test_name'],
        }

        result = getattr(obj, method)(**user_dict)
        
        test_result = result.get('result', None)
        obs = result.get('obs', None)
        ans = {'test_result': result}
        mongo_conn.update_one_test_by_id(**mongo_dict, test_result=test_result, obs=obs)
        return jsonify(ans)

        try:
            username = request.json['username']
            password = request.json['password']
        except KeyError:
            pass

        if method == 'reboot':
            ip_hgu = request.json['ip']
            username = request.json['username']
            password = request.json['password']
            
            ans = cliProbeObj.reboot(ip_hgu, username, password)
            

        elif method == 'ntpServer':

            ip = request.json['ip']
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']

            
            result = cliProbeObj.ntpServer(ip, username, password, modelo)

            test_result = result['result']
            ans = {'test_result': result}

            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)

            

        elif method == 'timeZone':
            ip = request.json['ip']
            test_battery_id = request.get_json()['test_battery_id']
            modelo = request.get_json()['modelo']
            caderno = request.get_json()['caderno']
            test_num = request.get_json()['test_num']
            test_name = request.get_json()['test_name']
            
            result = cliProbeObj.timeZone(ip, username, password, modelo)

            test_result = result['result']
            ans = {'test_result': result}

            mongo_conn.update_one_test_by_id(test_battery_id, caderno, test_name, test_num, test_result, result)
            
        elif method == 'connectSsh':
            ip_hgu = request.json['ip']
            username = request.json['username']
            password = request.json['password']
            
            ans = cliProbeObj.connectSsh(ip_hgu, username, password)
            
        elif method == 'execWget':
            ip_hgu = request.json['ip']
            username = request.json['username']
            password = request.json['password']
            url = request.json['url']
            
            ans = cliProbeObj.execWget(ip_hgu, username, password, url)
            
        elif method == 'execWput':
            ip_hgu = request.json['ip']
            username = request.json['username']
            password = request.json['password']
            url = request.json['url']
            
            ans = cliProbeObj.execWput(ip_hgu, username, password, url)
            
        elif method == 'execHGUHTTPGetFiltrar':
            ip_hgu = request.json['ip_hgu']
            user = request.json['user']
            passw = request.json['passw']
            pagina = request.json['pagina']
            filtro = request.json['filtro'] # filtro = Expressao regular
            
            ans = cliProbeObj.execHGUHTTPGetFiltrar(ip_hgu, user, passw, pagina, filtro)
            
        elif method == 'getAuthUserName':
            ip_hgu = request.json['ip']
            username = request.json['username']
            password = request.json['password']
            
            ans = cliProbeObj.getAuthUserName(ip_hgu, username, password)
            
        else:
            ans = {"name_teste": "Doesnt Exist", "response": "none"}

        return jsonify(ans)