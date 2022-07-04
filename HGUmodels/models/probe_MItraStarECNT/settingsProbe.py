#from asyncio import exceptions
from cgi import print_form
import datetime
import json
from os import name
import re
import time
import pandas as pd

# import unidecode
# from jinja2 import pass_context
#from typing import final
import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket

import requests
from json import JSONEncoder
from ..MItraStarECNT import HGU_MItraStarECNT
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException, ElementNotInteractableException
from HGUmodels.config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton

from HGUmodels.main_session import MainSession
from HGUmodels import wizard_config

session = MainSession()


mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()

dict_test_result_memory = {}

class HGU_MItraStarECNT_settingsProbe(HGU_MItraStarECNT):


    def accessWizard_401(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a/span').click()
            time.sleep(5)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            user_input = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/form/div/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('LoginPassword')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('acceptLogin')
            login_button.click()
            time.sleep(2)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[2]/a/span').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[1]/ul/li[2]/a/span').click()
            time.sleep(1)

            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
            dict_saida = {"Resultado_Probe": "OK"}
        except Exception:
            self._dict_result.update({"obs": "Nao foi possivel realizar o login com sucesso"})
            dict_saida = {"Resultado_Probe": "NOK"}
        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'accessWizard_401', dict_saida)
            return self._dict_result

    def testPasswordAdmin_402(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessWizard_401')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 401 primeiro'})
        else:
            res = result['Resultado_Probe']
            if res == 'OK':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': 'Password OK'})
            else:
                self._dict_result.update({'obs': 'Password incorreta'})

        return self._dict_result 



    def accessPadrao_403(self, flask_username):

        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            element = self._driver.find_element_by_xpath('/html/body/div/div[1]/div/div[2]')

            if element:
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
                dict_saida = {"Resultado_Probe": "OK"}

            else:
                self._dict_result.update({"obs": "Nao foi possivel realizar o login com sucesso"})
                dict_saida = {"Resultado_Probe": "NOK"}

        except Exception as exception:
            self._dict_result.update({'obs':str(exception)})
            dict_saida = {"Resultado_Probe": "NOK"}

        self._driver.quit()
        self.update_global_result_memory(flask_username, 'accessPadrao_403', dict_saida)
        return self._dict_result


    def testPasswordSupport_404(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessPadrao_403')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 403 primeiro'})
        else:
            res = result['Resultado_Probe']
            if res == 'OK':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': 'Password OK'})
            else:
                self._dict_result.update({'obs': 'Password incorreta'})

        return self._dict_result



    def accessRemoteHttp_405(self, flask_username):
        dict_saida405 = {}
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)
            # Passando por Manutencao
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="maintenance"]/span[1]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            # Clicando no MGMT Remoto
            self._driver.find_element_by_xpath('//*[@id="maintenance-remotemgmt"]').click()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(3)
            # Acessando o HTTP
            self._driver.find_element_by_xpath('//*[@id="t1"]/span').click()
            time.sleep(1)
            
           
            # Pegando o Access Server 
            accessHTTP = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[4]/ul/li[1]/div/ul/table/tbody/tr[2]/td[2]/select')
            for value in accessHTTP:
                name = value.get_attribute('name')
                type = value.get_attribute('type')
                val = value.get_attribute('value')
                dict_saida405.update({name: {"value": val, "type": type }})



            # Acessando o SSH
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="t5"]/span').click()
            time.sleep(1)

            # Pegando os valores
            accessSSH = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[1]/div/ul/table/tbody/tr[2]/td[2]/select')
            for value in accessSSH:
                name = value.get_attribute('name')
                type = value.get_attribute('type')
                val = value.get_attribute('value')
                dict_saida405.update({name: {"value": val, "type": type }})

            print(dict_saida405)

            # Resultado do teste
            for i,r in dict_saida405.items():

                if i == 'HttpsAccessInterface' and r['value'] != 'WAN':
                    self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', "obs":" Wan esta Desabilitado"})
                    break
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Access Server: {r['value']}"})
                    
            self._driver.quit()
        except Exception as exception:
            print(exception)
            self._dict_result.update({'obs':str(exception)})
            
        finally:
            self.update_global_result_memory(flask_username, 'accessRemoteHttp_405', dict_saida405)
            return self._dict_result


    '''
    Teste 406 e igual ao 407. 406 Teste de telnet. Nao disponivel
    ''' 

    
    def accessRemoteSSH_407(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessRemoteHttp_405')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 405 primeiro"})
        else:
            for i,r in result.items():
                if i == 'SSHAccessInterface' and r['value'] != 'WAN':
                    self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', "obs":"Wan esta Desabilitado"})
                    break
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Access Server: {r['value']}"})
        
        return self._dict_result


    def accessRemoteTrustedIP_408(self, flask_username):
        self._dict_result.update({'result':'failed',"obs": TEST_NOT_IMPLEMENTED_WARNING})
        return self._dict_result


    def NTPServer_409(self):

        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {self._address_ip} \n{'#' * 50}")
            
            try:
                ssh.connect(hostname=self._address_ip, 
                            username=self._username, 
                            password=self._password, 
                            timeout=2)
            except AuthenticationException:
                self._dict_result.update({ "obs":"Falha_Autenticacao"})

            except socket.timeout:
                self._dict_result.update({"obs":"Timeout"})

            else:
                
                try:
                    teste = ssh.invoke_shell()
                    teste.send('deviceinfo show ntp \n')
                    time.sleep(2)
                    output = teste.recv(65000)
                    out_str = output.decode('utf-8')
                    print(out_str)
                    str_list = out_str.splitlines()
                    for i in str_list:
                        if i.startswith('NTPServer1'):
                            split_ntp = i.split(':')
                            ntp_server = split_ntp[1]
                            ntp_server = ntp_server.strip()
                            print(ntp_server)

                    if (ntp_server == 'pool.ntp.br'):
                        self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': f'NTP Server OK: {ntp_server}'})
                    else:
                        self._dict_result.update({'obs': f'NTP Server: {ntp_server}'})

                except socket.timeout:
                    self._dict_result.update({"obs":"Timeout"})

                except Exception as exception:
                    self._dict_result.update({"obs":str(exception)})
            finally:
                return self._dict_result


    def timeZone_410(self):

        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {self._address_ip} \n{'#' * 50}")

            try:
                ssh.connect(hostname=self._address_ip, 
                            username=self._username, 
                            password=self._password, 
                            timeout=2)
            except AuthenticationException:
                self._dict_result.update({"obs": "Falha_Autenticacao"})
            except socket.timeout:
                self._dict_result.update({"obs": "Falha_Autenticacao"})
            else:
                try:
                    teste = ssh.invoke_shell()
                    teste.send('deviceinfo show ntp \n')
                    time.sleep(2)
                    output = teste.recv(65000)
                    out_str = output.decode('utf-8')
                    str_list = out_str.splitlines()
                    for i in str_list:
                        if i.startswith('localTimeZoneName'):
                            split_time = i.split(':')
                            time_zone = split_time[1]
                            time_zone = time_zone.strip()
                            print(time_zone)
    
                    if (time_zone == '(GMT-3:00) Brasilia'):
                        self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', 'obs': f'Timezone OK: {time_zone}'})
                    else:
                        self._dict_result.update({'obs': f'Timezone {time_zone}'})
    
                except socket.timeout:
                    self._dict_result.update({"obs": "Timeout_Connection"})
                except Exception as exception:
                    self._dict_result.update({"obs": str(exception)})
            finally:
                return self._dict_result 


    def checkACSSettings_411(self, flask_username):
        
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()

            #Manutencao >> TR069-Client
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="maintenance"]/a')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            tr69 = self._driver.find_element_by_xpath('//*[@id="maintenance-tr069Client"]').click()
            tr69 = self._driver.find_element_by_xpath('//*[@id="maintenance-tr069Client"]').text
 
            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')

            tr69_cwmp_valor = self._driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/ul/li[1]/div[1]/ul/li[2]/input[1]').get_attribute('checked')
            tr69_cwmp_valor = 'Habilitado' if tr69_cwmp_valor == 'true' else 'Desabilitado'
 
            tr69_acsURL_valor = self._driver.find_element_by_xpath('//*[@id="CWMP_ACSURL"]').get_attribute('value')
 
            tr69_acsUsername_valor = self._driver.find_element_by_xpath('//*[@id="CWMP_ACSUserName"]').get_attribute('value')
 
            tr69_acsPassword_valor = self._driver.find_element_by_xpath('//*[@id="CWMP_ACSPassword"]').get_attribute('value')
 
            tr69_acsPII_valor = self._driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/ul/li[1]/div[9]/ul/li[2]/input[1]').get_attribute('checked')
            tr69_acsPII_valor = 'Habilitado' if tr69_acsPII_valor=='true' else 'Desabilitado'
 
            tr69_acsPII_interval_valor = self._driver.find_element_by_xpath('//*[@id="CWMP_PeriodInterval"]').get_attribute('value')
 
            tr69_connection_request_URL_valor = self._driver.find_element_by_xpath('//*[@id="CWMP_ConnectionRequestPath"]').get_attribute('value')
 
            tr69_connection_request_Username_valor = self._driver.find_element_by_xpath('//*[@id="CWMP_ConnectionRequestUserName"]').get_attribute('value')
 
            tr69_connection_request_Password_valor = self._driver.find_element_by_xpath('//*[@id="CWMP_ConnectionRequestPassword"]').get_attribute('value')
            dict_saida411 = {
                "tr69_setting":
                    {
                        "tr69_cwmp": tr69_cwmp_valor,
                        "tr69_acsURL": tr69_acsURL_valor,
                        "tr69_acsUsername": tr69_acsUsername_valor,
                        "tr69_acsPassword": tr69_acsPassword_valor,
                        "tr69_acsPII": tr69_acsPII_valor,
                        "tr69_acsPII_interval": tr69_acsPII_interval_valor,
                    },
                "tr69_connection_request":
                    {
                        "tr69_connection_request_URL": tr69_connection_request_URL_valor,
                        "tr69_connection_request_Username": tr69_connection_request_Username_valor,
                        "tr69_connection_request_Password": tr69_connection_request_Password_valor
                    }
            }

            self._driver.quit()
            print(dict_saida411)

            if dict_saida411['tr69_setting']['tr69_acsURL'] == 'http://acs.telesp.net.br:7015/cwmpWeb/CPEMgt':
                self._dict_result.update({"Resultado_Probe": "OK",'result':'passed',"obs": "ACS URL: http://acs.telesp.net.br:7015/cwmpWeb/CPEMgt"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno ACS URL: {dict_saida411["tr69_setting"]["tr69_acsURL"]}'})

        except Exception as exception:
            self._driver.quit()
            self._dict_result.update({"obs":str(exception)})
        finally:
            self.update_global_result_memory(flask_username, 'checkACSSettings_411', dict_saida411)
            return self._dict_result
    

    def validarDefaultUserACS_412(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        
        else:
            value = result['tr69_connection_request'].get('tr69_connection_request_Username')
            if value == 'acsclient':
                self._dict_result.update({"obs": "Usuario: acsclient", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Usuario: {value}"})
        return self._dict_result


    def validarDefaultPasswordACS_413(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['tr69_setting'].get('tr69_acsPassword')
            if value == 'telefonica':
                self._dict_result.update({"obs": "Senha: telefonica", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Senha: {value}"})
        return self._dict_result


    # def GPV_OneObjct_414(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
    #     self._dict_result.update({'result':'failed',"obs": TEST_NOT_IMPLEMENTED_WARNING})
    #     return self._dict_result


    def GPV_OneObjct_414(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
        #TODO: This function needs refactoring, zeep library not working, test crashing
        class MyEncoder(JSONEncoder):
            def default(self, o):
                return o.__dict__
        acsPort = 7015
        objeto = GPV_Param['name']

       
        try:
            url = f'http://{IPACS}:{acsPort}/hdm'
            connTest = requests.post(url, timeout=4)

            if connTest.status_code != 200:
                self._dict_result.update({'result':'failed',"obs":f'ERROR002-ERRO DE CONECTIVIDADE COM ACS-HDM: {IPACS}:{acsPort}'})
                return self._dict_result
            else:
                ###INICIANDO WEBSERIVCES###
                #
                #try:
                import Setup.ACS.webSDO
                import Setup.ACS.webRemoteHDM
                from Setup.ACS import webRemoteHDM
                from Setup.ACS import webServiceImpl
                from Setup.ACS import webSDO
                nbiSDO = webSDO.SDO(IPACS, str(acsPort), acsUsername, acsPassword)
                nbiRH = webRemoteHDM.NRH(IPACS, str(acsPort), acsUsername, acsPassword)
                #except Exception as exception:
                #    print(exception)
                #    self._dict_result.update({'result':'failed',"obs":'ERROR_003-ERRO AO VALIDAR ARQUIVO WSDL NO SERVIDOR ACS-HDM #(LINE:84)'})
                #    return self._dict_result
                #
                ###BUSCANDO DADOS DO DISPOSITIVO###
                #
                tsa = time.time()
                sta = datetime.fromtimestamp(tsa).strftime('%Y_%m_%d_%HH:%MM:%SS')
                nbiRH.findDeviceBySerial(serialnumber, acsUsername, acsPassword)
                if nbiRH.msgTagExecution_02 == 'EXECUTED':
                    OUI = str(nbiRH.device["OUI"])
                    productClass = str(nbiRH.device["productClass"])
                    protocol = str(nbiRH.device["protocol"])
                    subscriberId = str(nbiRH.device["subscriberId"])
                    lastContactTime = str(nbiRH.device["lastContactTime"])
                    softwareVersion = str(nbiRH.device["softwareVersion"])
                    externalIpAddress = str(nbiRH.device["iPAddressWAN"])
                    activated = str(nbiRH.device["activated"])
                    lastActivationTime = pd.Timestamp(str(nbiRH.device["lastActivationTime"])).tz_convert("UTC")
                    lastActivationTime = lastActivationTime.strftime("%d-%m-%Y %H:%M:%S")
                    GPV = nbiSDO.getParameterValue(OUI, productClass, protocol, serialnumber, objeto)
                    if GPV != None:
                        GPV = json.dumps(GPV, cls=MyEncoder)
                        GPV_1 = json.loads(GPV)
                        json_saida = []
                        for key, value in enumerate(GPV_1):
                            for chave, valor in value.items():
                                aux = {
                                    "name":valor['name'],
                                    "type":valor['type'],
                                    "value":valor['value']
                                }
                                json_saida.append(aux)
                        self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', 'obs':json_saida})
                        return self._dict_result
                    else:
                        self._dict_result.update({'result':'failed',"obs":"GPV == None"})
                        return self._dict_result
                else:
                    self._dict_result.update({"obs":"nbiRH.msgTagExecution_02 != EXECUTED"})
        except Exception as exception:
            self._dict_result.update({"obs":str(exception)})
        return self._dict_result






    
    def periodicInformEnable_415(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['tr69_setting'].get('tr69_acsPII')
            if value == 'Habilitado':
                self._dict_result.update({"obs": "Informe: Habilitado ", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Informe: {value}"})
        return self._dict_result


    def periodicInformInterval_416(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['tr69_setting'].get('tr69_acsPII_interval')
            if value == '68400':
                self._dict_result.update({"obs": "Informe Interval: 68400", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Informe Interval: {value}"})
        return self._dict_result


    # def connectionRequestPort_417(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
    #     self._dict_result.update({'result':'failed',"obs": TEST_NOT_IMPLEMENTED_WARNING})
    #     return self._dict_result


    def connectionRequestPort_417(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
        d = self.GPV_OneObjct_414(serialnumber, GPV_Param, IPACS, acsUsername, acsPassword)
        
        gpv_probe = self._dict_result['Resultado_Probe']
    
        if gpv_probe == 'OK':
            gpv_result = self._dict_result['Resultado']
            for key in gpv_result:
                port_cr_value = key.get('value').strip('/').split(':')[2]
                if port_cr_value == '7547':
                    self._dict_result.update({"obs": None, "result":'passed', "Resultado_Probe": "OK"})
                    return self._dict_result
            self._dict_result.update({"obs": "port_cr_value != '7547'"})
            return self._dict_result
        elif gpv_probe == 'NOK':
            self._dict_result.update({"obs": "Teste 414 GPV_OneObjct Falhou!"})
            return self._dict_result


    def enableCwmp_418(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['tr69_setting'].get('tr69_cwmp')
            if value == 'Habilitado':
                self._dict_result.update({"obs": "CWMP: Habilitado", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno CWMP: {value}"})
        return self._dict_result


    def userConnectionRequest_419(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        #TODO: Verificar se o teste 419 é igual ao teste 412
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['tr69_connection_request'].get('tr69_connection_request_Username')
            if value == 'userid':
                self._dict_result.update({"obs": "Connection Request Username OK", "result":'passed'})
            else:
                self._dict_result.update({"obs": f"Connection Request Username incorreta, retorno: {value}", "result":'failed'})
        return self._dict_result


    def checkWanInterface_420(self, flask_username):
        try:

            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)
            
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()

            wanInterface = self._driver.find_element_by_xpath('//*[@id="network-broadband"]/a').click()
 
            self._driver.switch_to.default_content()
            time.sleep(3)

            self._driver.switch_to.frame('mainFrame')
            time.sleep(4)


            rows_string = [header.text for header in self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div/ul/li/div/table/tbody//tr')]
            time.sleep(3)
            table = [row.split() for row in rows_string]
            time.sleep(3)
            header_list = table[0]
            header_list.remove('Release')
            header_list = header_list[2:-1]
            rows = [row[1:] for row in table[1:4]]
            dict_saida420 = {}

            for i, row in enumerate(rows):

                d = {col:row[j] for (j,col) in enumerate(header_list)}
                dict_saida420.update({f'index_{i}':d})
            time.sleep(3)
            
            print('dict : ',dict_saida420)
            for k, item in dict_saida420.items():
                cpe_config = config_collection.find_one()
                if  cpe_config['REDE'] == 'VIVO_1':
                    if item['Encapsulamento'] == 'PPPoE' and item['VID/Prioridade'].split('/')[0] == '10': 
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Encapsulamento: PPPoE | VID/Prioridade: 10", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno: Encapsulamento:{item['Encapsulamento']}, VID/Prioridade:{item['VID/Prioridade']}"})
                        break
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})

        except Exception as exception:
            print(exception)
            self._dict_result.update({"obs": exception})
        finally:
            self._driver.quit()

            self.update_global_result_memory(flask_username, 'checkWanInterface_420', dict_saida420)
            return self._dict_result


    def prioridadePPPoE_421(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('Encapsulamento')
                cpe_config = config_collection.find_one()
                if iface_type == 'PPPoE' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                    separado_vid =  sub_dict.get('VID/Prioridade').split('/')[-1]
                    if separado_vid == '0':
                        self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VID/Prioridade: 0', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retornoNo VID/Prioridade: {separado_vid}"})
                        break
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: {iface_type}, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def tipoRedeInet_422(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('VID/Prioridade').split('/')[0]
                cpe_config = config_collection.find_one()
                if iface_type == '10' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                    if sub_dict.get('Encapsulamento') == 'PPPoE':
                        self._dict_result.update({"obs": 'VID/Prioridade: 10 | Encapsulamento: PPPoE', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno: VID/Prioridade:{iface_type}, Encapsulamento:{sub_dict.get('Type')}"})
                        break
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno: VID/Prioridade:{iface_type}, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def checkNatSettings_423(self, flask_username):
        time.sleep(3)
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)

            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            self._driver.find_element_by_xpath('//*[@id="network-broadband"]/a').click()
            time.sleep(1)

            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)

            table_flat = self._driver.find_elements_by_xpath('//*[@id="broadband_list"]/table/tbody/tr/td')
            checkbox_inputs = self._driver.find_elements_by_xpath('//*[@id="broadband_list"]/table/tbody//input')

            table = chunks(table_flat, 9)
            header_list = table[0]
            dict_saida423 = {}

            for i, row in enumerate(table[1:]):
                d = {col.text: (('Habilitado' 
                            if row[j].get_attribute('checked') == 'true' 
                            else 'Desabilitado') 
                                if row[j].get_attribute('checked') 
                                else row[j].text)
                    for (j,col) in enumerate(header_list[:-1])}
                dict_saida423.update({f'index_{i}':d})

            cpe_config = config_collection.find_one()

            for i, row in dict_saida423.items():
                if row['#'] == '1' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                    if row.get('NAT') == 'Enable':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: Interface 1, Adm.State: Habilitado", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface: Interface 1, Adm.State: {row['NAT']}"})
                        break
                else:
                    self._dict_result.update({"obs": f"ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
            self._driver.quit()
        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            self.update_global_result_memory(flask_username, 'checkNatSettings_423', dict_saida423)
            return self._dict_result


    # def checkMulticastSettings_424(self, flask_username):
    #     try:
    #         self._driver.get('http://' + self._address_ip + '/padrao')
    #         self.login_support()
    #         time.sleep(1)

    #         element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
    #         hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
    #         hover.perform()
    #         self._driver.find_element_by_xpath('//*[@id="network-homeNetworking"]').click()
    #         time.sleep(1)

    #         self._driver.switch_to.frame('mainFrame')
    #         time.sleep(1)

    #         # Pegando os inputs
    #         checkbox_inputs = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul//input')

    #         dict_saida424 = {}

    #         # Tratando seus valores
    #         for value in checkbox_inputs:
    #             name = value.get_attribute('name')
    #             if value.get_attribute('type') == 'radio':
    #                 if  value.get_attribute('checked'):
    #                     if value.get_attribute('value') == 'No':
    #                         val = value.get_attribute('value')
    #                         type = 'Disable'
    #                     else:
    #                         type = 'Ativado'
    #                         val = value.get_attribute('value')
    #             else:
    #                 type = value.get_attribute('type')
    #                 val = value.get_attribute('value')

    #             dict_saida424.update({name: {"value": val, "type": type }})
                
    #         print(dict_saida424)

    #         # Verificacao para retornar a resposta
    #         for i, row in dict_saida424.items():
    #             if i == 'igmp_quickleave_act':
    #                 if row['type'] == 'Disable':
    #                     self._dict_result.update({"Resultado_Probe": "OK", "obs": "IGMP Quickleave: Desabilitado", "result":"passed"})
    #                     break
    #                 else:
    #                     self._dict_result.update({"obs": f"Teste incorreto, retorno IGMP Quickleave: {row['type']}"})
    #                     break
    #             else:
    #                 self._dict_result.update({"obs": f"Teste incorreto, retorno {i}"})

    #         self._driver.quit()
    #     except Exception as e:
    #         self._dict_result.update({"obs": e})

    #     finally:
    #         self.update_global_result_memory(flask_username, 'checkMulticastSettings_424', dict_saida424)
    #         return self._dict_result

    def checkMulticastSettings_424(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(3)
            dict_saida424 = {}
            time.sleep(3)
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            time.sleep(3)

            hover.perform()
            time.sleep(3)

            self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[1]/li[2]/a').click()
            time.sleep(6)

            self._driver.switch_to.frame('mainFrame')
            time.sleep(3)

            #1 
            name =  self._driver.find_element_by_xpath(f'//*[@id="broadband_list"]/table/tbody/tr[2]/td[3]').text
            self._driver.find_element_by_xpath(f'//*[@id="editBtn"]').click()
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.find_element_by_xpath('/html/body/div[3]/div[2]/form/div[1]/div/ul/li[5]/div/ul/li/input').click()
            time.sleep(3)

            multicast = Select(self._driver.find_element_by_xpath('/html/body/div[3]/div[2]/form/div[1]/div/ul/div[4]/li[2]/div[2]/ul[3]/li[2]/select')).first_selected_option.text

            time.sleep(3)
            dict_saida424[name] = multicast
            print(dict_saida424)
            time.sleep(2)

            self._driver.find_element_by_xpath('/html/body/div[3]/div[1]/a/span').click()

            time.sleep(5)
            

            #2 
            self._driver.switch_to.frame('mainFrame')
            name =  self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div/ul/li/div/table/tbody/tr[3]/td[3]').text
            time.sleep(2)
            
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div/ul/li/div/table/tbody/tr[3]/td[9]/div/ul/li[1]/a').click()
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.find_element_by_xpath('/html/body/div[3]/div[2]/form/div[1]/div/ul/li[5]/div/ul/li/input').click()
            time.sleep(3)

            multicast = Select(self._driver.find_element_by_xpath('/html/body/div[3]/div[2]/form/div[1]/div/ul/div[4]/li[2]/div[2]/ul[3]/li[2]/select')).first_selected_option.text
            
            time.sleep(3)
            dict_saida424[name] = multicast
            print(dict_saida424)
            time.sleep(2)

            self._driver.find_element_by_xpath('/html/body/div[3]/div[1]/a/span').click()

            time.sleep(2)
            
            #3
            self._driver.switch_to.frame('mainFrame')

            name =  self._driver.find_element_by_xpath(f'/html/body/div[2]/div/form/div/div/ul/li/div/table/tbody/tr[4]/td[3]').text
            time.sleep(2)

            self._driver.find_element_by_xpath(f'/html/body/div[2]/div/form/div/div/ul/li/div/table/tbody/tr[4]/td[9]/div/ul/li[1]/a').click()
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.find_element_by_xpath('/html/body/div[3]/div[2]/form/div[1]/div/ul/li[5]/div/ul/li/input').click()
            time.sleep(3)

            multicast = Select(self._driver.find_element_by_xpath('/html/body/div[3]/div[2]/form/div[1]/div/ul/div[4]/li[2]/div[2]/ul[3]/li[2]/select')).first_selected_option.text
            
            time.sleep(3)
            dict_saida424[name] = multicast

            
            print(dict_saida424)
            
            try:
                if dict_saida424['Internet'] == 'Nenhum':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "IGMP Internet: Desabilitado", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno IGMP Internet: {dict_saida424['Internet']}"})
            except:
                self._dict_result.update({"obs": 'Interface Internet nao existe'})
        
        except (Exception, NoSuchElementException, ElementNotInteractableException) as e:
            self._dict_result.update({"obs": e})

        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkMulticastSettings_424', dict_saida424)
            return self._dict_result


    def getFullConfig_425(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/')
        time.sleep(2)
        self._driver.switch_to.default_content
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a').click()
        time.sleep(2)
        self.admin_authentication_mitraStat()
      

        print('\n#############################################'
                '\n MENU >> STATUS'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS
        ### ------------------------------------------ ###
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[1]/a/span').click()
        time.sleep(2)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        time.sleep(2)
        print('\n#############################################'
                '\n MENU >> STATUS >> GPON'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > GPON
        ### ------------------------------------------ ###
        gpon = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/th/span').text
        print(gpon)
        divOptical = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]/div[1]').text
        divOptical = divOptical.split("\n")
        print(divOptical)
        divOptRx = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]/div[2]').text
        divOptRx = divOptRx.split("\n")
        print(divOptRx)
        divOptTx = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]/div[3]').text
        divOptTx = divOptTx.split("\n")
        print(divOptTx)
        print('\n#############################################'
                '\n MENU >> STATUS >> INTERNET'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > INTERNET
        ### ------------------------------------------ ###
        internet = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[3]/th/span').text
        print(internet)
        divPpp = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[3]/td[1]/div').text
        divPpp = divPpp.split("\n")
        print(divPpp)
        detalhes_internet = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[3]/td[2]/a/span')
        print(detalhes_internet.text)
        detalhes_internet.click()
        detalhes_IPv4_head = self._driver.find_element_by_link_text('IPv4').text
        print(detalhes_IPv4_head)
        detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[4]/td[2]/div[2]/div[1]')
        time.sleep(1)
        items_key_internet_ipv4 = detalhes_IPv4.find_elements_by_tag_name("li")
        detalhes_IPv4_nome = []
        for i in items_key_internet_ipv4:
            teste = i.text
            detalhes_IPv4_nome.append(teste)
        print(detalhes_IPv4_nome)
        detalhes_IPv4 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[4]/td[2]/div[2]/div[2]')
        items_key = detalhes_IPv4.find_elements_by_tag_name("li")
        detalhes_IPv4_valor = []
        for i in items_key:
            teste = i.text
            detalhes_IPv4_valor.append(teste)
        print(detalhes_IPv4_valor)
        time.sleep(2)
        detalhes_IPv6 = self._driver.find_element_by_link_text('IPv6')
        detalhes_IPv6.click()
        time.sleep(1)
        detalhes_IPv6_head = self._driver.find_element_by_link_text('IPv6').text
        print(detalhes_IPv6_head)
        detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[4]/td[2]/div[3]/div[1]')
        time.sleep(1)
        items_key = detalhes_IPv6.find_elements_by_tag_name("li")
        detalhes_IPv6_nome = []
        for item in items_key:
            teste = item.text
            detalhes_IPv6_nome.append(teste)
        print(detalhes_IPv6_nome)
        detalhes_IPv6 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[4]/td[2]/div[3]/div[2]')
        items_key = detalhes_IPv6.find_elements_by_tag_name("li")
        detalhes_IPv6_valor = []
        for item in items_key:
            teste = item.text
            detalhes_IPv6_valor.append(teste)
        print(detalhes_IPv6_valor)
        time.sleep(2)
        print('\n#############################################'
                '\n MENU >> STATUS >> WIFI 2.4GHz'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > WIFI 2.4GHz
        ### ------------------------------------------ ###
        wifi_24 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[5]/th/span').text
        print(wifi_24)
        wifi_24_name = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[5]/td[1]/div').text
        wifi_24_name = wifi_24_name.replace('\n',' ').split(' ')
        print(wifi_24_name)
        wifi_24_detalhes = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[5]/td[2]/a/span')
        wifi_24_detalhes.click()
        wifi_24_detalhes_info = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[6]/td[1]/div')
        items_key = wifi_24_detalhes_info.find_elements_by_tag_name("li")
        wifi_24_valor = []
        for item in items_key:
            teste = item.text
            wifi_24_valor.append(teste)
        print(wifi_24_valor)
        wifi_24_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[6]/td[2]/div/textarea').get_attribute('value').strip('\n')
        print(wifi_24_detalhes_stations)
        time.sleep(2)
        print('\n#############################################'
                '\n MENU >> STATUS >> WIFI 5GHz'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > WIFI 5GHz
        ### ------------------------------------------ ###
        wifi_5 = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[7]/th/span').text
        print(wifi_5)
        wifi_5_name = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[7]/td[1]/div').text
        wifi_5_name = wifi_5_name.replace('\n', ' ').split(' ')
        print(wifi_5_name)
        wifi_5_detalhes = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[7]/td[2]/a')
        wifi_5_detalhes.click()
        wifi_5_detalhes_info = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[8]/td[1]/div')
        items_key = wifi_5_detalhes_info.find_elements_by_tag_name("li")
        wifi_5_valor = []
        for item in items_key:
            teste = item.text
            wifi_5_valor.append(teste)
        print(wifi_5_valor)
        wifi_5_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[8]/td[2]/div/textarea').get_attribute('value').strip('\n')
        wifi_5_detalhes_stations = wifi_5_detalhes_stations.split('\n')
        print(wifi_5_detalhes_stations)
        time.sleep(2)
        print('\n#############################################'
                '\n MENU >> STATUS >> REDE LOCAL'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > REDE LOCAL
        ### ------------------------------------------ ###
        rede_local = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[11]/th/span').text
        print(rede_local)
        time.sleep(2)
        rede_local_name = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[11]/td[1]').text
        rede_local_name = rede_local_name.replace(' ', '')
        rede_local_name = rede_local_name.split('\n')
        rede_local_name_ok = {"LAN1": "NULL", "LAN2": "NULL", "LAN3": "NULL", "LAN4": "NULL"}
        indexLAN = 0
        index = 0
        for i in rede_local_name:
            if i.startswith('LAN') == True:
                indexLAN = indexLAN + 1
                pos = 'LAN' + str(indexLAN)
            else:
                rede_local_name_ok[pos] = rede_local_name[index]
            index = index + 1
        print(rede_local_name_ok)

 
        rede_local_detalhes = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[11]/td[2]/a')
        rede_local_detalhes.click()
        rede_local_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[12]/td[2]/div/textarea').get_attribute('value')
        rede_local_stations = rede_local_stations.split('\n')
 
        time.sleep(2)
        print('\n#############################################'
                '\n MENU >> STATUS >> TV'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > TV
        ### ------------------------------------------ ###
        tv = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[13]/th/span').text
        print(tv)
        self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[13]/td[2]/a').click()
        tv_info = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[14]/td[1]/div')
        items_key = tv_info.find_elements_by_tag_name("li")
        tv_valor = []
        for item in items_key:
            teste = item.text
            # print(item.text)
            tv_valor.append(teste)
        print(tv_valor)
        tv_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[14]/td[2]/div/textarea').get_attribute('value')
        tv_stations = tv_stations.split('\n')
        print(tv_stations)
        time.sleep(2)
        print('\n#############################################'
                '\n MENU >> STATUS >> TELEFONE'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         STATUS > TELEFONE
        ### ------------------------------------------ ###
        telefone = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[15]/th/span').text
        print(telefone)
        telefone_info_rede = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[15]/td[1]/div[1]').text
        telefone_info_rede = telefone_info_rede.split('\n')
        print(telefone_info_rede)
        telefone_info_status = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[15]/td[1]/div[2]').text
        telefone_info_status = telefone_info_status.split('\n')
        print(telefone_info_status)
        # telefone_stations = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[14]/td[2]/textarea').get_attribute('value')
        # telefone_stations = telefone_stations.split('\n')
        # print(telefone_stations)
        # time.sleep(2)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> INTERNET'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > INTERNET
        ### ------------------------------------------ ###
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/a/span').click()
        time.sleep(1)
        config_internet = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[1]/a/span')
        config_internet.click()
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        config_internet = self._driver.find_element_by_xpath('/html/body/form/div/div[1]/div[1]/table/thead/tr/th').text
        print(config_internet)
        config_internet_usuario = self._driver.find_element_by_xpath('/html/body/form/div/div[1]/div[1]/table/tbody/tr[2]/td[1]/span').text.strip(': ')
        print(config_internet_usuario)
        config_internet_usuario_valor = self._driver.find_element_by_xpath('/html/body/form/div/div[1]/div[1]/table/tbody/tr[2]/td[2]/input').get_property('value')
        print(config_internet_usuario_valor)
        config_internet_senha = self._driver.find_element_by_xpath('/html/body/form/div/div[1]/div[1]/table/tbody/tr[3]/td[1]/span').text.strip(': ')
        print('############################## 1')
        print(config_internet_senha)
        config_internet_senha_valor = self._driver.find_element_by_xpath('/html/body/form/div/div[1]/div[1]/table/tbody/tr[3]/td[2]/input').text
        print('############################## 2')
        print('AQUI',config_internet_senha_valor)
        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> REDE LOCAL'
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > REDE LOCAL
        ### ------------------------------------------ ###
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        config_redelocal = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[2]/a/span')
        config_redelocal.click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        config_redelocal_dhcp = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/thead/tr/th').text
        print(config_redelocal_dhcp)
        config_redelocal_servidordhcp = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[2]/td[1]/span').text.strip(': ')
        print(config_redelocal_servidordhcp)
        config_redelocal_servidordhcp_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
        if config_redelocal_servidordhcp_valor == 'true':
            config_redelocal_servidordhcp_valor = 'Habilitado'
        else:
            config_redelocal_servidordhcp_valor = 'Desabilitado'
        print(config_redelocal_servidordhcp_valor)
        config_redelocal_iphgu = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[1]/span').text.strip(': ')
        print(config_redelocal_iphgu)
        config_redelocal_iphgu_valor01 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[1]').get_property('value')
        config_redelocal_iphgu_valor02 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[2]').get_property('value')
        config_redelocal_iphgu_valor03 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[3]').get_property('value')
        config_redelocal_iphgu_valor04 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[4]').get_property('value')
        config_redelocal_iphgu_valor = config_redelocal_iphgu_valor01 + '.' + config_redelocal_iphgu_valor02 + '.' + config_redelocal_iphgu_valor03 + '.' + config_redelocal_iphgu_valor04
        print(config_redelocal_iphgu_valor)

        config_redelocal_mask = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[1]/span').text.strip(': ')
        print(config_redelocal_mask)
        config_redelocal_mask_valor01 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[2]/input[1]').get_property('value')
        config_redelocal_mask_valor02 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[2]/input[2]').get_property('value')
        config_redelocal_mask_valor03 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[2]/input[3]').get_property('value')
        config_redelocal_mask_valor04 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[2]/input[4]').get_property('value')
        config_redelocal_mask_valor = config_redelocal_mask_valor01 + '.' + config_redelocal_mask_valor02 + '.' + config_redelocal_mask_valor03 + '.' + config_redelocal_mask_valor04
        print(config_redelocal_mask_valor)

        config_redelocal_pool = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[1]/span').text.strip(': ')
        print(config_redelocal_pool)
        config_redelocal_pool_valor_ini01 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[1]').get_property('value')
        config_redelocal_pool_valor_ini02 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[2]').get_property('value')
        config_redelocal_pool_valor_ini03 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[3]').get_property('value')
        config_redelocal_pool_valor_ini04 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[4]').get_property('value')
        config_redelocal_pool_ini_valor = config_redelocal_pool_valor_ini01 + '.' + config_redelocal_pool_valor_ini02 + '.' + config_redelocal_pool_valor_ini03 + '.' + config_redelocal_pool_valor_ini04
        config_redelocal_pool_valor_fin01 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[1]').get_property('value')
        config_redelocal_pool_valor_fin02 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[2]').get_property('value')
        config_redelocal_pool_valor_fin03 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[3]').get_property('value')
        config_redelocal_pool_valor_fin04 = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[4]').get_property('value')
        config_redelocal_pool_fin_valor = config_redelocal_pool_valor_fin01 + '.' + config_redelocal_pool_valor_fin02 + '.' + config_redelocal_pool_valor_fin03 + '.' + config_redelocal_pool_valor_fin04
        print(config_redelocal_pool_ini_valor)
        print(config_redelocal_pool_fin_valor)

        config_redelocal_dns = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[7]/td[1]/span').text.strip(': ')
        print(config_redelocal_dns)
        config_redelocal_dns_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[7]/td[2]/input[1]').get_attribute('checked')
        if config_redelocal_dns_valor == 'true':
            config_redelocal_dns_valor = 'Habilitado'
        else:
            config_redelocal_dns_valor = 'Desabilitado'
        print(config_redelocal_dns_valor)

        config_redelocal_concessao = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[10]/td[1]/span').text.strip(': ')
        print(config_redelocal_concessao)
        config_redelocal_concessao_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[1]/tbody/tr[10]/td[2]/input').get_property('value')
        print(config_redelocal_concessao_valor)

        config_redelocal_tabela_concessao = self._driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div[3]/form/table[4]')
        for i in config_redelocal_tabela_concessao:
            ths = i.find_elements_by_tag_name('th')
            print([th.text for th in ths])
            tds = i.find_elements_by_tag_name('td')
            print([td.text for td in tds])

        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> WIFI 2.4GHz '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > WIFI 2.4GHz
        ### ------------------------------------------ ###
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        config_wifi24 = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[3]/a/span')
        print(config_wifi24.text)
        config_wifi24.click()
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        time.sleep(5)
        config_wifi24 = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/h3/span').text.strip(': ')
        config_wifi24_basico = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/thead/tr/th/span').text.strip(': ')
        print(config_wifi24_basico)
        config_wifi24_basico_redeprivada = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[1]/span').text.strip(': ')
        print(config_wifi24_basico_redeprivada)
        config_wifi24_basico_redeprivada_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').get_attribute('checked')
        if config_wifi24_basico_redeprivada_valor == 'true':
            config_wifi24_basico_redeprivada_valor = 'Habilitado' 
        else:
            config_wifi24_basico_redeprivada_valor = 'Desabilitado'
        print(config_wifi24_basico_redeprivada_valor)
        
        config_wifi24_basico_anuncio = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[2]/td[1]/span').text.strip(': ')
        print(config_wifi24_basico_anuncio)
        config_wifi24_basico_anuncio_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
        if config_wifi24_basico_anuncio_valor == 'true':
            config_wifi24_basico_anuncio_valor = 'Habilitado'
        else:
            config_wifi24_basico_anuncio_valor = 'Desabilitado'
        print(config_wifi24_basico_anuncio_valor)

        config_wifi24_basico_ssid = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[1]/span').text.strip(': ')
        print(config_wifi24_basico_ssid)
        config_wifi24_basico_ssid_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input').get_property('value')
        print(config_wifi24_basico_ssid_valor)

        config_wifi24_basico_ssid_senha = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[1]/span').text.strip(': ')
        print(config_wifi24_basico_ssid_senha)
        config_wifi24_basico_ssid_senha_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input[1]').get_property('value')
        print(config_wifi24_basico_ssid_senha_valor)
        config_wifi24_basico_seguranca = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[5]/td[1]/span').text.strip(': ')
        print(config_wifi24_basico_seguranca)
        config_wifi24_basico_seguranca_valor = Select(self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[5]/td[2]/select')).first_selected_option.text
        print(config_wifi24_basico_seguranca_valor)

        config_wifi24_basico_wps = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[6]/td[1]/span').text.strip(': ')
        print(config_wifi24_basico_wps)
        config_wifi24_basico_wps_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[6]/td[2]/input[1]').get_attribute('checked')
        if config_wifi24_basico_wps_valor == 'true':
            config_wifi24_basico_wps_valor = 'Habilitado'
        else:
            config_wifi24_basico_wps_valor = 'Desabilitado'
        print(config_wifi24_basico_wps_valor)

        config_wifi24_avancado = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/ul/li[2]/a')
        config_wifi24_avancado.click()
        time.sleep(1)
        config_wifi24_avancado = config_wifi24_avancado.text
        print(config_wifi24_avancado)

        config_wifi24_avancado_modooperacao = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[1]/td[1]/span').text.strip(': ')
        print(config_wifi24_avancado_modooperacao)
        config_wifi24_avancado_modooperacao_valor = Select(self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[1]/td[2]/select')).first_selected_option.text
        print(config_wifi24_avancado_modooperacao_valor)

        config_wifi24_avancado_canal = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[2]/td[1]/span').text
        print(config_wifi24_avancado_canal)
        config_wifi24_avancado_canal_valor = Select(self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[2]/td[2]/select')).first_selected_option.text
        print(config_wifi24_avancado_canal_valor)

        config_wifi24_avancado_largurabanda = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[3]/td[1]/span').text.strip(': ')
        print(config_wifi24_avancado_largurabanda)
        config_wifi24_avancado_largurabanda_valor = Select(self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[3]/td[2]/select')).first_selected_option.text
        print(config_wifi24_avancado_largurabanda_valor)

        config_wifi24_avancado_wmm = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[4]/td[1]/span').text.strip(': ')
        print(config_wifi24_avancado_wmm)
        config_wifi24_avancado_wmm_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[4]/td[2]/input[1]').get_attribute('checked')
        if config_wifi24_avancado_wmm_valor == 'true' :
            config_wifi24_avancado_wmm_valor = 'Habilitado' 
        else:
            config_wifi24_avancado_wmm_valor = 'Desabilitado'
        print(config_wifi24_avancado_wmm_valor)


        config_wifi24_avancado_mac = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[6]/td[1]/span').text
        print(config_wifi24_avancado_mac)
        config_wifi24_avancado_mac_valor = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[4]/form/table[1]/tbody/tr[6]/td[2]').text
        print(config_wifi24_avancado_mac_valor)

        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> WIFI 5GHz '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > WIFI 5GHz
        ### ------------------------------------------ ###
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        config_wifi5 = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[4]/a/span')
        print(config_wifi5.text)
        config_wifi5.click()
        time.sleep(2)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        config_wifi5_basico = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/thead/tr/th/span').text
        print(config_wifi5_basico)
        config_wifi5_basico_redeprivada = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[1]/span').text.strip(': ')
        print(config_wifi5_basico_redeprivada)
        config_wifi5_basico_redeprivada_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').get_attribute('checked')
        if config_wifi5_basico_redeprivada_valor == 'true':
            config_wifi5_basico_redeprivada_valor = 'Habilitado'
        else:
            config_wifi5_basico_redeprivada_valor = 'Desabilitado'
        print(config_wifi5_basico_redeprivada_valor)

        config_wifi5_basico_anuncio = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[2]/td[1]/span').text.strip(': ')
        print(config_wifi5_basico_anuncio)
        config_wifi5_basico_anuncio_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
        if config_wifi5_basico_anuncio_valor == 'true':
            config_wifi5_basico_anuncio_valor = 'Habilitado'
        else:
            config_wifi5_basico_anuncio_valor = 'Desabilitado'
        print(config_wifi5_basico_anuncio_valor)

        config_wifi5_basico_ssid = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[1]/span').text.strip(': ')
        print(config_wifi5_basico_ssid)
        config_wifi5_basico_ssid_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input').get_property('value')
        print(config_wifi5_basico_ssid_valor)

        config_wifi5_basico_ssid_senha = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[1]/span').text.strip(': ')
        print(config_wifi5_basico_ssid_senha)
        config_wifi5_basico_ssid_senha_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input').get_property('value')
        print(config_wifi5_basico_ssid_senha_valor)
        config_wifi5_basico_seguranca = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[5]/td[1]/span').text.strip(': ')
        print(config_wifi5_basico_seguranca)
        config_wifi5_basico_seguranca_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[5]/td[2]/select')).first_selected_option.text
        print(config_wifi5_basico_seguranca_valor)

        config_wifi5_basico_wps = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[6]/td[1]').text
        print(config_wifi5_basico_wps)
        config_wifi5_basico_wps_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/form/table/tbody/tr[6]/td[2]/input[1]').get_attribute('checked')
        if config_wifi5_basico_wps_valor == 'true':
            config_wifi5_basico_wps_valor = 'Habilitado'
        else:
            config_wifi5_basico_wps_valor = 'Desabilitado'
        print(config_wifi5_basico_wps_valor)

        config_wifi5_avancado = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[2]/ul/li[2]/a/span')
        config_wifi5_avancado.click()
        time.sleep(1)
        config_wifi5_avancado = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/thead/tr/th/span').text
        print(config_wifi5_avancado)

        config_wifi5_avancado_modooperacao = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[1]/td[1]/span').text.strip(': ')
        print(config_wifi5_avancado_modooperacao)
        config_wifi5_avancado_modooperacao_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[1]/td[2]/select')).first_selected_option.text
        print(config_wifi5_avancado_modooperacao_valor)

        config_wifi5_avancado_canal = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[2]/td[1]/span').text.strip(': ')
        print(config_wifi5_avancado_canal)
        config_wifi5_avancado_canal_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[2]/td[2]/select')).first_selected_option.text
        print(config_wifi5_avancado_canal_valor)

        config_wifi5_avancado_largurabanda = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[3]/td[1]/span').text.strip(': ')
        print(config_wifi5_avancado_largurabanda)
        config_wifi5_avancado_largurabanda_valor = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[3]/td[2]/select')).first_selected_option.text
        print(config_wifi5_avancado_largurabanda_valor)

        config_wifi5_avancado_wmm = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[4]/td[1]').text.strip(": ")
        print(config_wifi5_avancado_wmm)
        config_wifi5_avancado_wmm_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[4]/td[2]/input[1]').get_attribute('checked')
        if config_wifi5_avancado_wmm_valor == 'true' :
            config_wifi5_avancado_wmm_valor = 'Habilitado' 
        else:
            config_wifi5_avancado_wmm_valor = 'Desabilitado'
        print(config_wifi5_avancado_wmm_valor)

        config_wifi5_avancado_mac = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[5]/td[1]/span').text.strip(': ')
        print(config_wifi5_avancado_mac)
        config_wifi5_avancado_mac_valor = self._driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[4]/form/table[1]/tbody/tr[5]/td[2]').text
        print(config_wifi5_avancado_mac_valor)
          
        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> FIREWALL '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > FIREWALL
        ### ------------------------------------------ ###
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        config_firewall = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[6]/a/span')
        config_firewall.click()
        config_firewall = config_firewall.text
        print(config_firewall)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        
        time.sleep(2)
        config_firewall_politicapadrao = self._driver.find_element_by_xpath('/html/body/form/div[1]/div/div[1]/table/thead[1]/tr/th/span').text
        print(config_firewall_politicapadrao)
        config_firewall_politicapadrao_status = self._driver.find_element_by_xpath('/html/body/form/div[1]/div/div[1]/table/tbody[1]/tr/td[1]/span').text.strip(': ')
        print(config_firewall_politicapadrao_status)
        config_firewall_politicapadrao_valor = self._driver.find_element_by_xpath('/html/body/form/div[1]/div/div[1]/table/tbody[1]/tr/td[2]/input[1]').get_attribute('checked')
        if config_firewall_politicapadrao_valor == 'true':
            config_firewall_politicapadrao_valor = 'Aceita'
        else:
            config_firewall_politicapadrao_valor = 'Rejeita'
        print(config_firewall_politicapadrao_valor)

        config_firewall_pingwan = self._driver.find_element_by_xpath('/html/body/form/div[1]/div/div[1]/table/thead[2]/tr/th').text.strip(': ')
        print(config_firewall_pingwan)
        config_firewall_pingwan_status = self._driver.find_element_by_xpath('/html/body/form/div[1]/div/div[1]/table/tbody[2]/tr/td[1]/span').text.strip(': ')
        print(config_firewall_pingwan_status)
        config_firewall_pingwan_valor = self._driver.find_element_by_xpath('/html/body/form/div[1]/div/div[1]/table/tbody[2]/tr/td[2]/input[1]').get_attribute('checked')
        if config_firewall_pingwan_valor == 'true':
            config_firewall_pingwan_valor = 'Aceita'
        else:
            config_firewall_pingwan_valor = 'Rejeita'
        print(config_firewall_pingwan_valor)



        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> CONFIGURAÇÕES >> MODO DA WAN '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > MODO DA WAN
        ### ------------------------------------------ ###
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        config_modowan = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[7]/a/span')
        print(config_modowan.text)
        config_modowan.click()
        config_modowan = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[2]/ul/li[7]/a/span').text
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        config_modowan_bridge = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/thead/tr/th/span').text
        print(config_modowan_bridge)

        config_modowan_bridge_modo = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[1]/span').text.strip(': ')
        print(config_modowan_bridge_modo)
        config_modowan_bridge_modo_valor = Select(self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/select')).first_selected_option.text
        print(config_modowan_bridge_modo_valor)

        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> GERENCIAMENTO >> IDIOMA '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > IDIOMA
        ### ------------------------------------------ ###
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        gerenciamento = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[3]/a/span')
        print(gerenciamento.text)
        gerenciamento.click()
        gerenciamento = gerenciamento.text
        time.sleep(2)
        gerenciamento_idioma = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[3]/ul/li[1]/a/span')
        gerenciamento_idioma.click()
        gerenciamento_idioma = gerenciamento_idioma.text
        print(gerenciamento_idioma)
        time.sleep(2)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        gerenciamento_idioma = self._driver.find_element_by_xpath('/html/body/form/div/div/div/table/thead/tr/th/span').text
        print(gerenciamento_idioma)
        gerenciamento_idioma_valor = self._driver.find_element_by_xpath('/html/body/form/div/div/div/table/tbody/tr[2]/td/label[1]/input').get_attribute('checked')
        if gerenciamento_idioma_valor == 'true':
            gerenciamento_idioma_valor = 'Português'
        else:
            gerenciamento_idioma_valor = 'Inglês'
        print(gerenciamento_idioma_valor)

        time.sleep(1)
        print('\n#############################################'
                '\n MENU >> SOBRE O DISPOSITIVO  '
                '\n#############################################\n')
        ### ------------------------------------------ ###
        ###         CONFIGURAÇÕES > SOBRE O DISPOSITIVO
        ### ------------------------------------------ ###
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        sobre = self._driver.find_element_by_xpath('/html/body/div[1]/div/div/ul/li[4]/a/span')
        print(sobre.text)
        sobre.click()
        time.sleep(2)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        sobre = self._driver.find_element_by_xpath('/html/body/div/div[1]/h3/span').text
        info_dispositivo = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/thead/tr/th/span').text
        print(info_dispositivo)
        info_dispositivo_fabricante = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[1]/td[1]/strong/span').text.strip(': ')
        print(info_dispositivo_fabricante)
        info_dispositivo_fabricante_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[1]/td[2]').text
        print(info_dispositivo_fabricante_valor)

        info_dispositivo_firmware = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[2]/td[1]/strong/span').text
        print(info_dispositivo_firmware)
        info_dispositivo_firmware_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[2]/td[2]').text
        print(info_dispositivo_firmware_valor)

        info_dispositivo_serial = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[3]/td[1]/strong/span').text
        print(info_dispositivo_serial)
        info_dispositivo_serial_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[3]/td[2]').text
        print(info_dispositivo_serial_valor)

        info_dispositivo_macwan = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[4]/td[1]/strong/span').text
        print(info_dispositivo_macwan)
        info_dispositivo_macwan_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[4]/td[2]').text
        print(info_dispositivo_macwan_valor)

        info_dispositivo_modelo = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[1]/td[3]/strong/span').text.strip(': ')
        print(info_dispositivo_modelo)
        iinfo_dispositivo_modelo_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[1]/td[4]').text
        print(iinfo_dispositivo_modelo_valor)

        info_dispositivo_hardware = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[2]/td[3]/strong/span').text
        print(info_dispositivo_hardware)
        info_dispositivo_hardware_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[2]/td[4]').text
        print(info_dispositivo_hardware_valor)

        info_dispositivo_serialgpon = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[3]/td[3]/strong/span').text.strip(': ')
        print(info_dispositivo_serialgpon)
        info_dispositivo_serialgpon_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[3]/td[4]').text
        print(info_dispositivo_serialgpon_valor)

        info_dispositivo_maclan = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[4]/td[3]/strong/span').text.strip(': ')
        print(info_dispositivo_maclan)
        info_dispositivo_maclan_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/table[1]/tbody/tr[4]/td[4]').text
        print(info_dispositivo_maclan_valor)




        print('\n\n\n == Criando JSON de saída... == ')
        print(gpon, internet, detalhes_IPv6_head)
        dict_saida425 = {
                        "Status":
                            {
                            gpon:
                                {
                                    divOptical[0]:divOptical[1],
                                    divOptRx[0]:divOptRx[1],
                                    divOptTx[0]:divOptTx[1]
                                },
                            internet:
                                {
                                    divPpp[0]: divPpp[1],
                                    detalhes_IPv4_head:
                                        {
                                            detalhes_IPv4_nome[0]: detalhes_IPv4_valor[0],
                                            detalhes_IPv4_nome[1]: detalhes_IPv4_valor[1],
                                            detalhes_IPv4_nome[2]: detalhes_IPv4_valor[2],
                                            detalhes_IPv4_nome[3]: detalhes_IPv4_valor[3],
                                            detalhes_IPv4_nome[4]: detalhes_IPv4_valor[4]
                                        },
                                    detalhes_IPv6_head:
                                        {
                                            detalhes_IPv6_nome[0]: detalhes_IPv6_valor[0],
                                            detalhes_IPv6_nome[1]: detalhes_IPv6_valor[1],
                                            detalhes_IPv6_nome[2]: detalhes_IPv6_valor[2],
                                            detalhes_IPv6_nome[3]: detalhes_IPv6_valor[3],
                                            detalhes_IPv6_nome[4]: detalhes_IPv6_valor[4],
                                            detalhes_IPv6_nome[5]: detalhes_IPv6_valor[5]
                                        }
                                },
                            wifi_24:
                                {
                                    wifi_24_valor[0]: wifi_24_valor[1],
                                    wifi_24_valor[2]: wifi_24_valor[3],
                                    wifi_24_valor[4]: wifi_24_valor[5],
                                    wifi_24_valor[6]: wifi_24_valor[7],
                                    "Estações Conectadas:": wifi_24_detalhes_stations
                                },
                            wifi_5:
                                {
                                    wifi_5_valor[0]: wifi_5_valor[1],
                                    wifi_5_valor[2]: wifi_5_valor[3],
                                    wifi_5_valor[4]: wifi_5_valor[5],
                                    wifi_5_valor[6]: wifi_5_valor[7],
                                    "Estações Conectadas:": wifi_5_detalhes_stations
                                },
                            rede_local:
                                {
                                    rede_local_name[0]: rede_local_name[1],
                                    rede_local_name[2]: rede_local_name[3],
                                    rede_local_name[4]: rede_local_name[5],
                                    "Estações Conectadas:": rede_local_stations
                                },
                            tv:
                                {
                                    tv_valor[0]: tv_valor[1],
                                    tv_valor[2]: tv_valor[3],
                                    "Estações Conectadas:": tv_stations
                                },
                            telefone:
                                {
                                    telefone_info_rede[0]: telefone_info_rede[1],
                                    telefone_info_status[0]: telefone_info_status[1],
                                    # "Estações Conectadas:": telefone_stations
                                }
                            },
                        "Configurações":
                            {
                                "Internet":
                                    {
                                        config_internet_usuario: config_internet_usuario_valor,
                                        config_internet_senha: config_internet_senha_valor
                                    },
                                rede_local:
                                    {
                                        config_redelocal_dhcp:config_redelocal_servidordhcp_valor,
                                        config_redelocal_iphgu:config_redelocal_iphgu_valor,
                                        config_redelocal_mask:config_redelocal_mask_valor,
                                        config_redelocal_pool:
                                            {
                                                "inicio:":config_redelocal_pool_ini_valor,
                                                "fim:":config_redelocal_pool_fin_valor
                                            },
                                        config_redelocal_dns:config_redelocal_dns_valor,
                                        config_redelocal_concessao:config_redelocal_concessao_valor
                                    },
                                'Rede Wifi 2.4Ghz':
                                    {
                                        config_wifi24_basico:
                                            {
                                                config_wifi24_basico_redeprivada:config_wifi24_basico_redeprivada_valor,
                                                config_wifi24_basico_anuncio:config_wifi24_basico_anuncio_valor,
                                                config_wifi24_basico_ssid:config_wifi24_basico_ssid_valor,
                                                config_wifi24_basico_ssid_senha:config_wifi24_basico_ssid_senha_valor,
                                                config_wifi24_basico_seguranca:config_wifi24_basico_seguranca_valor,
                                                config_wifi24_basico_wps:config_wifi24_basico_wps_valor
                                            },
                                        config_wifi24_avancado:
                                            {
                                                config_wifi24_avancado_modooperacao:config_wifi24_avancado_modooperacao_valor,
                                                config_wifi24_avancado_canal:config_wifi24_avancado_canal_valor,
                                                config_wifi24_avancado_largurabanda:config_wifi24_avancado_largurabanda_valor,
                                                config_wifi24_avancado_mac:config_wifi24_avancado_mac_valor
                                            }
                                    },
                                'Rede Wifi 5Ghz':
                                    {
                                        config_wifi5_basico:
                                            {
                                                config_wifi5_basico_redeprivada: config_wifi5_basico_redeprivada_valor,
                                                config_wifi5_basico_anuncio: config_wifi5_basico_anuncio_valor,
                                                config_wifi5_basico_ssid: config_wifi5_basico_ssid_valor,
                                                config_wifi5_basico_ssid_senha: config_wifi5_basico_ssid_senha_valor,
                                                config_wifi5_basico_seguranca: config_wifi5_basico_seguranca_valor,
                                                config_wifi5_basico_wps: config_wifi5_basico_wps_valor
                                            },
                                        config_wifi5_avancado:
                                            {
                                                config_wifi5_avancado_modooperacao: config_wifi5_avancado_modooperacao_valor,
                                                config_wifi5_avancado_canal: config_wifi5_avancado_canal_valor,
                                                config_wifi5_avancado_largurabanda: config_wifi5_avancado_largurabanda_valor,
                                                config_wifi5_avancado_wmm: config_wifi5_avancado_wmm_valor,
                                                config_wifi5_avancado_wmm: config_wifi5_avancado_wmm_valor,
                                                config_wifi5_avancado_mac: config_wifi5_avancado_mac_valor
                                            }
                                    },
                                "Firewall":
                                    {
                                        config_firewall_politicapadrao:
                                            {
                                                config_firewall_politicapadrao_status:config_firewall_politicapadrao_valor
                                            },
                                        config_firewall_pingwan:
                                            {
                                                config_firewall_pingwan_status:config_firewall_pingwan_valor
                                            }
                                    },
                                "Modo da Wan":
                                    {
                                        config_modowan_bridge:
                                            {
                                                config_modowan_bridge_modo:config_modowan_bridge_modo_valor
                                            }
                                    }
                            },
                        gerenciamento:
                            {
                                gerenciamento_idioma:gerenciamento_idioma_valor
                            },
                        sobre:
                            {
                                info_dispositivo:
                                    {
                                        info_dispositivo_fabricante:info_dispositivo_fabricante_valor,
                                        info_dispositivo_firmware:info_dispositivo_firmware_valor,
                                        info_dispositivo_serial:info_dispositivo_serial_valor,
                                        info_dispositivo_macwan:info_dispositivo_macwan_valor,
                                        info_dispositivo_modelo:iinfo_dispositivo_modelo_valor,
                                        info_dispositivo_hardware:info_dispositivo_hardware_valor,
                                        info_dispositivo_serialgpon:info_dispositivo_serialgpon_valor,
                                        info_dispositivo_maclan:info_dispositivo_maclan_valor
                                    }
                            }
                        }

        self._driver.quit()

        print(dict_saida425)
        user = dict_saida425['Configurações']['Internet'].get('Usuário')
        if user == 'cliente@cliente':
            self._dict_result.update({"Resultado_Probe": "OK", "obs": "Usuario: cliente@cliente", "result":"passed"})
        else:
            self._dict_result.update({"obs": f"Teste incorreto, retorno Usuario: {user}"})

        self.update_global_result_memory(flask_username, 'getFullConfig_425', dict_saida425)
        return self._dict_result
        

    def verificarSenhaPppDefaultFibra_426(self, flask_username):
        self._dict_result.update({'result':'failed',"obs": TEST_NOT_IMPLEMENTED_WARNING})
        return self._dict_result

    

    def checkWanInterface_x_427(self, flask_username, interface):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)
            
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            wanInterface = self._driver.find_element_by_xpath('//*[@id="network-broadband"]/a').click()
    
            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
    
            interface_edit = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div/ul/li/div/table/tbody/tr[2]/td[9]/div/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            time.sleep(1)
            gpon_wan_interface_form_input  = self._driver.find_elements_by_xpath('/html/body/div[3]/div[2]/form/div[1]/div/ul//input')
            dict_saida427 = {}
            for input in gpon_wan_interface_form_input:
                if input.get_attribute('value'):
                    if (input.get_attribute('type') == 'radio' and not input.get_attribute('checked')):
                        continue
                    else:
                        dict_saida427.update({input.get_attribute('name'): input.get_attribute('value') 
                                                                    if input.get_attribute('type') == 'radio'
                                                                    else input.get_attribute('checked') 
                                                                    if input.get_attribute('checked') 
                                                                    else input.get_attribute('value')})
            else:
                dhcp_ipv6 = {'0': 'SLAAC', '1': 'DHCP'}
                dict_saida427 = {k: (v if k!='PPPIPv6ModeRadio' else dhcp_ipv6[v])  for k,v in dict_saida427.items()}

                ip_stack = {'0': 'ipv4', '1': 'Dual Stack', '2': 'ipv6'}
                dict_saida427 = {k: (v if k!='ipv6Flag' else ip_stack[v])  for k,v in dict_saida427.items()}

            if dict_saida427['ipv6Flag'] == 'Dual Stack':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Dual Stack", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno IPv6: {dict_saida427['ipv6Flag']}"})

            print(dict_saida427)
            self._driver.quit()
        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            self.update_global_result_memory(flask_username, 'checkWanInterface_x_427', dict_saida427)
            return self._dict_result
            

    def validarDHCPv6Wan_428(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 427 primeiro"})
        else:
            ans_428 = result['PPPIPv6ModeRadio']
            if 'SLAAC' == ans_428:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6 Radio: SLAAC", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno IPv6 Radio: {ans_428}"})
        return self._dict_result


    def checkLANSettings_429(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)
            
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            self._driver.find_element_by_xpath('//*[@id="network-homeNetworking"]/a').click()
    
            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)

            lan_form_input  = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul//input')
            dict_saida429 = {}
            for input in lan_form_input:
                try:
                    if input.get_attribute('value'):
                        if input.get_property('type') =='radio' and input.get_attribute('checked'):
                            dict_saida429.setdefault(input.get_attribute('name'), input.get_attribute('value'))
                        elif input.get_property('type') != 'radio':
                            dict_saida429.setdefault(input.get_attribute('name'), input.get_attribute('value'))

  
                except Exception as e:
                    print(e)


            self._driver.find_element_by_xpath('//*[@id="t4"]/span').click()
            time.sleep(2)

            ipv6_dict_form = {}                     
            ipv6_form_input = self._driver.find_elements_by_xpath('//*[@id="contentPanel"]/form/div/div[2]/ul//input')

            for input in ipv6_form_input:
                try:
                    if input.get_attribute('value'):
                        ipv6_dict_form.update({input.get_attribute('name'): 
                                                                       input.get_attribute('value') 
                                                                       if input.get_property('type')=='radio' 
                                                                       else input.get_attribute('checked') 
                                                                       if input.get_attribute('checked') 
                                                                       else input.get_attribute('value')})
                except Exception as e:
                    print(e)
            else:
                link_local = {'Yes': 'Manual', 'No': 'EUI64'}
                ipv6_dict_form = {k: (v if (k!='linklocal_type' and 
                                            k!='rs_identifer') else link_local[v])  
                                       for k,v in ipv6_dict_form.items()}

                link_local = {'0': 'PVC0', '1': 'PVC1','2': 'PVC2', '3': 'PVC3','4': 'PVC4', '5': 'PVC5','6': 'PVC6', '7': 'PVC7'}
                ipv6_dict_form = {k: (v if (k!='LanDelegateStaticFlag_H') else link_local[v])  
                                       for k,v in ipv6_dict_form.items()}


            dict_saida429.update(ipv6_dict_form)

            if dict_saida429['LanDelegateStaticFlag_H'] == 'PVC0':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefixo Delegado da WAN: PVC0", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Prefixo Delegado da WAN: {dict_saida429['LanDelegateStaticFlag_H']}"})

            self._driver.quit()
            
            print(dict_saida429)

        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            self.update_global_result_memory(flask_username, 'checkLANSettings_429', dict_saida429)
            return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_431(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('Encapsulamento')
                if iface_type == 'PPPoE' and cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if sub_dict.get('VID/Prioridade') == '8,35':
                        self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VID/Prioridade: 8,35', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: PPPoE, VID/Prioridade: {sub_dict.get('VID/Prioridade')}"})
                        break
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_432(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('VID/Prioridade').split('/')[0]
                if iface_type == '8,35' and cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if sub_dict.get('Encapsulamento') == 'PPPoE':
                        self._dict_result.update({"obs": 'VID/Prioridade: 8,35 Encapsulamento: PPPoE', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs":  f"Teste incorreto, retorno VID/Prioridade: {iface_type}, Encapsulamento: {sub_dict.get('Encapsulamento')}"})
                        break
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_433(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkNatSettings_423')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 423 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for _, row in result.items():
                interface = row.get('#')
                if interface == '1' and cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if row['NAT'] == 'Enable':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: Interface 1, Adm.State: Enable", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Interface: Interface 1, Adm.State: {row['NAT']}"})
                        break
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}" })
        return self._dict_result


    def checkMulticastSettings_434(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                try:
                    internet = result['Internet'] 
                    if internet == 'Nenhum':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "IGMP Internet: Desabilitado", "result":"passed"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno IGMP Internet: {internet}"})
                except:
                    self._dict_result.update({"obs": 'Interface Internet nao existe'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_usernamePppDefault_435(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 425 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            usuario = result['Configurações']['Internet']['Usuário']
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                if usuario == 'cliente@cliente':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Usuário: cliente@cliente', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno: Usuário: {usuario}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result

    
    def vivo_1_passwordPppDefault_436(self, flask_username):
        self._dict_result.update({'result':'failed',"obs": TEST_NOT_IMPLEMENTED_WARNING})
        return self._dict_result


    def checkWanInterface_x_437(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 427 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            iface_type = result['ipv6Flag']
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                if iface_type == 'Dual Stack':
                    self._dict_result.update({"obs": 'IPv6: Dual Stack', "result":'passed', "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno IPv6: {iface_type}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def validarDHCPv6Wan_438(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 427 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            iface_type = result['PPPIPv6ModeRadio']
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                if iface_type == 'SLAAC':
                    self._dict_result.update({"obs": 'PPPIPv6ModeRadio: SLAAC', "result":'passed', "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno PPPIPv6ModeRadio: {iface_type}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result
    

    def checkLANSettings_439(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 429 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                if result['LanDelegateStaticFlag_H'] == 'PVC0':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefixo Delegado da WAN: PVC0", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Prefixo Delegado da WAN: {result['LanDelegateStaticFlag_H']}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_441(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            for _, sub_dict in result.items():
                cpe_config = config_collection.find_one()
                if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if sub_dict.get('Encapsulamento') == 'PPPoE':
                        iface_type = sub_dict.get('VID/Prioridade').split('/')[0]
                        if iface_type == '0,35':
                            self._dict_result.update({"obs": 'Encapsulamento PPPoE, VID/Prioridade: 0,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VID/Prioridade: 0,35'})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: {sub_dict.get('Encapsulamento')}"})
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_442(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            for _, sub_dict in result.items():
                cpe_config = config_collection.find_one()
                iface_type = sub_dict.get('VID/Prioridade').split('/')[0]
                if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    if iface_type == '8,35':
                        if sub_dict.get('Encapsulamento') == 'PPPoE':
                            self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VID/Prioridade: 8,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: {sub_dict.get('Encapsulamento')}"})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno VID/Prioridade: {iface_type}"})
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_443(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkNatSettings_423')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 423 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            for _, row in result.items():
                interface = row.get('#')
                if interface == '1':
                    if row['NAT'] == 'Enable' and cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Interface: Interface 1, Adm.State: Enable", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Interface: Interface 1, Adm.State: {row['NAT']}, e REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
                        break
            else:
                self._dict_result.update({"obs": "Interface: Interface 1 nao existe" })
        return self._dict_result


    def checkMulticastSettings_444(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                try:
                    internet = result['Internet'] 
                    if internet == 'Nenhum':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "IGMP Internet: Desabilitado", "result":"passed"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno IGMP Internet: {internet}"})
                except:
                    self._dict_result.update({"obs": 'Interface Internet nao existe'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_2_usernamePppDefault_445(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        try:
            result = session.get_result_from_test(flask_username, 'getFullConfig_425')
            cpe_config = config_collection.find_one()
            usuario = result['Configurações']['Internet']['Usuário']
            #print('\n #445 usuario:', usuario)
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                if usuario == 'cliente@cliente':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Usuário: cliente@cliente', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno Usuário: {usuario}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        except Exception:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        finally:
            return self._dict_result

        
    def vivo_2_passwordPppDefault_446(self, flask_username):
        self._dict_result.update({'result':'failed',"obs": TEST_NOT_IMPLEMENTED_WARNING})
        return self._dict_result


    def validarDualStack_447(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            iface_type = result['ipv6Flag']
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':    

                if iface_type == 'Dual Stack':
                    self._dict_result.update({"obs": 'IPv6: Dual Stack', "result":'passed', "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": 'Teste incorreto, retorno IPv6: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def validarDHCPv6Wan_448(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            iface_type = result['PPPIPv6ModeRadio']
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':    
                if 'SLAAC' == iface_type:
                    self._dict_result.update({"obs": 'PPPIPv6ModeRadio: SLAAC', "result":'passed', "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": f"Testes incorreto, retorno PPPIPv6ModeRadio: {iface_type}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def prefixDelegationInet_449(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        try:
            result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        except Exception:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            for i, r in result.items():
                if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                    delegate = r['LanDelegateStaticFlag_H']
                    if delegate == 'PVC0':
                        self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefixo Delegado da WAN: PVC0", "result":"passed"})
                        break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Prefixo Delegado da WAN: {delegate}"})
                        break
                else:
                    self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        finally:
            return self._dict_result

    
    def vivo_1_vlanIdIptvVivo1_450(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            for _, sub_dict in result.items():
                cpe_config = config_collection.find_one()
                if cpe_config['REDE'] == 'VIVO_1': 
                    if sub_dict.get('Name') == 'Mediaroom':
                        iface_type = sub_dict.get('VID/Prioridade').split('/')[0]
                        print(iface_type)
                        if iface_type == '20':
                            self._dict_result.update({"obs": 'Name: Mediaroom,  VID: 20', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Name: Mediaroom,  VID:  {iface_type}"})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Name: {sub_dict.get('Name')}"})
                else:
                    self._dict_result.update({"obs": f"REDE: {cpe_config['REDE']}"})
                    break
        return self._dict_result

    
    def vivo_1_prioridadeIptv_451(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            for _, sub_dict in result.items():
                cpe_config = config_collection.find_one()
                if cpe_config['REDE'] == 'VIVO_1': 
                    if sub_dict.get('Name') == 'Mediaroom':
                        priority = sub_dict.get('VID/Prioridade').split('/')[-1]
                        if priority == '3':
                            self._dict_result.update({"obs": 'Name: Mediaroom,  Prioridade: 3', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Name: Mediaroom, Prioridade: {priority}"})
                            break
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Name: {sub_dict.get('Name')}"})
                else:
                    self._dict_result.update({"obs": f"REDE: {cpe_config['REDE']}"})
        return self._dict_result


    def vivo_1_validarNatIptv_452(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkNatSettings_423')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 423 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'Mediaroom':
                        if sub_dict.get('NAT') == 'Enable':
                            self._dict_result.update({"obs": 'Interface: Mediaroom | Adm.State: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Mediaroom | Adm.State: {sub_dict.get("Adm.State")}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    # def vivo_1_igmpIptv_453(self, flask_username):
    #     #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
    #     result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
    #     if len(result) == 0:
    #         self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
    #     else:
    #         cpe_config = config_collection.find_one()
    #         print("-----------------",result['igmp_quickleave_act']['type'])
    #         igmp_check = result['igmp_quickleave_act']['type']
    #         if cpe_config['REDE'] == 'VIVO_1':
    #             if result['igmp_snoop_act']['type'] == 'Ativado':
    #                 self._dict_result.update({"obs": 'Interface: Mediaroom, IGMP Snoop Act: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
    #             else:
    #                 self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Mediaroom, IGMP Snoop Act: {igmp_check}'})
    #         else:
    #             self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
    #     return self._dict_result


    def vivo_1_igmpIptv_453(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                try:
                    igmp_check = result['Internet']
                    if igmp_check != 'Nenhum':
                        self._dict_result.update({"obs": 'Interface: Internet, IGMP Snoop Act: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Internet, IGMP: {igmp_check}'})
                except:
                    self._dict_result.update({"obs": 'Interface Internet nao existe'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vlanIdVodVivo2_454(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        print(result)
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'Multicast':
                        vid = sub_dict.get('VID/Prioridade').split('/')[0]
                        if vid == '602':
                            self._dict_result.update({"obs": 'Name: Multicast, VLAN: 602', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: Multicast, VID: {vid}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo2_validarNatIPTV_455(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 e 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        result2 = session.get_result_from_test(flask_username, 'checkNatSettings_423')
        if len(result) == 0 and len(result2) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 e 423 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_name = 'ipNotFound'
                    iface_type = sub_dict.get('VID/Prioridade').split('/')[-1]
                    cpe_config = config_collection.find_one()
                    if iface_type == '3':
                        if sub_dict.get('VID/Prioridade').split('/')[0] == '602':
                            iface_name = sub_dict.get('Name')
                            break
                # 2
                for _, sub_dict in result2.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == iface_name:
                        if sub_dict.get('NAT') == 'Enable':
                            self._dict_result.update({"obs": 'Adm.State:  Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Adm.State: {sub_dict.get("NAT")} '})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name 1: {iface_type}, Name 2: {iface_name} '})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
            
        return self._dict_result


    # def vivo_2_igmpVoD_456(self, flask_username):
    #     #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
    #     result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
    #     if len(result) == 0:
    #         self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
    #     else:
    #         cpe_config = config_collection.find_one()
    #         if cpe_config['REDE'] == 'VIVO_2':
    #             for i, row in result.items():
    #                 if i == 'ip5':
    #                     if row['type'] == 'Ativado':
    #                         self._dict_result.update({"obs": 'Interface: ip5 | IGMP Quickleave Habilitado', "result":'passed', "Resultado_Probe":"OK"})
    #                         break
    #                     else:
    #                         self._dict_result.update({"obs": f"Teste incorreto, retorno Interface: ip5 | IGMP Quickleave: {row['type']}"})
    #                         break
    #                 else:
    #                     self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {i}'})
    #         else:
    #             self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
    #     return self._dict_result


    def vivo_2_igmpVoD_456(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                igmp_check = result['Multicast']
                if igmp_check != 'Nenhum':
                    self._dict_result.update({"obs": 'Interface: Mediaroom, IGMP: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Mediaroom, IGMP: {igmp_check}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vlanIdMulticastVivo2_457(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": f'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'Multicast':
                        if sub_dict.get('VID/Prioridade').split('/')[0] == '4000':
                            self._dict_result.update({"obs": 'Name: Multicast | VID: 4000', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: Multicast | VID: {sub_dict.get("VID/Prioridade").split("/")[0]} '})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result

        
    def natMulticastVivo2_458(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkNatSettings_423')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 423 primeiro'})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict.get('Name')
                if iface_type == 'Mediaroom':
                    if sub_dict.get('NAT') == 'Disable':
                        self._dict_result.update({"obs": 'Interface: Mediaroom | Adm.State: Desabilitado', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Mediaroom | Adm.State: {sub_dict.get("Adm.State")} '})
                        break
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
        return self._dict_result


    # def checkIGMPVivo2_459(self, flask_username):
    #     #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
    #     result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
    #     result1 = session.get_result_from_test(flask_username, 'checkWanInterface_420')
    #     if len(result) == 0 and len(result1) == 0:
    #         self._dict_result.update({"obs": 'Execute o teste 420 e 424 primeiro'})
    #     else:
    #         ip = result1['index_2'].get('IP')
    #         iface_type = 'ipNotFound'
    #         for i, sub_dict in result.items():
    #             if i == 'uiViewIPAddr':
    #                 iface_type = sub_dict['value']
    #             if iface_type == ip:
    #                 igmp = result['igmp_quickleave_act'].get('type')
    #                 if igmp == 'Disable':
    #                     self._dict_result.update({"obs": f'Interface: {iface_type} | IGMP: Ativado', "result":'passed', "Resultado_Probe":"OK"})
    #                     break
    #                 self._dict_result.update({"obs": f"Teste incorreto, retorno Interface: {iface_type} | IGMP: {sub_dict.get('type')}"})
    #                 break
    #             else:
    #                 self._dict_result.update({"obs":  f'Teste incorreto, retorno Interface: {iface_type}'})
    #     return self._dict_result

    def checkIGMPVivo2_459(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0: 
            self._dict_result.update({"obs": 'Execute o teste 424 primeiro'})
        else:
            try:
                igmp_check = result['Mediaroom']
                if igmp_check != 'Nenhum':
                    self._dict_result.update({"obs": f'Interface: Mediaroom, IGMP: Habilitado: {igmp_check}', "result":'passed', "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Mediaroom, IGMP: {igmp_check}'})
            except:
                self._dict_result.update({"obs": 'Interface Mediaroom nao existe'})

        return self._dict_result
  

    def vivo1_vlanIdVoip_460(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": f'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'VoIP':
                        if sub_dict.get('VID/Prioridade').split('/')[0] == '30':
                            obs_result = 'Name: VoIP | VID: 30'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result = f'Teste incorreto, retorno Name: VoIP, VID: {sub_dict.get("VLAN")}'
                            break
                    else:
                        obs_result = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"
            
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'VoIP':
                        if sub_dict.get('VID/Prioridade').split('/')[0] == '601':
                            obs_result2 = 'Name: VoIP | VID: 601'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Name: VoIP, VID: {sub_dict.get("VLAN")}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"

            self._dict_result.update({"obs": f"Teste 460_1: {obs_result}, Teste 460_2: {obs_result2}" })
        return self._dict_result


    def vivo2_prioridadeVoip_461(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": f'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'VoIP':
                        if sub_dict.get('VID/Prioridade').split('/')[-1] == '5':
                            obs_result = 'Name: VoIP | Priority: 5'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result = f'Teste incorreto, retorno Name: VoIP | Priority: {sub_dict.get("Priority")}'
                            break
                    else:
                        obs_result = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"

            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == 'VoIP':
                        if sub_dict.get('VID/Prioridade').split('/')[-1] == '601':
                            obs_result2 = 'Name: VoIP | Priority: 601'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Name: VoIP | Priority: {sub_dict.get("Priority")}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno Name: {iface_type}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
        
            self._dict_result.update({"obs": f"Teste 461_1: {obs_result}, Teste 461_2: {obs_result2}" })
        return self._dict_result
    

    def vivo1_validarNatVoip_462(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result1 = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        result2 = session.get_result_from_test(flask_username, 'checkNatSettings_423')

        if len(result1) == 0 and len(result2) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 e 423 primeiro'})

        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                iface_name = 'ipNotFound'
                for _, sub_dict in result1.items():
                    iface_type = sub_dict.get('VID/Prioridade').split('/')[-1]
                    if iface_type == '5':
                        if sub_dict.get('VID/Prioridade').split('/')[0] == '30':
                            iface_name = sub_dict.get('Name')
                            obs_result1 = f"Name: {sub_dict.get('Name')}"
                            break
                        else:
                            obs_result1 = (f'Teste incorreto, retorno Priority: 5 | VLAN: {sub_dict.get("VLAN")}')
                            break
                    else:
                        obs_result1 = (f'Teste incorreto, retorno Priority: {iface_type}')

                for _, sub_dict in result2.items():
                    iface_type = sub_dict.get('Name')
                    if iface_type == iface_name:
                        if sub_dict.get('NAT') == 'Enable':
                            obs_result1 = 'Adm.State: Habilitado'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result1 = f'Teste incorreto, retorno Adm.State: {sub_dict.get("NAT")}'
                            break
                    else:
                        obs_result1 = f'Teste incorreto, retorno {iface_type} diferente de {iface_name}'

            else:
                obs_result1 = f"REDE:{cpe_config['REDE']}"
        
        #2
            if cpe_config['REDE'] == 'VIVO_2':
                iface_name2 = 'ipNotFound'
                for _, sub_dict in result1.items():
                    iface_type2 = sub_dict.get('VID/Prioridade').split('/')[-1]
                    if iface_type2 == '5':
                        if sub_dict.get('VID/Prioridade').split('/')[0] == '601':
                            iface_name2 = sub_dict.get('Name')
                            obs_result2 = f"Name: {iface_name}"
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Priority: 5, VLAN: {sub_dict.get("VID/Prioridade").split("/")[0]}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno Priority: {iface_type2}'
                    
                for _, sub_dict in result2.items():
                    iface_type2 = sub_dict.get('Name')
                    if iface_type2 == iface_name2:
                        if sub_dict.get('NAT') == 'Enable':
                            obs_result2 = 'Adm.State: Enable'
                            self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            obs_result2 = f'Teste incorreto, retorno Adm.State: {sub_dict.get("NAT")}'
                            break
                    else:
                        obs_result2 = f'Teste incorreto, retorno {iface_type2} diferente de {iface_name2}'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
         
            self._dict_result.update({"obs": f"Teste 462_1: {obs_result1}, Teste 462_2: {obs_result2}" })
        return self._dict_result

    
    # def vivo_1_igmpVoip_463(self, flask_username):
    #     #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
    #     result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
    #     result2 = session.get_result_from_test(flask_username, 'checkWanInterface_420')

    #     if len(result) == 0 or len(result2) == 0:
    #         self._dict_result.update({"obs": 'Execute o teste 420 e 424 primeiro'})
    #     else:
    #         cpe_config = config_collection.find_one()
    #         iface_type = result2['index_1'].get('Name')

    #         if cpe_config['REDE'] == 'VIVO_1':
    #             for key, col in result.items():
    #                 if iface_type == 'VoIP':
    #                     if key == 'igmp_quickleave_act':
    #                         if col['type'] == 'Ativado':
    #                             obs_result = 'Interface: VoIP | IGMP Quickleave: Ativado'
    #                             print(obs_result)
    #                             self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
    #                             break
    #                         else:
    #                             obs_result = f'Teste incorreto, retorno Interface: {iface_type} | IGMP Quickleave: {col["type"]}'
    #                             break

    #                 else:
    #                     obs_result =  f'Teste incorreto, retorno Interface: {iface_type}'
    #         else:
    #             obs_result = f"REDE:{cpe_config['REDE']}"
            
    #         if cpe_config['REDE'] == 'VIVO_2':
    #             for key, col in result.items():
    #                 if iface_type == 'VoIP':
    #                     if key == 'igmp_quickleave_act':
    #                         if col['type'] == 'Ativado':
    #                             obs_result2 = 'Interface: VoIP | IGMP Quickleave: Ativado'
    #                             self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
    #                             break
    #                         else:
    #                             obs_result2 =  f'Teste incorreto, retorno Interface: {iface_type} | IGMP Quickleave: {col["type"]}'
    #                             break
    #             else:
    #                 obs_result2 =  f'Teste incorreto, retorno Interface: {iface_type}'
    #         else:
    #             obs_result2 = f"REDE:{cpe_config['REDE']}"
    #         self._dict_result.update({"obs": f"463_1: {obs_result}, 463_2: {obs_result2}"})
    #     return self._dict_result

    def vivo_1_igmpVoip_463(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 424 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkMulticastSettings_424')
        if len(result) == 0: 
            self._dict_result.update({"obs": 'Execute o teste e 424 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                try:
                    igmp_check = result['VoIP']
                    if igmp_check != 'Nenhum':
                        obs_result = f'Interface: VoIP, IGMP: Habilitado: {igmp_check}'
                        self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                    else:
                        obs_result =  f'Teste incorreto, retorno Interface: VoIP, IGMP: {igmp_check}'
                except:
                    obs_result =  'Interface VoIP nao existe'
            else:
                obs_result = f"REDE:{cpe_config['REDE']}"
            
            if cpe_config['REDE'] == 'VIVO_2':
                try:
                    igmp_check = result['VoIP']
                    if igmp_check != 'Nenhum':
                        obs_result2 = f'Interface: VoIP, IGMP: Habilitado: {igmp_check}'
                        self._dict_result.update({"result":'passed', "Resultado_Probe":"OK"})
                    else:
                        obs_result2 = f'Teste incorreto, retorno Interface: VoIP, IGMP: {igmp_check}'
                except:
                    obs_result2 =  'Interface VoIP nao existe'
            else:
                obs_result2 = f"REDE:{cpe_config['REDE']}"
            
            self._dict_result.update({"obs": f"463_1: {obs_result}, 463_2: {obs_result2}"})
        return self._dict_result


    def checkLANDHCPSettings_x_464(self, flask_username):
        dict_saida464 = {}

        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(3)
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
            time.sleep(1)

            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            self._driver.find_element_by_xpath('//*[@id="network-homeNetworking"]/a').click()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="t5"]/span').click()
            time.sleep(2)
            print('1')

            # Pegando os inputs
            columns_1 = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[2]/div/table/tbody/tr[2]//td')
            time.sleep(2)
            columns_2 = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[2]/div/table/tbody/tr[3]//td')
            print('2')
            name_columns = ['#', 'Estado', 'Gateway', 'Máscara de sub-rede', 'Piscina de iniciot', 'Pool End', 
                            'DNS Servidor 1', 'DNS Servidor 2', 'VendorID', 'VendorID Modo', 'VendorID Excluir', 
                            'Option240 Estado', 'Option240 Value', 'Modificar']

            c1 = []
            c2 = []

            for col1 in columns_1:
                c1.append(col1.text)

            for col2 in columns_2:
                c2.append(col2.text)
            print('3')

            list_values = [{k: v for k, v in zip(name_columns, c1)}, {k: v for k, v in zip(name_columns, c2)}]
            i = 0
            for value in list_values:
                dict_saida464[i]= value
                i+= 1
                gateway = value.get('Gateway')
                subnet = value.get('Máscara de sub-rede')
                if gateway == '192.168.15.1':
                    self._dict_result.update({"obs": f"Gateway: {gateway} | Subnet: {subnet}", "result":"passed", "Resultado_Probe": "OK"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Gateway: {gateway} | Subnet: {subnet}" })
            print('dict final',dict_saida464)

        except Exception as ex:
            self._dict_result({"obs": ex})
        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkLANDHCPSettings_x_464', dict_saida464)
            return self._dict_result


    def poolDhcpLan_465(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            start_addr = result[0].get('Piscina de iniciot')
            end_addr = result[0].get('Pool End')
            if start_addr == '192.168.15.1' and end_addr == '192.168.15.200':
                self._dict_result.update({"obs": 'IP Address Range OK', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Piscina de iniciot: {start_addr} | Pool End: {end_addr}'})
        return self._dict_result


    def leaseTime_466(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            lease_time_466 = result['dhcp_LeaseTime']
            if '14400' == lease_time_466:
                self._dict_result.update({"obs": 'Lease Time: 14400', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Lease Time: {lease_time_466}'})      
        return self._dict_result

    
    def vendorIdIptvEnable_467(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            vendorID = result[0].get('VendorID')
            print(vendorID)
            vendorID_check = result[0].get('VendorID Excluir')
            cpe_config = config_collection.find_one()
            
            #1
            if vendorID_check == 'Enabled':
                obs_result1 = f'VendorID esta Habilitado'
                self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
            else:
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                obs_result1 = f"Teste incorreto, retorno VendorID: {vendorID_check}"

            #2
            if cpe_config['REDE'] == 'VIVO_1':
                if vendorID == 'MSFT_IPTV,TEF_IPTV':
                    obs_result2 = f'Valor VendorID: {vendorID}'
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                    obs_result2 = f"Teste incorreto, retorno Valor VendorID: {vendorID}"
            else:
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                obs_result2 = f"REDE:{cpe_config['REDE']}"
            
            #3
            if cpe_config['REDE'] == 'VIVO_2':
                if vendorID == 'GVT-STB,RSTIH89-500_HD,DSTIH78_GVT,VM1110,DSTIH79_GVT,VM1110_HD_HYBRID,DSITH79_GVT_HD':
                    obs_result3 = f'Valor VendorID: {vendorID}'
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                    obs_result3 = f"Teste incorreto, retorno Valor VendorID: {vendorID}"
            else:
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                obs_result3 = f"REDE:{cpe_config['REDE']}"

            self._dict_result.update({"obs": f"467_1: {obs_result1} | 467_2: {obs_result2} | 467_3: {obs_result3}"})
            
        return self._dict_result


    def poolDhcpIptv_468(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            start_addr = result[1].get('Piscina de iniciot')
            end_addr = result[1].get('Pool End')
            if start_addr == '192.168.15.230' and end_addr == '192.168.15.254':
                self._dict_result.update({"obs": 'IP Address Range OK', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Piscina de iniciot: {start_addr} | Pool End: {end_addr}'})
        return self._dict_result


    def igmpSnoopingLAN_469(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            igmp_check = result['igmp_snoop_act']
            if igmp_check == 'Yes':
                self._dict_result.update({"obs": 'IGMP Snoop Act: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno IGMP Snoop Act: {igmp_check}'})
       
        return self._dict_result


    def verificarWifi24SsidDefault_470(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_ssid = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['SSID']
            ssid = re.findall("^VIVOFIBRA-\w{4}", result_ssid)
            if ssid:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'SSID: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'SSID: NOK'})
        return self._dict_result


    def verificarWifi24Habilitado_471(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            rede_pv = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['Rede Wi-Fi Privada']
            if rede_pv == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Rede Wi-Fi Privada: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Rede Wi-Fi Privada: {rede_pv}'})
        return self._dict_result


    def verificarWifi24Padrao_472(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            modo_ope = result['Configurações']['Rede Wifi 2.4Ghz']['Avançado']['Modo de Operação']
            if modo_ope == '802.11g/n':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Operação: 802.11g/n', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retornoModo de Operação: {modo_ope}'})
        return self._dict_result


    def frequencyPlan_473(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        self._driver.switch_to.default_content()
        configuracao_rede = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[2]')
        time.sleep(2)
        ActionChains(self._driver).move_to_element(configuracao_rede).perform()
        self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[1]/li[3]/a').click()
        time.sleep(3)
        self._driver.switch_to.frame('mainFrame')
        time.sleep(3)
        self._driver.find_element_by_xpath('//*[@id="t5"]/span').click()
        time.sleep(3)

        bandwidth = Select(self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[1]/div/ul[7]/li[2]/select')).first_selected_option.text
        print(bandwidth)
        self._driver.find_element_by_xpath('/html/body/ul/li[1]/a/span').click()
        time.sleep(3)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('mainFrame')
        time.sleep(2)
        canais = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[2]/div[2]/ul[7]/li[2]/select')
        canais24G_list = [x.get_attribute('value') for x in canais.find_elements_by_tag_name("option")]
        indice = canais24G_list.index('0')
        canais24G_list[indice] = 'Auto'
        print(canais24G_list)
        
        cpe_config = config_collection.find_one()

        if bandwidth == '20MHz':
            ref_list = cpe_config["REF_CHANNEL_2_4_20MHz"]   
            print('ref', ref_list)           
            if canais24G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

        else:
            ref_list = cpe_config["REF_CHANNEL_2_4_40MHz"]    
            print('ref', ref_list) 
            if canais24G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})
        self._driver.quit()
        return self._dict_result   



    def verificarWifi24AutoChannel_474(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            canal = result['Configurações']['Rede Wifi 2.4Ghz']['Avançado'].get('Canal:')
            if canal == 'Automático':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Canal: Automático', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Canal: {canal}'})
            
        return self._dict_result

    def verificarWifi24LarguraBanda_475(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            larg_banda_canal = result['Configurações']['Rede Wifi 2.4Ghz']['Avançado']['Largura de Banda do Canal']
            if larg_banda_canal == '20 MHz':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Largura de Banda do Canal: 20 MHz', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Largura de Banda do Canal: {larg_banda_canal}'})
            
        return self._dict_result


    def verificarWifi24Seguranca_476(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            seguranca = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['Modo de Segurança']
            if seguranca == 'WPA2':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Segurança: WPA2', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retornoModo de Segurança: {seguranca}'})          
        return self._dict_result


    def verificarWifi24PasswordDefault_477(self, flask_username):   
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(3)
        element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
        hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
        hover.perform()
        print('1')
        self._driver.find_element_by_xpath('//*[@id="network-wireless"]').click()
        time.sleep(3)
        self._driver.switch_to.frame('mainFrame')
        time.sleep(3)
        
        self._driver.find_element_by_xpath('//*[@id="btn_wpa2pskmore"]').click()
        # self._driver.find_element_by_xpath('//*[@id="btn_wpa2pskmore"]').click()
        passphrase_value = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/div[3]/ul/li/div[2]/div[2]/ul/li[2]/input').get_attribute('value')

        cript = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/div[3]/ul/li/div[8]/ul/li[2]/select').text.strip()
        self._driver.quit()
        password = re.findall("^\w{8}", passphrase_value)
        dict_saida477 = {'passphrase': passphrase_value, 'Criptografia': cript }
        if password:
            self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Passprhase: OK', "result":"passed"})
        else:
            self._dict_result.update({"obs": 'Teste incorreto, retorno Passphrase: NOK'})          
        
        print(dict_saida477)
        self.update_global_result_memory(flask_username, 'verificarWifi24PasswordDefault_477', dict_saida477)
        return self._dict_result


    def cipherModeDefault_478(self, flask_username):
        result = session.get_result_from_test(flask_username, 'verificarWifi24PasswordDefault_477')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 477 primeiro'})
        else:
            encryption_value = result['Criptografia']
            if encryption_value == "AES":
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Encryption: AES', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Encryption: {encryption_value}'})          
        
        return self._dict_result


    def verificarWifi24WPS_479(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            wps = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['WPS']
            if wps == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'WPS: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno WPS: {wps}'})          
        return self._dict_result


    def verificarWifi5SsidDefault_480(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_ssid = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas']['SSID']
            ssid = re.findall("^VIVOFIBRA-\w{4}.*-5G$", result_ssid)
            if ssid:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'SSID: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno SSID: NOK'})
            
        return self._dict_result


    def verificarWifi5Habilitado_481(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            rede_pv = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas'].get('Rede Wi-Fi Privada')
            if rede_pv == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Rede Wi-Fi Privada: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Rede Wi-Fi Privada: {rede_pv}'})        
        return self._dict_result


    def verificarWifi5Padrao_482(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            modo_ope = result['Configurações']['Rede Wifi 5Ghz']['Configurações Avançadas'].get('Modo de Operação')
            if modo_ope == '802.11n/ac':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Operação: 802.11n/ac', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Modo de Operação: {modo_ope}'})           
        return self._dict_result


    def frequencyPlan5GHz_483(self, flask_username):

        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(3)
        element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
        hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
        hover.perform()
        time.sleep(3)

        self._driver.find_element_by_xpath('//*[@id="network-wireless5G"]').click()
        time.sleep(2)
        self._driver.switch_to.frame('mainFrame')
        time.sleep(3)

        wps = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[4]/div[2]/ul/li[2]/select//option')
        for v in wps:

            if v.get_attribute('selected'):
                wps_value = v.text

        time.sleep(2)
        cript = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/div/li[4]/div[2]/div/ul[1]/li[2]/select/option[1]')
        for c in cript:
            cript_value = c.text

        time.sleep(3)

        self._driver.find_element_by_xpath('/html/body/ul/li[4]/a/span').click()
        time.sleep(2)
        bandwidth5G_value = self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[1]/div/ul[3]/li[2]').text
        time.sleep(3)

        canal_values = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[1]/div/ul[4]/li[2]/select//option')
        time.sleep(3)

        channel5G_list = []
        for v in canal_values:
            channel5G_list.append(v.get_attribute('value'))


        for x in range(0,len(channel5G_list)):
            if int(channel5G_list[x]) >=52 and int(channel5G_list[x]) <=140:
                channel5G_list[x] = channel5G_list[x]+'(DFS)'


        dict_saida483 = {'advanced': {'chanel5G': channel5G_list, 'band5G': bandwidth5G_value}, 'general': {'encryption': cript_value, 'wps': wps_value}}

        print(dict_saida483)

        cpe_config = config_collection.find_one()

        if bandwidth5G_value == '20':
            ref_list = cpe_config["REF_CHANNEL_5_20MHz"]              
            if channel5G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})
       
        if bandwidth5G_value == '40':
            ref_list = ref_list = cpe_config["REF_CHANNEL_5_40MHz"]      
            if channel5G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})
         
        if bandwidth5G_value == '80':
            ref_list = ref_list = cpe_config["REF_CHANNEL_5_80MHz"]    
            if channel5G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})
        self.update_global_result_memory(flask_username, 'frequencyPlan5GHz_483', dict_saida483)
        
        self._driver.quit()        
        return self._dict_result


    def verificarWifi5AutoChannel_484(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            canal = result['Configurações']['Rede Wifi 5Ghz']['Configurações Avançadas'].get('Canal')
            if canal == 'Automático':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Canal: Automático', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Canal: {canal}'})         
        return self._dict_result


    def verificarWifi5LarguraBanda_485(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            larg_banda_canal = result['Configurações']['Rede Wifi 5Ghz']['Configurações Avançadas'].get('Largura de Banda do Canal')
            if larg_banda_canal == '80 MHz':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Largura de Banda do Canal: 80 MHz', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Largura de Banda do Canal: {larg_banda_canal}'})
            
        return self._dict_result


    def verificarWifi5Seguranca_486(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            seguranca = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas'].get('Modo de Segurança')
            if seguranca == 'WPA2':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Segurança: WPA2', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Modo de Segurança: {seguranca}'})          
        return self._dict_result


    def verificarWifi5PasswordDefault_487(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_senha = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas'].get('Senha')
            senha = re.findall("^\w{8}", result_senha)
            if senha:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Senha: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno Senha: NOK'})          
        return self._dict_result


    def cipherModeDefault5GHz_488(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 483 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'frequencyPlan5GHz_483')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 483 primeiro'})
        else:
            encryption_value = result['general'].get('encryption')
            if encryption_value == "AES":
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Encryption: AES', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Encryption: {encryption_value}'})           
        return self._dict_result


    def verificarWifi5WPS_489(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 483 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'frequencyPlan5GHz_483')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 483 primeiro'})
        else:
            wps = result['general'].get('wps')
            if wps == 'WPA2-PSK':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'WPS: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno WPS: {wps}'})          
        return self._dict_result


    def checkVoIPSettings_490(self, flask_username, interface=1):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)
            
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="voip"]/span[2]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            self._driver.find_element_by_xpath('//*[@id="voip-sip"]/a').click()
    
            time.sleep(5)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
    
            self._driver.find_element_by_xpath('//*[@id="t1"]').click()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="editBtn"]').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            time.sleep(2)
            form_input  = self._driver.find_elements_by_xpath('/html/body/div[3]/div[2]/form/div[1]/div/ul//input')
            
            dict_form = {}
            for input in form_input:
                if input.get_attribute('value'):
                    if (input.get_attribute('type') == 'radio' and not input.get_attribute('checked')):
                        continue
                    else:
                        dict_form.update({input.get_attribute('name'): input.get_attribute('value') 
                                                                    if input.get_attribute('type') == 'radio'
                                                                    else input.get_attribute('checked') 
                                                                    if input.get_attribute('checked') 
                                                                    else input.get_attribute('value')})
            else:
                fax_option = {'FALSE': 'G711', 'TRUE': 'T38'}
                dict_form = {k: (v if k!='FAX_Option' else fax_option[v])  for k,v in dict_form.items()}

            if dict_form['FAX_Option'] == 'T38':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "T38: Habilitado", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno T38: Desabilitado"})
            print(dict_form)
            self._driver.quit()
        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            self.update_global_result_memory(flask_username, 'checkVoIPSettings_490', dict_form)
            return self._dict_result


    def verificarDtmfMethod_491(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            dtm = result['DTMFMode_data']
            if dtm == 'RFC2833':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "DTMF Method: RFC2833", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno DTMF Method: {dtm}"})

        return self._dict_result

    
    def prioridadeCodec_0_493(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            value = result['FAX_Option']
            if value == 'G711':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "G711: Habilitado", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno G711: Desabilitado"})

        return self._dict_result


    def prioridadeCodec_1_494(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            value = result['FAX_Option']
            if value == 'G.729':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "G.729: Habilitado", "result":"passed"})
            else:
                self._dict_result.update({"obs": "Teste incorreto, G.729: Desabilitado "})

        return self._dict_result



    def checkNATALGSettings_495(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(3)
            
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[2]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            self._driver.find_element_by_xpath('//*[@id="network-nat"]/a').click()
             
            time.sleep(3)
            self._driver.switch_to.frame('mainFrame')

            self._driver.find_element_by_xpath('//*[@id="t4"]/span').click()
           
            time.sleep(3)
            
            radio_input  = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[1]/div[2]/ul/li[2]//input')
            
            dict_form = {}
            for input in radio_input:
                if input.get_attribute('value'):
                    if (input.get_attribute('type') == 'radio' and not input.get_attribute('checked')):
                        continue
                    else:
                        dict_form.update({input.get_attribute('name'): input.get_attribute('value') 
                                                                    if input.get_attribute('type') == 'radio'
                                                                    else input.get_attribute('checked') 
                                                                    if input.get_attribute('checked') 
                                                                    else input.get_attribute('value')})
            else:
                alg_option = {'Yes': 'Desabilitado', 'No': 'Habilitado'}
                dict_form = {k: (v if k!='ALG_SIP' else alg_option[v])  for k,v in dict_form.items()}

            if dict_form['ALG_SIP'] == 'Desabilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'LAN Setting ALG SIP: Desabilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno: LAN Setting ALG SIP {dict_form['ALG_SIP']}"})

        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            self._driver.quit()

            self.update_global_result_memory(flask_username, 'checkNATALGSettings_495', dict_form)
            return self._dict_result


    def checkSNMP_496(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(3)

            #Hover na configuracao de rede
            element_to_hover_over = self._driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/div[2]/ul/li[6]/span[1]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            time.sleep(3)

            #Clicou na Lan
            self._driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div/ul[5]/li[10]/a').click()
             
            
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrame')
            time.sleep(3)

            self._driver.find_element_by_xpath('/html/body/ul/li[3]/a/span').click()
           
            time.sleep(2)
            
            snmp_name = [value.text for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li/div/ul/table/tbody/tr[3]//td')]
            snmp = [value.get_attribute('checked') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li/div/ul/table/tbody/tr[3]/td//input')]
        
            snmp_name = snmp_name[1].split()
            snmp = snmp_name[snmp.index('true')]

            if snmp == 'Disable':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "SNMP: Desabilitado", "result":"passed"})
            else:
                self._dict_result.update({"obs": "Teste incorreto, retorno SNMP: Habilitado"})

        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result



    def checkUPnP_497(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(3)

            #Hover na configuracao de rede
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[2]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            time.sleep(3)

            #Clicou na Lan
            self._driver.find_element_by_xpath('//*[@id="network-homeNetworking"]/a').click()
             
            
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrame')
            time.sleep(3)

            self._driver.find_element_by_xpath('//*[@id="t3"]/span').click()
           
            time.sleep(3)
            
            #Capiturando Inputs da tela
            radio_input  = self._driver.find_elements_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[1]/div[2]/ul/li[2]//input')
            
            dict_form = {}
            for input in radio_input:
                if input.get_attribute('value'):
                    if (input.get_attribute('type') == 'radio' and not input.get_attribute('checked')):
                        continue
                    else:
                        dict_form.update({input.get_attribute('name'): input.get_attribute('value') 
                                                                    if input.get_attribute('type') == 'radio'
                                                                    else input.get_attribute('checked') 
                                                                    if input.get_attribute('checked') 
                                                                    else input.get_attribute('value')})
            else:
                alg_option = {'Yes': 'Habilitado', 'No': 'Desabilitado'}
                dict_form = {k: (v if k!='enblUpnp' else alg_option[v])  for k,v in dict_form.items()}

            if dict_form['enblUpnp'] == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'UPnP Setting Adm.State: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno: UPnP Setting Adm.State {dict_form['ALG_SIP']}"})

            self._driver.quit()
        except Exception as exception:
            self._dict_result.update({"obs": exception})
        finally:
            self.update_global_result_memory(flask_username, 'checkUPnP_497', dict_form)
        return self._dict_result



    def linkLocalType_498(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            linkLocal = result['Status']['Internet']['IPv6'].get('Endereço de IPv6 Link-Local - LAN:')
            print(linkLocal)
            try:
                if linkLocal.split('/')[1] == '64':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "link local: 64", "result":"passed"})
            except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno link local: {linkLocal}"})

        return self._dict_result


    def lanGlobalType_499(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            linkGlobal = result['Status']['Internet']['IPv6'].get('Endereço de IPv6 Global - WAN:')
            try:
                if linkGlobal.split('/')[1] == '64':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "WAN global identifier: 64", "result":"passed"})
            except:
                self._dict_result.update({"obs": f"Teste incorreto, retorno WAN global identifier: {linkGlobal}"})
        return self._dict_result


    def prefixDelegationfromInet_500(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            delegate = result['LanDelegateStaticFlag_H']
            if delegate == 'PVC0':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefixo Delegado da WAN: PVC0", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Prefixo Delegado da WAN: {delegate}"})
            
        return self._dict_result


    