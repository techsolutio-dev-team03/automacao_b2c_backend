from re import S
from ..AskeyBROADCOM import HGU_AskeyBROADCOM
import requests
import time
from ...config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException
from selenium.common.exceptions import UnexpectedAlertPresentException
from HGUmodels.main_session import MainSession
import datetime
from skpy import Skype
import iperf3
import os

session = MainSession()

class HGU_AskeyBROADCOM_ipv6Probe(HGU_AskeyBROADCOM):

    # 172
    def ipv6_wan_enabled(self, flask_username, url_list, ipv_x, dhcpv6):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(5)

        self.ipv_x_setting(ipv_x)
        self.dhcp_v6(dhcpv6_state = dhcpv6)
        self.dhcp_stateless()
        self.eth_interfaces_down()
        
        url_request_result = []
        for url in url_list:
            try:
                acesso = requests.get(url, timeout = 15).status_code
                print(f"Res. acesso ao site {url}: {acesso}" )
                if acesso == 200:
                    url_request_result.append(True)
                else:
                    url_request_result.append(False)
                    break
            except:
                print(f"Res. acesso ao site {url}: erro" )
                url_request_result.append(False)
                break
            
        if all(url_request_result):
            self._dict_result.update({"obs": f'Foi possivel acessar todos os sites', "result":'passed', "Resultado_Probe":"OK"})
        else:
            self._dict_result.update({"obs": f'Nao foi possivel acessar todos os sites'})

        self.eth_interfaces_up()
        self._driver.quit()
        return self._dict_result
 
 
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
            self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
            self.dhcp_v6(True)
            self._driver.quit()
            return self._dict_result


  # 193
    def connectSkype_193(self, flask_username,  ipv_x, dhcpv6):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(5)
        self.ipv_x_setting(ipv_x)
        self.dhcp_v6(dhcpv6_state = dhcpv6)
        self.eth_interfaces_down()
        data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            sk = Skype('dev.team05@techsolutio.com' , 'Techsolutio@123')
            time.sleep(3)
            ch = sk.chats.create(admins=("Dev05 Techsolutio")) #sk.contacts['echo123'].chat
            msg_enviada = f"Teste Skype por {flask_username} em {data} no {self._model_name}"
            print(msg_enviada)
            ch.sendMsg(msg_enviada)
            time.sleep(5)
            msg_recebida = ch.getMsgs()[0].content
            print('\n', msg_recebida)
            if msg_recebida == msg_enviada:
                self._dict_result.update({"obs": f'Conexao com skype OK', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Conexao com skype NOK'}) 
        except:
            self._dict_result.update({"obs": f'Conexao com skype NOK'}) 
        self.eth_interfaces_up()
        self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
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
            self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
            self.dhcp_v6(True)
            self._driver.quit()
            return self._dict_result


    # 203
    def ipv4ExecIperf_203(self, flask_username, iperf_server, ipv_x, dhcpv6):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(5)

        self.ipv_x_setting(ipv_x)
        self.dhcp_v6(dhcpv6_state = dhcpv6)
        self.eth_interfaces_down()

        try:
            client = iperf3.Client()
            client.server_hostname = iperf_server
            client.verbose = True
            resultado = client.run()
            #print(resultado.json)
            if resultado.error == None:
                self._dict_result.update({"obs": f'Conexao: Cliente Iperf - Server {iperf_server} realizado com sucesso. Enviado {resultado.sent_Mbps} Mbps; Recebido {resultado.received_Mbps} Mbps', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Falha na Conexao: Cliente Iperf - Server {iperf_server}, erro: {resultado.error}'})
        except:
            self._dict_result.update({"obs": f'Falha no teste Iperf'})
        finally:
            self.eth_interfaces_up()
            self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
            self.dhcp_v6(True)
            self._driver.quit()
            return self._dict_result


    # 212
    def ipv4DownloadCentOS_212(self, flask_username, iperf_server, ipv_x, dhcpv6):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(5)

        self.ipv_x_setting(ipv_x)
        self.dhcp_v6(dhcpv6_state = dhcpv6)
        self.eth_interfaces_down()

        try:
            os.system('wget --tries=2 -O ~/Downloads/CentOS http://mirror.ufscar.br/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-Minimal-2009.iso')
            os.system('wget --tries=2 -O ~/Downloads/CentOS-sha http://mirror.ufscar.br/centos/7.9.2009/isos/x86_64/sha256sum.txt')
            with open(os.path.expanduser("~")+'/Downloads/CentOS-sha') as file:
                sha256sum_list = file.readlines()
            sha256sum = [sha.split(' ')[0] for sha in sha256sum_list if 'Minimal' in sha]
            sha256sum_download = os.popen('sha256sum '+os.path.expanduser("~")+'/Downloads/CentOS').read().split(' ')[0]
            if sha256sum_download == sha256sum[0]:
                self._dict_result.update({"obs": 'Download do CentoOS realizado com sucesso', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": 'Falha no download do CentoOS'})
        except:
            self._dict_result.update({"obs": f'Falha no teste de Download'})
        finally:
            os.system('rm '+os.path.expanduser("~")+'/Downloads/CentOS')
            os.system('rm '+os.path.expanduser("~")+'/Downloads/CentOS-sha')
            self.eth_interfaces_up()
            self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
            self.dhcp_v6(True)
            self._driver.quit()
            return self._dict_result