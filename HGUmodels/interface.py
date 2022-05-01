from HGUmodels.main_session import MainSession
import os
import time

session = MainSession()

class HGUModelInterface():
    def __init__(self, address_ip, model_name, username, password, driver, dict_result):
        self._address_ip = address_ip
        self._model_name = model_name
        self._username = username
        self._password = password
        self._driver = driver
        self._dict_result = dict_result 
    

    def update_global_result_memory(self, flask_username, test_name, dict_out):
        if not session.check_username(flask_username):
            session.insert_username(flask_username)
            
        session.update_state(flask_username, test_name, dict_out)

    # desliga interfaces, exceto a referente ao HGU em teste
    def eth_interfaces_down(self):
        
        interfaces = [interface.split('\n') for interface in os.popen('ifconfig').read().split('\n\n') if interface.startswith("ens")]
        for interface in interfaces:
            ip_net =  '.'.join(self._address_ip.split('.')[:3])
            if_name = interface[0].split(':')[0]
            if any([ip_net in address for address in interface]):
                continue
            else:
                print(f'echo 4ut0m4c40 | sudo -S ip link set {if_name} down')
                os.system(f'echo 4ut0m4c40 | sudo -S ip link set {if_name} down')
                time.sleep(2)


    def eth_interfaces_up(self):
        
        interfaces = [interface.split('\n') for interface in os.popen('ifconfig -a').read().split('\n\n') if interface.startswith("ens")]
        for interface in interfaces:
            if_name = interface[0].split(':')[0]
            print(f'echo 4ut0m4c40 | sudo -S ip link set {if_name} up')
            os.system(f'echo 4ut0m4c40 | sudo -S ip link set {if_name} up')
            time.sleep(2)




