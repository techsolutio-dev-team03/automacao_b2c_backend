from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoConnSigleton:
    
    def __init__(self, db='mongo-test-database', collection='test_batteries') -> None:
        self._client = MongoClient('mongodb://root:rootpassword@localhost:27017/')
        self._db = self._client[db]
        self._collection = self._db[collection]
        
    def get_collection(self):
        return self._collection

    def update_one_test_by_id(self, test_battery_id, caderno, test_name, test_num, test_result, obs):
        test = {
            'caderno': caderno,
            'test_name': test_name,
            'test_num': test_num,
            'test_result': test_result,
            'observation': obs
        }
        self._collection.update_one(
            {'_id': ObjectId(test_battery_id)},
            {
                '$push': {
                    'test_battery': test
                    }
            }
        )
        return None