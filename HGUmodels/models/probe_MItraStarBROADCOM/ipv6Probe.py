# import re
# import time
# from datetime import datetime
from ..MItraStarBROADCOM import HGU_MItraStarBROADCOM
# from json import JSONEncoder
# import json
import requests
# import sys
# import pandas as pd
# from collections import namedtuple
from ...config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
# from daos.mongo_dao import MongoConnSigleton
# from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException

# from paramiko.ssh_exception import SSHException
# import socket
# from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

# from HGUmodels import wizard_config

session = MainSession()

class HGU_MItraStarBROADCOM_ipv6Probe(HGU_MItraStarBROADCOM):

    def accessSantander_210(self, flask_username):
        site = 'http://www.santander.com.br'
        self.eth_interfaces_down()
        try:
            acesso = requests.get(site).status_code
            print(acesso)
            if acesso == 200:
                self._dict_result.update({"obs": f'Acesso a {site} ok', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Nao foi possivel acessar o site {site},  erro: {acesso}'})
        except:
            self._dict_result.update({"obs": f'Nao foi possivel acessar o site {site}'})
        finally:
            self.eth_interfaces_up()
            return self._dict_result
        
            
        
    