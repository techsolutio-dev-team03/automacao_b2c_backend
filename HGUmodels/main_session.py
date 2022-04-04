
class MainSession:
    __instance = None
    def __new__(cls, dict_test_memory=None):
        if MainSession.__instance is None:
            MainSession.__instance = object.__new__(cls)
        MainSession.__instance._dict_test_memory = dict_test_memory
        return MainSession.__instance

    def __init__(self):
        self._dict_test_memory = {}

    def update_state(self, flask_username, test_name, dict_out):
        username_exist = self._dict_test_memory.get(flask_username, None)
        if username_exist:
            self._dict_test_memory[flask_username].update({test_name: dict_out})
        else:
            self._dict_test_memory.update({flask_username:{test_name: dict_out}})

    def insert_username(self, flask_username):
        self._dict_test_memory.update({flask_username: {}})

    def check_username(self, flask_username):
        return flask_username in self._dict_test_memory

    def get_result_from_test(self, flask_username, test_name):
        try:
            return self._dict_test_memory[flask_username][test_name]
        except KeyError:
            return {}

    def clear_cache_by_user(self, flask_username):
        self._dict_test_memory.update({flask_username: {}})
