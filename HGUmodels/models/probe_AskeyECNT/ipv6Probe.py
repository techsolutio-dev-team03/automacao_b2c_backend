from ..AskeyECNT import HGU_AskeyECNT
import time
import requests
from ...config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException
from selenium.common.exceptions import UnexpectedAlertPresentException
from HGUmodels.main_session import MainSession
import datetime
import pyshark
from skpy import Skype
import iperf3
import os
import subprocess
import paramiko
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException
from paramiko.ssh_exception import SSHException

session = MainSession()

class HGU_AskeyECNT_ipv6Probe(HGU_AskeyECNT):

    # 172
    # def ipv6_wan_enabled(self, flask_username, url_list, ipv_x, dhcpv6):
    #     self._driver.get('http://' + self._address_ip + '/padrao')
    #     self.login_support()
    #     time.sleep(5)

    #     self.ipv_x_setting(ipv_x)
    #     self.dhcp_v6(dhcpv6_state = dhcpv6)
    #     self.dhcp_stateless()
    #     self.eth_interfaces_down()
        
    #     url_request_result = []
    #     for url in url_list:
    #         try:
    #             acesso = requests.get(url, timeout = 15).status_code
    #             print(f"Res. acesso ao site {url}: {acesso}" )
    #             if acesso == 200:
    #                 url_request_result.append(True)
    #             else:
    #                 url_request_result.append(False)
    #                 break
    #         except:
    #             print(f"Res. acesso ao site {url}: erro" )
    #             url_request_result.append(False)
    #             break
            
    #     if all(url_request_result):
    #         self._dict_result.update({"obs": f'Foi possivel acessar todos os sites', "result":'passed', "Resultado_Probe":"OK"})
    #     else:
    #         self._dict_result.update({"obs": f'Nao foi possivel acessar todos os sites'})

    #     self.eth_interfaces_up()
    #     self._driver.quit()
    #     return self._dict_result


    # #190, 191, 192 - Fora de escopo
    # def ipv_x_url_test(self, flask_username, test_url, ipv_x, dhcpv6):
    #     self._driver.get('http://' + self._address_ip + '/padrao')
    #     self.login_support()
    #     time.sleep(5)

    #     self.ipv_x_setting(ipv_x)
    #     self.dhcp_v6(dhcpv6_state = dhcpv6)
    #     self.eth_interfaces_down()

    #     try:
    #         acesso = requests.get(test_url, timeout = 15).status_code
    #         print(acesso)
    #         if acesso == 200:
    #             self._dict_result.update({"obs": f'Acesso a {test_url} ok', "result":'passed', "Resultado_Probe":"OK"})
    #         else:
    #             self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url},  erro: {test_url}'})
    #     except:
    #         self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url}'})
    #     finally:
    #         self.eth_interfaces_up()
    #         self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
    #         self.dhcp_v6(True)
    #         self._driver.quit()
    #         return self._dict_result


    # # 195, 196 - Fora de escopo
    # def ipv_x_url_test_not(self, flask_username, test_url, ipv_x, dhcpv6):
    #     self._driver.get('http://' + self._address_ip + '/padrao')
    #     self.login_support()
    #     time.sleep(5)

    #     self.ipv_x_setting(ipv_x)
    #     self.dhcp_v6(dhcpv6_state = dhcpv6)
    #     self.eth_interfaces_down()

    #     try:
    #         acesso = requests.get(test_url, timeout = 15).status_code
    #         print(acesso)
    #         if acesso == 200:
    #             self._dict_result.update({"obs": f'Foi possivel acessar o site {test_url}'})
    #         else:
    #             self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url}', "result":'passed', "Resultado_Probe":"OK"})
    #     except:
    #         self._dict_result.update({"obs": f'Nao foi possivel acessar o site {test_url}', "result":'passed', "Resultado_Probe":"OK"})
    #     finally:
    #         self.eth_interfaces_up()
    #         self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
    #         self.dhcp_v6(True)
    #         self._driver.quit()
    #         return self._dict_result


    # # 203 - Fora de escopo
    # def ipv4ExecIperf_203(self, flask_username, iperf_server, ipv_x, dhcpv6):
    #     self._driver.get('http://' + self._address_ip + '/padrao')
    #     self.login_support()
    #     time.sleep(5)

    #     #self.ipv_x_setting(ipv_x)
    #     #self.dhcp_v6(dhcpv6_state = dhcpv6)
    #     self.eth_interfaces_down()

    #     try:
    #         client = iperf3.Client()
    #         client.server_hostname = iperf_server
    #         resultado = client.run()
    #         print(resultado.json)
    #         if resultado.error == None:
    #             self._dict_result.update({"obs": f'Conexao: Cliente Iperf - Server {iperf_server} realizado com sucesso. Enviado {resultado.sent_Mbps:.2f} Mbps; Recebido {resultado.received_Mbps:.2f} Mbps', "result":'passed', "Resultado_Probe":"OK"})
    #         else:
    #             self._dict_result.update({"obs": f'Falha na Conexao: Cliente Iperf - Server {iperf_server}, erro: {resultado.error}'})
    #     except:
    #         self._dict_result.update({"obs": f'Falha no teste Iperf'})
    #     finally:
    #         self.eth_interfaces_up()
    #         self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
    #         self.dhcp_v6(True)
    #         self._driver.quit()
    #         return self._dict_result


    # 212
    def ipv4DownloadCentOS_212(self, flask_username, ipv_x, dhcpv6):
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


    # 218
    def connectSkype_218(self, flask_username,  ipv_x, dhcpv6):
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
        # self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
        # self.dhcp_v6(True)
        self._driver.quit()
        return self._dict_result


    # 230
    def iPerf2PCsClientServer_230(self, flask_username,  ipv_x, dhcpv6):
        # self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
        # self.login_support()
        # time.sleep(3)
        # self.ipv_x_setting(ipv_x)
        # self.dhcp_v6(dhcpv6_state = dhcpv6)
        # self.eth_interfaces_down()
        
        # Encontra o ip da maquina local:
        network = '.'.join(self._address_ip.split('.')[:3])
        ip_maq = os.popen(f'ifconfig | grep {network}').read().strip(' ').split(' ')[1]
        print(ip_maq)
        
        # Encontra o ip da maquina remota
        try:
            ips = os.popen(f'nmap -sP {self._address_ip}/24').readlines()
            ips = [ip.split(' ')[-1].strip(' \n()') for ip in ips if network in ip]
            ip_remoto_list = []
            for ip in ips:
                if ip != ip_maq and ip != network+'.1' and ip != network+'.100' and ip != network+'.230':
                    ip_remoto_list.append(ip)
            print(ip_remoto_list)
        except Exception as e:
            print(e)

        # Conecta com a maquina remota via ssh e configura como server do IPerf
        for ip_remoto in ip_remoto_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_remoto, username='automacao', password='4ut0m4c40', timeout=2)
                teste = ssh.invoke_shell()
                teste.send('iperf3 -s \n')
                time.sleep(2)
                output = teste.recv(65000).decode('utf-8')
                print(ip_remoto)
                print(output)
                break
            except Exception as e:
                print(e)
                continue
        else:
            print(e)
            self._dict_result.update({"obs": f'Falha na Conexao ssh com {ip_remoto}: verifique as configuracoes de usuario, senha e firewall'})
            return self._dict_result  

        # Executa o teste IPerf como cliente
        try:
            client = iperf3.Client()
            client.server_hostname = ip_remoto
            client.protocol = 'tcp'
            resultado = client.run()
            print(resultado.error)
            if resultado.error == None:
                self._dict_result.update({"obs": f'IPerf: Cliente local -> Server remoto realizado com sucesso. Transmissao {resultado.sent_Mbps:.2f} Mbps; Recepcao {resultado.received_Mbps:.2f} Mbps', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Falha na Conexao: Cliente Iperf - Server , erro: {resultado.error}'})
        except:
            self._dict_result.update({"obs": f'Falha no teste Iperf'})
        finally:
            # self.eth_interfaces_up()
            # self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
            # self.dhcp_v6(True)
            ssh.close()
            self._driver.quit()
            return self._dict_result      


    # 231
    def iPerf2PCsServerClient_231(self, flask_username,  ipv_x, dhcpv6):
        # self._driver.get('http://' + self._address_ip + '/padrao')
        # self.login_support()
        # time.sleep(3)
        # self.ipv_x_setting(ipv_x)
        # self.dhcp_v6(dhcpv6_state = dhcpv6)
        # self.eth_interfaces_down()
        
        # Encontra o ip da maquina local:
        network = '.'.join(self._address_ip.split('.')[:3])
        ip_maq = os.popen(f'ifconfig | grep {network}').read().strip(' ').split(' ')[1]
        print(ip_maq)
        
        # Encontra o ip da maquina remota
        try:
            ips = os.popen(f'nmap -sP {self._address_ip}/24').readlines()
            ips = [ip.split(' ')[-1].strip(' \n()') for ip in ips if network in ip]
            ip_remoto_list = []
            for ip in ips:
                if ip != ip_maq and ip != network+'.1' and ip != network+'.100' and ip != network+'.230':
                    ip_remoto_list.append(ip)
            print(ip_remoto_list)
        except Exception as e:
            print(e)

        # Inicia o Iperf como server na maquina local
        iperf_server = subprocess.Popen('iperf3 -s', shell=True)
        
        # Inicia o Iperf como cliente na maquina remota e executa o teste
        for ip_remoto in ip_remoto_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_remoto, username='automacao', password='4ut0m4c40', timeout=2)
                teste = ssh.invoke_shell()
                teste.send(f'iperf3 -c {ip_maq} \n')
                time.sleep(12)
                output = teste.recv(65000).decode('utf-8')
                print(output)
                resultado = output.split('\n')[-2].strip(' ')
                if 'iperf Done.' in resultado:
                    sender = ' '.join(output.split('\n')[-5].split(' ')[12:14])
                    receiver = ' '.join(output.split('\n')[-4].split(' ')[12:14])
                    self._dict_result.update({"obs": f'IPerf: Server local <- Client remoto realizado com sucesso. Transmissao {sender}; Recepcao {receiver}', "result":'passed', "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": f'Falha na Conexao: Server <- Cliente'})    
                break
            except Exception as e:
                print(e)
                continue
        else:
            print(e)
            self._dict_result.update({"obs": f'Falha na Conexao ssh com {ip_remoto}: verifique as configuracoes de usuario, senha e firewall'})
            return self._dict_result 

        # self.eth_interfaces_up()
        # self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
        # self.dhcp_v6(True)   
        ssh.close()
        self._driver.quit()
        iperf_server.terminate()
        return self._dict_result 


    # 255
    def iPerf2PCsClientServerIpv6_255(self, flask_username,  ipv_x, dhcpv6):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(3)
        self.ipv_x_setting(ipv_x)
        # self.dhcp_v6(dhcpv6_state = dhcpv6)
        # self.eth_interfaces_down()
        
        # Encontra o ip da maquina local:
        network = '.'.join(self._address_ip.split('.')[:3])
        ip_maq = os.popen(f'ifconfig | grep {network}').read().strip(' ').split(' ')[1]
        print(ip_maq)
        
        # Encontra o ip da maquina remota
        try:
            ips = os.popen(f'nmap -sP {self._address_ip}/24').readlines()
            ips = [ip.split(' ')[-1].strip(' \n()') for ip in ips if network in ip]
            ip_remoto_list = []
            for ip in ips:
                if ip != ip_maq and ip != network+'.1' and ip != network+'.100' and ip != network+'.230':
                    ip_remoto_list.append(ip)
            print(ip_remoto_list)
        except Exception as e:
            print(e)

        # Conecta com a maquina remota via ssh e configura como server do IPerf
        for ip_remoto in ip_remoto_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_remoto, username='automacao', password='4ut0m4c40', timeout=2)
                teste = ssh.invoke_shell()
                teste.send('iperf3 -s \n')
                time.sleep(2)
                output = teste.recv(65000).decode('utf-8')
                print(ip_remoto)
                print(output)
                break
            except Exception as e:
                print(e)
                continue
        else:
            print(e)
            self._dict_result.update({"obs": f'Falha na Conexao ssh com {ip_remoto}: verifique as configuracoes de usuario, senha e firewall'})
            return self._dict_result  

        # Executa o teste IPerf como cliente
        try:
            client = iperf3.Client()
            client.server_hostname = ip_remoto
            client.protocol = 'tcp'
            resultado = client.run()
            print(resultado.error)
            if resultado.error == None:
                self._dict_result.update({"obs": f'IPerf: Cliente local -> Server remoto realizado com sucesso. Transmissao {resultado.sent_Mbps:.2f} Mbps; Recepcao {resultado.received_Mbps:.2f} Mbps', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Falha na Conexao: Cliente Iperf - Server , erro: {resultado.error}'})
        except:
            self._dict_result.update({"obs": f'Falha no teste Iperf'})
        finally:
            # self.eth_interfaces_up()
            self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
            # self.dhcp_v6(True)
            ssh.close()
            self._driver.quit()
            return self._dict_result      


    # 256
    def iPerf2PCsServerClientIpv6_256(self, flask_username,  ipv_x, dhcpv6):
        # self._driver.get('http://' + self._address_ip + '/padrao')
        # self.login_support()
        # time.sleep(3)
        # self.ipv_x_setting(ipv_x)
        # self.dhcp_v6(dhcpv6_state = dhcpv6)
        # self.eth_interfaces_down()
        
        # Encontra o ipv6 da maquina local:
        network = '.'.join(self._address_ip.split('.')[:3])
        ip_maq = os.popen(f'ifconfig | grep {network}').read().strip(' ').split(' ')[1]
        print(ip_maq)
        interfaces = [interface.split('\n') for interface in os.popen('ifconfig').read().split('\n\n') if interface.startswith("ens")]
        for interface in interfaces:
            if any([ip_maq in address for address in interface]):
                if_name = interface[0].split(':')[0]
                print(if_name)
        inet6_raw = os.popen(f'ip addr show {if_name}').readlines()
        for inet6 in inet6_raw:
            if inet6.strip(' ').startswith('inet6'):
                ip6_maq = inet6.strip(' ').split(' ')[1].split('/')[0]
                print(ip6_maq)
                break
           
        # Encontra o ip da maquina remota
        try:
            ips = os.popen(f'nmap -sP {self._address_ip}/24').readlines()
            ips = [ip.split(' ')[-1].strip(' \n()') for ip in ips if network in ip]
            ip_remoto_list = []
            for ip in ips:
                if ip != ip_maq and ip != network+'.1' and ip != network+'.100' and ip != network+'.230':
                    ip_remoto_list.append(ip)
            print(ip_remoto_list)
        except Exception as e:
            print(e)

        # Inicia o Iperf como server na maquina local
        iperf_server = subprocess.Popen('iperf3 -s', shell=True)
        
        # Inicia o Iperf como cliente na maquina remota e executa o teste
        for ip_remoto in ip_remoto_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_remoto, username='automacao', password='4ut0m4c40', timeout=2)
                teste = ssh.invoke_shell()
                teste.send(f'ping -6 {ip6_maq} \n')
                time.sleep(3)
                teste.send(chr(3))
                time.sleep(1)
                teste.send(f'iperf3 -6 -c {ip6_maq} \n')
                time.sleep(12)
                output = teste.recv(65000).decode('utf-8')
                print(output)
                resultado = output.split('\n')[-2].strip(' ')
                if 'iperf Done.' in resultado:
                    sender = ' '.join(output.split('\n')[-5].split(' ')[12:14])
                    receiver = ' '.join(output.split('\n')[-4].split(' ')[12:14])
                    self._dict_result.update({"obs": f'IPerf: Server local <- Client remoto realizado com sucesso. Transmissao {sender}; Recepcao {receiver}', "result":'passed', "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": f'Falha na Conexao: Server <- Cliente'})    
                break
            except Exception as e:
                print(e)
                continue
        else:
            print(e)
            self._dict_result.update({"obs": f'Falha na Conexao ssh com {ip_remoto}: verifique as configuracoes de usuario, senha e firewall'})
            return self._dict_result 

        # self.eth_interfaces_up()
        # self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
        # self.dhcp_v6(True)   
        ssh.close()
        self._driver.quit()
        iperf_server.terminate()
        return self._dict_result 