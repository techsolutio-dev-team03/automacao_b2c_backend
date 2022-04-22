import re
import time
from datetime import datetime
from ..MitraStarECNT import HGU_MItraStarECNT
from json import JSONEncoder
import json
import requests
import sys
import pandas as pd
from collections import namedtuple
from ...config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException

from paramiko.ssh_exception import SSHException
import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config

session = MainSession()

mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()


class HGU_MItraStarECNT_functionalProbe(HGU_MItraStarECNT):

    def connectFakeWizard_68(self, flask_username):

        site1 = "http://{address_ip}/wancfg.cmd?action=view".format(address_ip=self._address_ip)
        
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('site1 = ' + site1)
        print('-=-' * 20)
        try:
            print('\n\n == Abrindo URL ' + site1 + ' == ')
            self._driver.get(site1)
            time.sleep(5)
            print('\n\n == Aguardando redirecionamento de página == ')
            if self._driver.find_element_by_xpath('/html/body/h4'):
                result = self._driver.find_element_by_xpath('/html/body/h4').text
                print(result)
            time.sleep(1)
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": None})
        except NoSuchElementException as exception:
            print(exception)
            self._driver.quit()
            self._dict_result.update({"obs": str(exception)})
        finally:
            return self._dict_result