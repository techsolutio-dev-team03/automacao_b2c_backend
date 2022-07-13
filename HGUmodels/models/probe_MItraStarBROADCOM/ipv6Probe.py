# import re
import signal
from socket import timeout
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
import datetime
from skpy import Skype
import iperf3
import os
import subprocess
import paramiko
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException
from paramiko.ssh_exception import SSHException

# from daos.mongo_dao import MongoConnSigleton
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException

# from paramiko.ssh_exception import SSHException
# import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

# from HGUmodels import wizard_config

session = MainSession()

class HGU_MItraStarBROADCOM_ipv6Probe(HGU_MItraStarBROADCOM):

 
    # 172
    # def ipv6_wan_enabled(self, flask_username, url_list, ipv_x, dhcpv6):
    #     self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
    #     self.login_support()

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
    #     self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
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
    #     self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
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
    #     self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
    #     self.login_support()
    #     time.sleep(5)

    #     self.ipv_x_setting(ipv_x)
    #     self.dhcp_v6(dhcpv6_state = dhcpv6)
    #     self.eth_interfaces_down()

    #     try:
    #         client = iperf3.Client()
    #         client.server_hostname = iperf_server
    #         client.verbose = True
    #         resultado = client.run()
    #         #print(resultado.json)
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


   #186
    def connect_ipv4_ipv6_186(self, flask_username):#, ipv_x, dhcpv6):
        interface_name = self.get_interface(self._address_ip)
        print(interface_name)

        for n in range(0,3):
            print('reiniciando interface')
            os.system(f'echo 4ut0m4c40 | sudo -S ifconfig {interface_name} down')
            time.sleep(2)
            os.system(f'echo 4ut0m4c40 | sudo -S ifconfig {interface_name} up')
            time.sleep(10)
            print('interface reiniciada')

            response_ipv6_ip = os.popen(f'ping6 2800:3f0:4001:833::200e -c 10 -I {interface_name}').read()
            print(response_ipv6_ip)
            response_ipv6_url = os.popen(f'ping6 ipv6.google.com -c 10 -I {interface_name}').read()
            print(response_ipv6_url)
            teste_ipv6 = 'OK' if '10 recebidos' in response_ipv6_ip and '10 recebidos' in response_ipv6_url else 'NOK'

            response_ipv4_ip = os.popen(f'ping 142.250.218.78 -c 10 -I {interface_name}').read()
            print(response_ipv4_ip)
            response_ipv4_url = os.popen(f'ping ipv4.google.com -c 10 -I {interface_name}').read()
            print(response_ipv4_url)
            teste_ipv4 = 'OK' if '10 recebidos' in response_ipv4_ip and '10 recebidos' in response_ipv4_url else 'NOK'
                
            if teste_ipv4 == 'NOK' or teste_ipv6 == 'NOK': break
        
        if teste_ipv4 == 'OK' and teste_ipv6 == 'OK':
            self._dict_result.update({"obs": 'Conectividade IPv4 e IPv6 OK', "result":'passed', "Resultado_Probe":"OK"})
        else:
            self._dict_result.update({"obs": f'Falha no teste de conectividade IPv4 = {teste_ipv4} e IPv6 = {teste_ipv6}'})
        return self._dict_result


    # 212
    def ipv4DownloadCentOS_212(self, flask_username, ipv_x, dhcpv6):

        try:
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            self.ipv_x_setting(ipv_x)
            self.dhcp_v6(dhcpv6_state = dhcpv6)
            self.eth_interfaces_down()
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
        try:
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            self.ipv_x_setting(ipv_x)
            self.dhcp_v6(dhcpv6_state = dhcpv6)
            self.eth_interfaces_down()
            data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
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


    # 230
    def iPerf2PCsClientServer_230(self, flask_username,  ipv_x, dhcpv6):
        ip_remoto = []
        # Verifica nome da rede wifi e senha
        # self._driver.get('http://' + self._address_ip + '/')
        # self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
        # time.sleep(1)
        # self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
        # time.sleep(1)
        # self.login_admin()
        # wifi_network = self._driver.find_element_by_id("txtSsid").get_attribute('value')
        # senha = self._driver.find_element_by_id("txtPassword").get_attribute('value')
        # self._driver.quit()

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
                if ip != ip_maq and int(ip.split('.')[3]) > 1 and int(ip.split('.')[3]) < 100:
                    ip_remoto_list.append(ip)
            print(ip_remoto_list)
        except Exception as e:
            print(e)


        # Conecta com a maquina remota via ssh e configura como server do IPerf
        for ip_remoto in ip_remoto_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_remoto, username='automacao', password='aux', timeout=2)
                teste = ssh.invoke_shell()
                
                # Reset da interface evita problemas de erros na conexão
                # teste.send('echo 4ut0m4c40 | sudo -S usb-reset 0bda:c811\n')
                # teste.recv(65000).decode('utf-8')
                # print('reiniciando interface usb')
                # time.sleep(40)
                
                # Conexão no wifi da máquina Aux
                # teste.send(f'echo 4ut0m4c40 | sudo -S nmcli dev wifi conn "{wifi_network}" password "{senha}"  \n')
                # time.sleep(1)
                # teste.recv(65000).decode('utf-8')
                # print('conectando na interface wifi')
                # time.sleep(30)
                # con_wifi_status = teste.recv(65000).decode('utf-8')
                # # print("\n"*20, con_wifi_status)
                # interface_wifi = con_wifi_status.split(" ")[1].strip('“"” ')
                # # print("\n"*20, interface_wifi)
                # teste.send(f'ifconfig {interface_wifi} \n')
                # time.sleep(1)
                # ip_wifi = teste.recv(65000).decode('utf-8')
                # ip_wifi = ip_wifi.split("\n")[2].strip(' ').split(' ')[1]
                # print("\n", ip_wifi)

                teste.send('iperf3 -s \n')
                time.sleep(2)
                output = teste.recv(65000).decode('utf-8')
                # print(ip_wifi)
                print(output)
                break
            except Exception as e:
                print(e)
                continue
        else:
            self._dict_result.update({"obs": f'Falha na Conexao ssh com {ip_remoto}: verifique as configuracoes de usuario, senha e firewall'})
            return self._dict_result  

        # Executa o teste IPerf como cliente
        try:
            # client = iperf3.Client()
            # client.server_hostname = ip_wifi
            # client.protocol = 'tcp'
            # resultado = client.run()
           
            resultado = os.popen(f'iperf3 -c {ip_remoto}')
            time.sleep(12)
            # print(resultado.error)
            # output = teste.recv(65000).decode('utf-8')
    #             print("\n", output)
            saida = resultado.read()
            print(saida)
            resultado = saida.split('\n')[-2].strip(' ')
            if 'iperf Done.' in resultado:
                sender = ' '.join(saida.split('\n')[-5].split(' ')[12:14])
                receiver = ' '.join(saida.split('\n')[-4].split(' ')[12:14])
                self._dict_result.update({"obs": f'IPerf: Server local -> Client remoto realizado com sucesso. Transmissao {sender}; Recepcao {receiver}', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Falha na Conexao: Server -> Cliente'}) 
            # if resultado.error == None:
            #     self._dict_result.update({"obs": f'IPerf: Cliente local -> Server remoto realizado com sucesso. Transmissao {resultado.sent_Mbps:.2f} Mbps; Recepcao {resultado.received_Mbps:.2f} Mbps', "result":'passed', "Resultado_Probe":"OK"})
            # else:
            #     self._dict_result.update({"obs": f'Falha na Conexao: Cliente Iperf - Server , erro: {resultado.error}'})
        except:
            self._dict_result.update({"obs": f'Falha no teste Iperf'})
        finally:
            # self.eth_interfaces_up()
            # self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
            # self.dhcp_v6(True)
            # print(teste.recv(65000).decode('utf-8'))
            teste.send(chr(3))
            # teste.send(f'echo 4ut0m4c40 | sudo -S nmcli conn delete {wifi_network} \n')
            time.sleep(2)
            # resultado.close()

            ssh.close()
            
            return self._dict_result      


    # # 231
    def iPerf2PCsServerClient_231(self, flask_username,  ipv_x, dhcpv6):
        ip_remoto = []
        # self._driver.get('http://' + self._address_ip + '/')
        # self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
        # time.sleep(1)
        # self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
        # time.sleep(1)
        # self.login_admin()
        # wifi_network = self._driver.find_element_by_id("txtSsid").get_attribute('value')
        # senha = self._driver.find_element_by_id("txtPassword").get_attribute('value')
        # self._driver.quit()
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
                if ip != ip_maq and int(ip.split('.')[3]) > 1 and int(ip.split('.')[3]) < 100:
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
                ssh.connect(hostname=ip_remoto, username='automacao', password='aux', timeout=2)
                teste = ssh.invoke_shell()

                # Reset da interface evita problemas de erros na conexão
                # teste.send('echo 4ut0m4c40 | sudo -S usb-reset 0bda:c811\n')
                # teste.recv(65000).decode('utf-8')
                # print('reiniciando interface usb')
                # time.sleep(40)
                
                # teste.send(f'echo 4ut0m4c40 | sudo -S nmcli dev wifi conn "{wifi_network}" password "{senha}"  \n')
                # time.sleep(1)
                # teste.recv(65000).decode('utf-8')
                # print('conectando na interface wifi')
                # time.sleep(30)
                # con_wifi_status = teste.recv(65000).decode('utf-8')
                # # print("\n"*20, con_wifi_status)
                # interface_wifi = con_wifi_status.split(" ")[1].strip('“"” ')
                # # print("\n"*20, interface_wifi)
                # teste.send(f'ifconfig {interface_wifi} \n')
                # time.sleep(1)
                # ip_wifi = teste.recv(65000).decode('utf-8')
                # ip_wifi = ip_wifi.split("\n")[2].strip(' ').split(' ')[1]
                # print("\n", ip_wifi)
                
                teste.send(f'iperf3 -c {ip_maq} -B {ip_remoto} \n')
                time.sleep(12)
                output = teste.recv(65000).decode('utf-8')
                print("\n", output)
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
            self._dict_result.update({"obs": f'Falha na Conexao ssh com {ip_remoto}: verifique as configuracoes de usuario, senha e firewall'})
            return self._dict_result 

        # self.eth_interfaces_up()
        # self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
        # self.dhcp_v6(True)   
        teste.send(chr(3))
        # teste.send(f'echo 4ut0m4c40 | sudo -S nmcli conn delete {wifi_network} \n')
        time.sleep(2)
        ssh.close()
        self._driver.quit()
        iperf_server.terminate()
        return self._dict_result 


    # # 255
    def iPerf2PCsClientServerIpv6_255(self, flask_username,  ipv_x, dhcpv6):
        ip_remoto = []
    #     self._driver.get('http://' + self._address_ip + '/')
    #     self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
    #     time.sleep(1)
    #     self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
    #     time.sleep(1)
    #     self.login_admin()
    #     wifi_network = self._driver.find_element_by_id("txtSsid").get_attribute('value')
    #     senha = self._driver.find_element_by_id("txtPassword").get_attribute('value')
        self._driver.quit()
    #     # self.ipv_x_setting(ipv_x)
    #     # self.dhcp_v6(dhcpv6_state = dhcpv6)
        
        
    #     # Encontra o ip da maquina local:
        network = '.'.join(self._address_ip.split('.')[:3])
        ip_maq = os.popen(f'ifconfig | grep {network}').read().strip(' ').split(' ')[1]
        print(ip_maq)
        
    #     # Encontra o ip da maquina remota
        try:
            ips = os.popen(f'nmap -sP {self._address_ip}/24').readlines()
            ips = [ip.split(' ')[-1].strip(' \n()') for ip in ips if network in ip]
            ip_remoto_list = []
            for ip in ips:
                if ip != ip_maq and int(ip.split('.')[3]) > 1 and int(ip.split('.')[3]) < 100:
                    ip_remoto_list.append(ip)
            print(ip_remoto_list)
        except Exception as e:
            print(e)


    #     # Conecta com a maquina remota via ssh e configura como server do IPerf
        for ip_remoto in ip_remoto_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_remoto, username='automacao', password='aux', timeout=2)
                teste = ssh.invoke_shell()
                teste.recv(65000).decode('utf-8')
    #             # Reset da interface evita problemas de erros na conexão
    #             teste.send('echo 4ut0m4c40 | sudo -S usb-reset 0bda:c811\n')
    #             teste.recv(65000).decode('utf-8')
    #             print('reiniciando interface usb')
    #             time.sleep(40)
                
    #             teste.send(f'echo 4ut0m4c40 | sudo -S nmcli dev wifi conn "{wifi_network}" password "{senha}"  \n')
    #             time.sleep(1)
    #             teste.recv(65000).decode('utf-8')
    #             print('conectando na interface wifi')
    #             time.sleep(30)
    #             con_wifi_status = teste.recv(65000).decode('utf-8')
    #             # print("\n"*20, con_wifi_status)
    #             interface_wifi = con_wifi_status.split(" ")[1].strip('“"” ')
    #             # print("\n"*20, interface_wifi)
    #             teste.send(f'ifconfig {interface_wifi} \n')
    #             time.sleep(1)
    #             ip_wifi = teste.recv(65000).decode('utf-8')
    #             ip_wifi = ip_wifi.split("\n")[2].strip(' ').split(' ')[1]
    #             print("\n", ip_wifi)

                # Encontra o ipv6 da maquina remota:
                teste.send('ifconfig \n')
                time.sleep(2)
                output = teste.recv(65000).decode('utf-8')
                # print('\n'*10, output.lstrip('ifconfig \r\nautomacao@automacao-Aux:~$ ifconfig \r\n'))
                # print('\n'*10, output.split('\r\n'))
                interfaces = [interface.split('\n') for interface in output.lstrip('ifconfig \r\nautomacao@automacao-Aux:~$ ifconfig \r\n').split('\r\n\r\n') if interface.startswith("ens")]
                print('\n'*10, interfaces)
                for interface in interfaces:
                    if any([ip_remoto in address for address in interface]):
                        if_name = interface[0].split(':')[0]
                        print(if_name)
                teste.send(f'ip addr show {if_name} \n')
  
                time.sleep(2)
                inet6_raw = teste.recv(65000).decode('utf-8')
                print('\n'*10, inet6_raw)
                for inet6 in inet6_raw.split('\n'):
                    if inet6.strip(' ').startswith('inet6'):
                        ip6_remoto = inet6.strip(' ').split(' ')[1].split('/')[0]
                        print('\n'*10, ip6_remoto)
                        break

                teste.send('iperf3 -s \n')
                time.sleep(2)
                output = teste.recv(65000).decode('utf-8')
                # print(ip_remoto)
                # print(output)
                break
            except Exception as e:
                print(e)
                continue
        else:
            self._dict_result.update({"obs": f'Falha na Conexao ssh com {ip_remoto}: verifique as configuracoes de usuario, senha e firewall'})
            return self._dict_result  


        # Executa o teste IPerf como cliente
        try:
            # client = iperf3.Client()
            # client.server_hostname = ip_wifi
            # client.protocol = 'tcp'
            # resultado = client.run()


   
            print(f"ping {ip6_remoto}")
            ping = subprocess.Popen(f'ping6 {ip6_remoto}', shell=True, preexec_fn=os.setsid)
            time.sleep(3)
            os.killpg(os.getpgid(ping.pid), signal.SIGTERM)
            time.sleep(1)
            print("iniciando cliente")
            # time.sleep(1000)
            resultado = os.popen(f'iperf3 --connect-timeout 5000 -c {ip6_remoto}')
            time.sleep(12)
            # print(resultado.error)
            # output = teste.recv(65000).decode('utf-8')
    #             print("\n", output)
            saida = resultado.read()
            print(saida)
            resultado = saida.split('\n')[-2].strip(' ')
            if 'iperf Done.' in resultado:
                sender = ' '.join(saida.split('\n')[-5].split(' ')[12:14])
                receiver = ' '.join(saida.split('\n')[-4].split(' ')[12:14])
                self._dict_result.update({"obs": f'IPerf: Server local -> Client remoto realizado com sucesso. Transmissao {sender}; Recepcao {receiver}', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Falha na Conexao: Server -> Cliente'}) 
            # if resultado.error == None:
            #     self._dict_result.update({"obs": f'IPerf: Cliente local -> Server remoto realizado com sucesso. Transmissao {resultado.sent_Mbps:.2f} Mbps; Recepcao {resultado.received_Mbps:.2f} Mbps', "result":'passed', "Resultado_Probe":"OK"})
            # else:
            #     self._dict_result.update({"obs": f'Falha na Conexao: Cliente Iperf - Server , erro: {resultado.error}'})
        except:
            self._dict_result.update({"obs": f'Falha no teste Iperf'})
        finally:
            # self.eth_interfaces_up()
            # self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
            # self.dhcp_v6(True)
            # print(teste.recv(65000).decode('utf-8'))
            teste.send(chr(3))
            # teste.send(f'echo 4ut0m4c40 | sudo -S nmcli conn delete {wifi_network} \n')
            time.sleep(2)
            # resultado.close()
            ssh.close()
            
            return self._dict_result   


    # # 256
    def iPerf2PCsServerClientIpv6_256(self, flask_username,  ipv_x, dhcpv6):
        ip_remoto = []
    #     self._driver.get('http://' + self._address_ip + '/')
    #     self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
    #     time.sleep(1)
    #     self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[3]/a').click()
    #     time.sleep(1)
    #     self.login_admin()
    #     wifi_network = self._driver.find_element_by_id("txtSsid").get_attribute('value')
    #     senha = self._driver.find_element_by_id("txtPassword").get_attribute('value')
    #     self._driver.quit()
        
    #     # Encontra o ipv6 da maquina local:
        network = '.'.join(self._address_ip.split('.')[:3])
        ip_maq = os.popen(f'ifconfig | grep {network}').read().strip(' ').split(' ')[1]
        print(ip_maq)
        interfaces = [interface.split('\n') for interface in os.popen('ifconfig').read().split('\n\n') if interface.startswith("ens")]
        # print('\n'*10, interfaces)
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
           
    #     # Encontra o ip da maquina remota
        try:
            ips = os.popen(f'nmap -sP {self._address_ip}/24').readlines()
            ips = [ip.split(' ')[-1].strip(' \n()') for ip in ips if network in ip]
            ip_remoto_list = []
            for ip in ips:
                if ip != ip_maq and int(ip.split('.')[3]) > 1 and int(ip.split('.')[3]) < 100:
                    ip_remoto_list.append(ip)
            print(ip_remoto_list)
        except Exception as e:
            print(e)

    #     # Inicia o Iperf como server na maquina local
        iperf_server = subprocess.Popen('iperf3 -s', shell=True)
        
    #     # Inicia o Iperf como cliente na maquina remota e executa o teste
        for ip_remoto in ip_remoto_list:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip_remoto, username='automacao', password='aux', timeout=2)
                teste = ssh.invoke_shell()

    #             # Reset da interface evita problemas de erros na conexão
    #             teste.send('echo 4ut0m4c40 | sudo -S usb-reset 0bda:c811\n')
    #             teste.recv(65000).decode('utf-8')
    #             print('reiniciando interface usb')
    #             time.sleep(40)
                
    #             teste.send(f'echo 4ut0m4c40 | sudo -S nmcli dev wifi conn "{wifi_network}" password "{senha}"  \n')
    #             time.sleep(1)
    #             teste.recv(65000).decode('utf-8')
    #             print('conectando na interface wifi')
    #             time.sleep(30)
    #             con_wifi_status = teste.recv(65000).decode('utf-8')
    #             # print("\n"*20, con_wifi_status)
    #             interface_wifi = con_wifi_status.split(" ")[1].strip('“"” ')
    #             # print("\n"*20, interface_wifi)
    #             teste.send(f'ifconfig {interface_wifi} \n')
    #             time.sleep(1)
    #             ip_wifi = teste.recv(65000).decode('utf-8')
    #             print(ip_wifi)
    #             ip_wifi = ip_wifi.split("\n")[3].strip(' ').split(' ')[1]
    #             print("\n", ip_wifi)
                
                teste.send(f'ping -6 {ip6_maq} \n')
                time.sleep(3)
                teste.send(chr(3))
                time.sleep(1)
                teste.send(f'iperf3 -6 --connect-timeout 5000 -c {ip6_maq} \n') #-B {ip_remoto} \n')
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
            self._dict_result.update({"obs": f'Falha na Conexao ssh com {ip_remoto}: verifique as configuracoes de usuario, senha e firewall'})
            return self._dict_result 

        # self.eth_interfaces_up()
        # self.ipv_x_setting('IPv4&IPv6(Dual Stack)')
        # self.dhcp_v6(True)  
        teste.send(chr(3))
        # teste.send(f'echo 4ut0m4c40 | sudo -S nmcli conn delete {wifi_network} \n')
        time.sleep(2)
        ssh.close()
        self._driver.quit()
        iperf_server.terminate() 
        return self._dict_result 