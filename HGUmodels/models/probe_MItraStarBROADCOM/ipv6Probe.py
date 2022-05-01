# import re
import time
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
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException

# from paramiko.ssh_exception import SSHException
# import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

# from HGUmodels import wizard_config

session = MainSession()

class HGU_MItraStarBROADCOM_ipv6Probe(HGU_MItraStarBROADCOM):

    def ipv6_only_url_test(self, flask_username, test_url):

        self.ipv6_only_setting()
        self.eth_interfaces_down()

        try:
            acesso = requests.get(test_url).status_code
            print(acesso)
            if acesso == 200:
                self._dict_result.update({"obs": f'Acesso a {test_url} ok', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url},  erro: {test_url}'})
        except:
            self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url}'})
        finally:
            self.ipv4_ipv6_setting()
            self._driver.quit()
            self.eth_interfaces_up()
            return self._dict_result
        
            
        
    