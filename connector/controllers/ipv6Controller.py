from flask_restful import Resource, reqparse
from flask import jsonify, request
from daos.mongo_dao import MongoConnSigleton
from probes import ipv6Probe


mongo_conn = MongoConnSigleton()


class ipv6(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ip', type=str)

    def get(self, method):
        pass

    def post(self, method):

        obj = ipv6Probe.Ipv6()

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
        print(result)
        
        test_result = result.get('result', None)
        obs = result.get('obs', None)
        ans = {'test_result': result}
        mongo_conn.update_one_test_by_id(**mongo_dict, test_result=test_result, obs=obs)
        return jsonify(ans)