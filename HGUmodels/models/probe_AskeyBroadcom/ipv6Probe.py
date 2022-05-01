from ..AskeyBROADCOM import HGU_AskeyBROADCOM
import requests
from ...config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException
from selenium.common.exceptions import UnexpectedAlertPresentException
from HGUmodels.main_session import MainSession

session = MainSession()

class HGU_AskeyBROADCOM_ipv6Probe(HGU_AskeyBROADCOM):

    def ipv6_only_url_test(self, flask_username, test_url):

        self.ipv6_only_setting()
        self.eth_interfaces_down()

        try:
            acesso = requests.get(test_url, timeout = 15).status_code
            print(acesso)
            if acesso == 200:
                self._dict_result.update({"obs": f'Acesso a {test_url} ok', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url},  erro: {test_url}'})
        except:
            self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url}'})
        finally:
            self.eth_interfaces_up()
            self.ipv4_ipv6_setting()
            self._driver.quit()
            return self._dict_result