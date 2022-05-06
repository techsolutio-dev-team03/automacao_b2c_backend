from ..MItraStarECNT import HGU_MItraStarECNT
import requests
import time
from ...config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException
from selenium.common.exceptions import UnexpectedAlertPresentException
from HGUmodels.main_session import MainSession

session = MainSession()

class HGU_MItraStarECNT_ipv6Probe(HGU_MItraStarECNT):


    #190, 191, 192
    def ipv_x_url_test(self, flask_username, test_url, ipv_x, dhcpv6):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(2)

        self.ipv_x_setting(ipv_x)
        self.dhcp_v6(dhcpv6_state = dhcpv6)
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
            self.ipv_x_setting('IPv6/IPv4 Dual Stack')
            self.dhcp_v6(True)
            self._driver.quit()
            return self._dict_result


    # 195, 196
    def ipv_x_url_test_not(self, flask_username, test_url, ipv_x, dhcpv6):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(2)

        self.ipv_x_setting(ipv_x)
        self.dhcp_v6(dhcpv6_state = dhcpv6)
        self.eth_interfaces_down()

        try:
            acesso = requests.get(test_url, timeout = 15).status_code
            print(acesso)
            if acesso == 200:
                self._dict_result.update({"obs": f'Foi possivel acessar o site {test_url}'})
            else:
                self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url}', "result":'passed', "Resultado_Probe":"OK"})
        except:
            self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url}', "result":'passed', "Resultado_Probe":"OK"})
        finally:
            self.eth_interfaces_up()
            self.ipv_x_setting('IPv6/IPv4 Dual Stack')
            self.dhcp_v6(True)
            self._driver.quit()
            return self._dict_result