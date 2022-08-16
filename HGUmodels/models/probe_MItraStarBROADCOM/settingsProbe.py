#from asyncio import exceptions
from cgi import print_form
from datetime import datetime
from os import name
import re
import time
from typing import List
# from jinja2 import pass_context
#from typing import final
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException
import socket

# import pyperclip

from json import JSONEncoder
import requests


from ..MItraStarBROADCOM import HGU_MItraStarBROADCOM
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.select import Select
from HGUmodels.config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton

from HGUmodels.main_session import MainSession

session = MainSession()


mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()

dict_test_result_memory = {}

class HGU_MItraStarBROADCOM_settingsProbe(HGU_MItraStarBROADCOM):


    def accessWizard_401(self, flask_username):
        try:
            dict_saida = {}
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            self.admin_authentication_mitraStat()
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="username"]')
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
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            self._driver.switch_to.frame('basefrm')
            element = self._driver.find_element_by_xpath('/html/body/blockquote/form/b/table/tbody/tr[1]/td[2]')

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
        
        try:
            dict_saida = {}
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            # Management
            self._driver.find_element_by_xpath('//*[@id="folder70"]/table/tbody/tr/td/a/span').click()
            time.sleep(3)          
            # Access Control
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[81]/table/tbody/tr/td/a/span').click()
            time.sleep(2)
            # Remote Management
            self._driver.find_element_by_xpath('//*[@id="item82"]/table/tbody/tr/td/a').click()
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            table_trust_domain = [value.text for value in self._driver.find_elements_by_xpath('/html/body/form/div/div[2]/ul/div[1]/table/tbody/tr//td') if value.text != '']
            inputs_checkbox = [value.get_attribute('checked') for value in self._driver.find_elements_by_xpath('/html/body/form/div/div[2]/ul/div[1]/table/tbody/tr//input') if value.get_attribute('type') == 'checkbox']
            inputs_ports = [value.get_attribute('value') for value in self._driver.find_elements_by_xpath('/html/body/form/div/div[2]/ul/div[1]/table/tbody/tr/td//input') if value.get_attribute('name')[-4:] == 'Port']
            inputs_checkbox = ['Enable' if i == 'true' else 'Disable' for i in inputs_checkbox]
            ip_address = self._driver.find_element_by_xpath('/html/body/form/div/div[2]/ul/table/tbody/tr[3]/td[3]/input').text
            dict_saida = {
                table_trust_domain[5]: 
                    {table_trust_domain[1]: inputs_checkbox[0], table_trust_domain[2]: inputs_checkbox[1], table_trust_domain[3]: inputs_checkbox[2], table_trust_domain[4]: inputs_ports[0] },
                table_trust_domain[9]: {
                    table_trust_domain[1]: inputs_checkbox[3], table_trust_domain[2]: inputs_checkbox[4], table_trust_domain[3]: inputs_checkbox[5], table_trust_domain[4]: inputs_ports[1] },
                table_trust_domain[13]: 
                    {table_trust_domain[1]: inputs_checkbox[6], table_trust_domain[2]: inputs_checkbox[7], table_trust_domain[3]: inputs_checkbox[8], table_trust_domain[4]: inputs_ports[2] },
                table_trust_domain[17]: 
                    {table_trust_domain[1]: inputs_checkbox[9], table_trust_domain[2]: inputs_checkbox[10], table_trust_domain[3]: inputs_checkbox[11], table_trust_domain[4]: table_trust_domain[21] },
                'IP Address': ip_address
            }
            print(dict_saida)

            http_wan = dict_saida['HTTP']['WAN']
            if http_wan == 'Disable':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', "obs":" Access Remote HTTP: WAN Desabilitado"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, Access Remote HTTP: WAN Habilitado"})
                    
            self._driver.quit()
        except Exception as exception:
            print(exception)
            self._dict_result.update({'obs':str(exception)})
            
        finally:
            self.update_global_result_memory(flask_username, 'accessRemoteHttp_405', dict_saida)
            return self._dict_result


    def accessRemoteSSH_407(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessRemoteHttp_405')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 405 primeiro"})
        else:
            ssh_wan = result['SSH']['WAN']
            if ssh_wan == 'Disable':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', "obs": "Access Remote SSH: WAN Desabilitado"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, Access Remote SSH: WAN Habilitado"})
            
        return self._dict_result


    def accessRemoteTrustedIP_408(self, flask_username):
        result = session.get_result_from_test(flask_username, 'accessRemoteHttp_405')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 405 primeiro"})
        else:
            if result['IP Address'] == '':
                self._dict_result.update({"Resultado_Probe": "OK", 'result':'passed', "obs": f"Trusted IP: {result['IP Address']}"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, Trusted IP: {result['IP Address']}"})
            
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
                            time_zone = time_zone.split(',')[0].strip()
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
            dict_saida = {}
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder70"]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="folder78"]/table/tbody/tr/td/a/span').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            dict_saida = {}

            acs_names = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[2]/tbody//td') if value.text != '']
            acs_values = [value.get_attribute('value') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td//input')]

            names_inform = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr//td')]
            inform = [value.get_attribute('checked') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr/td//input')]
            
            names_soap = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[4]/tbody/tr//td')]
            soap = [value.get_attribute('checked') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[4]/tbody/tr/td//input')]

            con_names = [value.text.replace(":", "") for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/div/table/tbody/tr//td') if value.text != '']
            con_values = [value.get_attribute('value') for value in self._driver.find_elements_by_xpath('//html/body/blockquote/form/div/table/tbody/tr/td//input')]
            
            for a, b in zip(acs_names, acs_values):
                dict_saida[a.replace(":", "")] = b
            
            dict_saida.update({"Inform": names_inform[inform.index('true')+1], 
                                "SOAP": names_soap[soap.index('true')+1], 
                                con_names[0]: con_values[0],
                                con_names[1]: con_values[1],
                                con_names[2]: con_names[3]})

            print(dict_saida)
            
            acs_url = dict_saida['ACS URL']
            if  acs_url == 'http://acs.telesp.net.br:7005/cwmpWeb/WGCPEMgt':
                self._dict_result.update({"obs": acs_url, "Resultado_Probe": "OK", 'result':'passed'})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno ACS URL: {acs_url}"})

        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkACSSettings_411', dict_saida)

            return self._dict_result


    def validarDefaultUserACS_412(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        
        else:
            value = result['ACS User Name']
            if value == 'acsclient':
                self._dict_result.update({"obs": "Usuario: acsclient", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Usuario: {value}"})
        return self._dict_result

    # resolver o ** da senha
    def validarDefaultPasswordACS_413(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['ACS Password']
            if value == 'telefonica':
                self._dict_result.update({"obs": "Senha: telefonica", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Senha: {value}"})
        return self._dict_result


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
                    self._dict_result.update({'result':'failed',"obs":"nbiRH.msgTagExecution_02 != EXECUTED"})
                    return self._dict_result   
        except Exception as exception:
            self._dict_result.update({'result':'failed',"obs":str(exception)})
            return self._dict_result




    def periodicInformEnable_415(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['Inform']
            if value == 'Enable':
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
            value = result['Inform Interval']
            if value == '68400':
                self._dict_result.update({"obs": "Informe Interval: 68400", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Informe Interval: {value}"})
        return self._dict_result


    def connectionRequestPort_417(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword):
        self._dict_result.update({'result':'failed',"obs": TEST_NOT_IMPLEMENTED_WARNING})
        return self._dict_result


    def enableCwmp_418(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['SOAP']
            if value == 'Enable':
                self._dict_result.update({"obs": "SOAP: Habilitado", "result":'passed', "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno SOAP: {value}"})
        return self._dict_result


    def userConnectionRequest_419(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 411 seja executado em conjunto
        #TODO: Verificar se o teste 419 é igual ao teste 412
        result = session.get_result_from_test(flask_username, 'checkACSSettings_411')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 411 primeiro"})
        else:
            value = result['Connection Request User Name']
            if value == 'userid':
                self._dict_result.update({"obs": "Connection Request Username OK", "result":'passed'})
            else:
                self._dict_result.update({"obs": f"Connection Request Username incorreta, retorno: {value}", "result":'failed'})
        return self._dict_result



    def checkWanInterface_420(self, flask_username):
        
        try:
            dict_saida420 = {}
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder1"]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="folder3"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
       
            keys = []
            dict_saida420 = {}
            for m, row in enumerate(self._driver.find_elements_by_xpath('/html/body/blockquote/form/center/table/tbody/tr')):
                for n, cell in enumerate(row.find_elements_by_tag_name('td')):
                    if m == 0: keys.append(cell.text)
                    else: 
                        if n == 0: 
                            interface = cell.text
                            dict_saida420[cell.text] = {}
                        else:
                            dict_saida420[interface][keys[n]] = cell.text
            ### Adicionando as Vlan Priorities:
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="item14"]/table/tbody/tr/td/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            vlan_p = self._driver.find_element_by_xpath('/html/body/blockquote/form/center/table/tbody/tr[1]/td[6]').text
            
            for m, row in enumerate(self._driver.find_elements_by_xpath('/html/body/blockquote/form/center/table/tbody//tr')):
                for n, cell in enumerate(row.find_elements_by_tag_name('td')):
                    if cell.text in dict_saida420:
                        dict_saida420[cell.text][vlan_p] = row.text.split(' ')[4]
            self._driver.quit()
            ###
            print(dict_saida420)
            
            cpe_config = config_collection.find_one()
            for k, item in dict_saida420.items():
                if True: # cpe_config['REDE'] == 'VIVO_1':
                    if item['Type'] == 'PPPoE':
                        if item['VlanMuxId'] == '10': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "Encapsulamento: PPPoE | VlanId: 10", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: Encapsulamento:{item['Type']}, VlanId:{item['VlanMuxId']}"})
                            break
                elif cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                    if item['Type'] == 'PPPoE':
                        if item['VlanMuxId'] == '600': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "Encapsulamento: PPPoE | VlanId: 600", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: Encapsulamento:{item['Type']}, VlanId:{item['VlanMuxId']}"})
                            break
                else:
                    self._dict_result.update({"obs": f"REDE: {cpe_config['REDE']}, ACCESS: {cpe_config['ACCESS']}, TYPE: {cpe_config['TYPE']}"})

        except Exception as exception:
            print(exception)
            self._dict_result.update({"obs": exception})
        finally:
            self.update_global_result_memory(flask_username, 'checkWanInterface_420', dict_saida420)
            return self._dict_result


    def prioridadePPPoE_421(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Type')
                    if iface_type == 'PPPoE': 
                        if sub_dict['Vlan8021p'] == '0':
                            self._dict_result.update({"obs": 'Encapsulamento: PPPoE, Prioridade: 0', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Prioridade: {sub_dict['Vlan8021p']}"})
                            break
                else:
                    self._dict_result.update({"obs": "Interface nao disponivel"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: {iface_type}, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def tipoRedeInet_422(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                for _, sub_dict in result.items():
                    iface_id = sub_dict.get('VlanMuxId')
                    if iface_id == '10': 
                        if sub_dict['Type'] == 'PPPoE':
                            self._dict_result.update({"obs": 'VlanId: 10, tipo: PPPoE', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Tipo: {sub_dict['Type']}"})
                            break
                else:
                    self._dict_result.update({"obs": "Interface nao disponivel"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def checkNatSettings_423(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        self._driver.quit()
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                try:
                    nat = result['ppp0.1']['NAT']
                    if nat == 'Enabled':
                        self._dict_result.update({"obs": 'Interface PPPoE: NAT Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface PPPoE: NAT Desabilitado"})
                except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Interface não disponível"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def checkMulticastSettings_424(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        self._driver.quit()
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['ACCESS'] == 'FIBER' and cpe_config['TYPE'] == 'FIBER':
                try:
                    igmp = result['ppp0.1']['Igmp Src Enbl']
                    if igmp == 'Disabled':
                        self._dict_result.update({"obs": 'Interface PPPoE: Igmp Desabilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface PPPoE: Igmp Habilitado"})
                except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Interface não disponível"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def getFullConfig_425(self, flask_username):
        try:
            dict_saida425 = {}
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            self.admin_authentication_mitraStat()
            time.sleep(2)
        
            print('\n#############################################'
                    '\n MENU >> STATUS'
                    '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         STATUS
            ### ------------------------------------------ ###
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[1]/a').click()
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
            detalhes_internet = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[3]/td[2]/a')
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
            wifi_24_detalhes = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[5]/td[2]/a')
            wifi_24_detalhes.click()
            wifi_24_detalhes_info = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[6]/td[1]/div')
            items_key = wifi_24_detalhes_info.find_elements_by_tag_name("li")
            wifi_24_valor = []
            for item in items_key:
                teste = item.text
                wifi_24_valor.append(teste)
            print(wifi_24_valor)
            wifi_24_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[6]/td[2]/textarea').get_attribute('value').strip('\n')
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
            wifi_5_detalhes_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[8]/td[2]/textarea').get_attribute('value').strip('\n')
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
            tv_stations = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[14]/td[2]/textarea').get_attribute('value')
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
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            config_internet = self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a')
            config_internet.click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            config_internet = self._driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/form/table/thead/tr/th').text
            print(config_internet)
            config_internet_usuario = self._driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/form/table/tbody/tr[2]/td[1]').text.strip(': ')
            print(config_internet_usuario)
            config_internet_usuario_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/form/table/tbody/tr[2]/td[2]/input').get_property('value')
            print(config_internet_usuario_valor)
            config_internet_senha = self._driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/form/table/tbody/tr[3]/td[1]').text.strip(': ')
            print('############################## 1')
            print(config_internet_senha)
            config_internet_senha_valor = self._driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/form/table/tbody/tr[3]/td[2]/input').get_attribute('text')
            print('############################## 2')
            print(config_internet_senha_valor)
            time.sleep(1)
            print('\n#############################################'
                    '\n MENU >> CONFIGURAÇÕES >> REDE LOCAL'
                    '\n#############################################\n')
            ### ------------------------------------------ ###
            ###         CONFIGURAÇÕES > REDE LOCAL
            ### ------------------------------------------ ###
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            config_redelocal = self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[2]/a')
            config_redelocal.click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            config_redelocal_dhcp = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/thead/tr/th').text
            print(config_redelocal_dhcp)
            config_redelocal_servidordhcp = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[2]/td[1]').text.strip(': ')
            print(config_redelocal_servidordhcp)
            config_redelocal_servidordhcp_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
            if config_redelocal_servidordhcp_valor == 'true':
                config_redelocal_servidordhcp_valor = 'Habilitado'
            else:
                config_redelocal_servidordhcp_valor = 'Desabilitado'
            print(config_redelocal_servidordhcp_valor)
            config_redelocal_iphgu = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[1]').text.strip(': ')
            print(config_redelocal_iphgu)
            config_redelocal_iphgu_valor01 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[1]').get_property('value')
            config_redelocal_iphgu_valor02 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[2]').get_property('value')
            config_redelocal_iphgu_valor03 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[3]').get_property('value')
            config_redelocal_iphgu_valor04 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[3]/td[2]/input[4]').get_property('value')
            config_redelocal_iphgu_valor = config_redelocal_iphgu_valor01 + '.' + config_redelocal_iphgu_valor02 + '.' + config_redelocal_iphgu_valor03 + '.' + config_redelocal_iphgu_valor04
            print(config_redelocal_iphgu_valor)

            config_redelocal_mask = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[1]').text.strip(': ')
            print(config_redelocal_mask)
            config_redelocal_mask_valor01 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[2]/input[1]').get_property('value')
            config_redelocal_mask_valor02 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[2]/input[2]').get_property('value')
            config_redelocal_mask_valor03 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[2]/input[3]').get_property('value')
            config_redelocal_mask_valor04 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[4]/td[2]/input[4]').get_property('value')
            config_redelocal_mask_valor = config_redelocal_mask_valor01 + '.' + config_redelocal_mask_valor02 + '.' + config_redelocal_mask_valor03 + '.' + config_redelocal_mask_valor04
            print(config_redelocal_mask_valor)

            config_redelocal_pool = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[1]').text.strip(': ')
            print(config_redelocal_pool)
            config_redelocal_pool_valor_ini01 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[1]').get_property('value')
            config_redelocal_pool_valor_ini02 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[2]').get_property('value')
            config_redelocal_pool_valor_ini03 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[3]').get_property('value')
            config_redelocal_pool_valor_ini04 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[5]/td[2]/input[4]').get_property('value')
            config_redelocal_pool_ini_valor = config_redelocal_pool_valor_ini01 + '.' + config_redelocal_pool_valor_ini02 + '.' + config_redelocal_pool_valor_ini03 + '.' + config_redelocal_pool_valor_ini04
            config_redelocal_pool_valor_fin01 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[1]').get_property('value')
            config_redelocal_pool_valor_fin02 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[2]').get_property('value')
            config_redelocal_pool_valor_fin03 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[3]').get_property('value')
            config_redelocal_pool_valor_fin04 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[6]/td/input[4]').get_property('value')
            config_redelocal_pool_fin_valor = config_redelocal_pool_valor_fin01 + '.' + config_redelocal_pool_valor_fin02 + '.' + config_redelocal_pool_valor_fin03 + '.' + config_redelocal_pool_valor_fin04
            print(config_redelocal_pool_ini_valor)
            print(config_redelocal_pool_fin_valor)

            config_redelocal_dns = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[7]/td[1]').text.strip(': ')
            print(config_redelocal_dns)
            config_redelocal_dns_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[7]/td[2]/input[1]').get_attribute('checked')
            if config_redelocal_dns_valor == 'true':
                config_redelocal_dns_valor = 'Habilitado'
            else:
                config_redelocal_dns_valor = 'Desabilitado'
            print(config_redelocal_dns_valor)

            config_redelocal_concessao = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[10]/td[1]').text.strip(': ')
            print(config_redelocal_concessao)
            config_redelocal_concessao_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[1]/tbody/tr[10]/td[2]/input').get_property('value')
            print(config_redelocal_concessao_valor)

            config_redelocal_tabela_concessao = self._driver.find_elements_by_xpath('/html/body/div/div/div[1]/div[3]/form/table[4]')
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
            config_wifi24 = self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[3]/a')
            print(config_wifi24.text)
            config_wifi24.click()
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(5)
            config_wifi24 = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/h3').text.strip(': ')
            config_wifi24_basico = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/thead/tr/th').text.strip(': ')
            print(config_wifi24_basico)
            config_wifi24_basico_redeprivada = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[1]/td[1]').text.strip(': ')
            print(config_wifi24_basico_redeprivada)
            config_wifi24_basico_redeprivada_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]/input[1]').get_attribute('checked')
            if config_wifi24_basico_redeprivada_valor == 'true':
                config_wifi24_basico_redeprivada_valor = 'Habilitado' 
            else:
                config_wifi24_basico_redeprivada_valor = 'Desabilitado'
            print(config_wifi24_basico_redeprivada_valor)
            
            config_wifi24_basico_anuncio = self._driver.find_element_by_xpath('//html/body/div/div/div[1]/div[3]/form/table/tbody/tr[2]/td[1]').text.strip(': ')
            print(config_wifi24_basico_anuncio)
            config_wifi24_basico_anuncio_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
            if config_wifi24_basico_anuncio_valor == 'true':
                config_wifi24_basico_anuncio_valor = 'Habilitado'
            else:
                config_wifi24_basico_anuncio_valor = 'Desabilitado'
            print(config_wifi24_basico_anuncio_valor)

            config_wifi24_basico_ssid = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[3]/td[1]').text.strip(': ')
            print(config_wifi24_basico_ssid)
            config_wifi24_basico_ssid_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[3]/td[2]/input').get_property('value')
            print(config_wifi24_basico_ssid_valor)

            config_wifi24_basico_ssid_senha = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[4]/td[1]').text.strip(': ')
            print(config_wifi24_basico_ssid_senha)
            config_wifi24_basico_ssid_senha_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[4]/td[2]/input').get_property('value')
            print(config_wifi24_basico_ssid_senha_valor)
            config_wifi24_basico_seguranca = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[5]/td[1]').text.strip(': ')
            print(config_wifi24_basico_seguranca)
            config_wifi24_basico_seguranca_valor = Select(self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[5]/td[2]/select')).first_selected_option.text
            print(config_wifi24_basico_seguranca_valor)

            config_wifi24_basico_wps = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[6]/td[1]').text.strip(': ')
            print(config_wifi24_basico_wps)
            config_wifi24_basico_wps_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[6]/td[2]/input[1]').get_attribute('checked')
            if config_wifi24_basico_wps_valor == 'true':
                config_wifi24_basico_wps_valor = 'Habilitado'
            else:
                config_wifi24_basico_wps_valor = 'Desabilitado'
            print(config_wifi24_basico_wps_valor)

            config_wifi24_avancado = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/ul/li[2]/a')
            config_wifi24_avancado.click()
            time.sleep(1)
            config_wifi24_avancado = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/thead/tr/th').text
            print(config_wifi24_avancado)

            config_wifi24_avancado_modooperacao = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[1]/td[1]').text.strip(': ')
            print(config_wifi24_avancado_modooperacao)
            config_wifi24_avancado_modooperacao_valor = Select(self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[1]/td[2]/select')).first_selected_option.text
            print(config_wifi24_avancado_modooperacao_valor)

            config_wifi24_avancado_canal = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[2]/td[1]').text
            print(config_wifi24_avancado_canal)
            config_wifi24_avancado_canal_valor = Select(self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[2]/td[2]/select')).first_selected_option.text
            print(config_wifi24_avancado_canal_valor)

            config_wifi24_avancado_largurabanda = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[3]/td[1]').text.strip(': ')
            print(config_wifi24_avancado_largurabanda)
            config_wifi24_avancado_largurabanda_valor = Select(self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[3]/td[2]/select')).first_selected_option.text
            print(config_wifi24_avancado_largurabanda_valor)

            config_wifi24_avancado_wmm = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[4]/td[1]').text.strip(': ')
            print(config_wifi24_avancado_wmm)
            config_wifi24_avancado_wmm_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[4]/td[2]/input[1]').get_attribute('checked')
            if config_wifi24_avancado_wmm_valor == 'true' :
                config_wifi24_avancado_wmm_valor = 'Habilitado' 
            else:
                config_wifi24_avancado_wmm_valor = 'Desabilitado'
            print(config_wifi24_avancado_wmm_valor)


            config_wifi24_avancado_mac = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[5]/td[1]').text
            print(config_wifi24_avancado_mac)
            config_wifi24_avancado_mac_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table[1]/tbody/tr[5]/td[2]').text
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
            config_wifi5 = self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[4]/a')
            print(config_wifi5.text)
            config_wifi5.click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            config_wifi5_basico = self._driver.find_element_by_xpath('//*[@id="tab-01"]/form/table/thead/tr/th').text
            print(config_wifi5_basico)
            config_wifi5_basico_redeprivada = self._driver.find_element_by_xpath('//*[@id="tab-01"]/form/table/tbody/tr[1]/td[1]').text.strip(': ')
            print(config_wifi5_basico_redeprivada)
            config_wifi5_basico_redeprivada_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table/tbody/tr[1]/td[2]/input[1]').get_attribute('checked')
            if config_wifi5_basico_redeprivada_valor == 'true':
                config_wifi5_basico_redeprivada_valor = 'Habilitado'
            else:
                config_wifi5_basico_redeprivada_valor = 'Desabilitado'
            print(config_wifi5_basico_redeprivada_valor)

            config_wifi5_basico_anuncio = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table/tbody/tr[2]/td[1]').text.strip(': ')
            print(config_wifi5_basico_anuncio)
            config_wifi5_basico_anuncio_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table/tbody/tr[2]/td[2]/input[1]').get_attribute('checked')
            if config_wifi5_basico_anuncio_valor == 'true':
                config_wifi5_basico_anuncio_valor = 'Habilitado'
            else:
                config_wifi5_basico_anuncio_valor = 'Desabilitado'
            print(config_wifi5_basico_anuncio_valor)

            config_wifi5_basico_ssid = self._driver.find_element_by_xpath('//*[@id="tab-01"]/form/table/tbody/tr[3]/td[1]').text.strip(': ')
            print(config_wifi5_basico_ssid)
            config_wifi5_basico_ssid_valor = self._driver.find_element_by_xpath('/html/body/div/div/div[1]/div[4]/form/table/tbody/tr[3]/td[2]/input').get_property('value')
            print(config_wifi5_basico_ssid_valor)

            config_wifi5_basico_ssid_senha = self._driver.find_element_by_xpath('//*[@id="tr_password"]/td[1]').text.strip(': ')
            print(config_wifi5_basico_ssid_senha)
            config_wifi5_basico_ssid_senha_valor = self._driver.find_element_by_xpath('//*[@id="password"]').get_property('value')
            print(config_wifi5_basico_ssid_senha_valor)
            config_wifi5_basico_seguranca = self._driver.find_element_by_xpath('//*[@id="tab-01"]/form/table/tbody/tr[5]/td[1]').text.strip(': ')
            print(config_wifi5_basico_seguranca)
            config_wifi5_basico_seguranca_valor = Select(self._driver.find_element_by_xpath('//*[@id="tab-01"]/form/table/tbody/tr[5]/td[2]/select')).first_selected_option.text
            print(config_wifi5_basico_seguranca_valor)

            config_wifi5_basico_wps = self._driver.find_element_by_xpath('//*[@id="tr_wps"]/td[1]').text
            print(config_wifi5_basico_wps)
            config_wifi5_basico_wps_valor = self._driver.find_element_by_xpath('//*[@id="wlWscMode"]').get_attribute('checked')
            if config_wifi5_basico_wps_valor == 'true':
                config_wifi5_basico_wps_valor = 'Habilitado'
            else:
                config_wifi5_basico_wps_valor = 'Desabilitado'
            print(config_wifi5_basico_wps_valor)

            config_wifi5_avancado = self._driver.find_element_by_xpath('//*[@id="tabtitle-02"]')
            config_wifi5_avancado.click()
            time.sleep(1)
            config_wifi5_avancado = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/thead/tr/th').text
            print(config_wifi5_avancado)

            config_wifi5_avancado_modooperacao = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/tbody/tr[1]/td[1]').text.strip(': ')
            print(config_wifi5_avancado_modooperacao)
            config_wifi5_avancado_modooperacao_valor = Select(self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/tbody/tr[1]/td[2]/select')).first_selected_option.text
            print(config_wifi5_avancado_modooperacao_valor)

            config_wifi5_avancado_canal = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/tbody/tr[2]/td[1]').text.strip(': ')
            print(config_wifi5_avancado_canal)
            config_wifi5_avancado_canal_valor = Select(self._driver.find_element_by_xpath('//*[@id="wlChannel"]')).first_selected_option.text
            print(config_wifi5_avancado_canal_valor)

            config_wifi5_avancado_largurabanda = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/tbody/tr[3]/td[1]').text.strip(': ')
            print(config_wifi5_avancado_largurabanda)
            config_wifi5_avancado_largurabanda_valor = Select(self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/tbody/tr[3]/td[2]/select')).first_selected_option.text
            print(config_wifi5_avancado_largurabanda_valor)

            config_wifi5_avancado_wmm = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/tbody/tr[4]/td[1]').text.strip(": ")
            print(config_wifi5_avancado_wmm)
            config_wifi5_avancado_wmm_valor = self._driver.find_element_by_xpath('//*[@id="wlDisableWme_wl0v0"]').get_attribute('checked')
            if config_wifi5_avancado_wmm_valor == 'true' :
                config_wifi5_avancado_wmm_valor = 'Habilitado' 
            else:
                config_wifi5_avancado_wmm_valor = 'Desabilitado'
            print(config_wifi5_avancado_wmm_valor)

            config_wifi5_avancado_mac = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/tbody/tr[5]/td[1]').text.strip(': ')
            print(config_wifi5_avancado_mac)
            config_wifi5_avancado_mac_valor = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table[1]/tbody/tr[5]/td[2]').text
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
            config_firewall = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[6]/a')
            config_firewall.click()
            config_firewall = config_firewall.text
            print(config_firewall)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            
            time.sleep(2)
            config_firewall_politicapadrao = self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/table[1]/thead[1]/tr/th').text
            print(config_firewall_politicapadrao)
            config_firewall_politicapadrao_status = self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/table[1]/tbody[1]/tr/td[1]').text.strip(': ')
            print(config_firewall_politicapadrao_status)
            config_firewall_politicapadrao_valor = self._driver.find_element_by_xpath('//*[@id="dAction"]').get_attribute('checked')
            if config_firewall_politicapadrao_valor == 'true':
                config_firewall_politicapadrao_valor = 'Aceita'
            else:
                config_firewall_politicapadrao_valor = 'Rejeita'
            print(config_firewall_politicapadrao_valor)

            config_firewall_pingwan = self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/table[1]/thead[2]/tr/th').text.strip(': ')
            print(config_firewall_pingwan)
            config_firewall_pingwan_status = self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/table[1]/tbody[2]/tr/td[1]').text.strip(': ')
            print(config_firewall_pingwan_status)
            config_firewall_pingwan_valor = self._driver.find_element_by_xpath('//*[@id="icmpStatus"]').get_attribute('checked')
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
            config_modowan = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[7]/a')
            config_modowan.click()
            config_modowan = config_modowan.text
            print(config_modowan)
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            config_modowan_bridge = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table/thead/tr/th').text
            print(config_modowan_bridge)

            config_modowan_bridge_modo = self._driver.find_element_by_xpath('//*[@id="tab-02"]/form/table/tbody/tr[1]/td[1]').text.strip(': ')
            print(config_modowan_bridge_modo)
            config_modowan_bridge_modo_valor = Select(self._driver.find_element_by_xpath('//*[@id="op_mode"]')).first_selected_option.text
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
            gerenciamento = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a')
            gerenciamento.click()
            gerenciamento = gerenciamento.text
            print(gerenciamento)
            time.sleep(2)
            gerenciamento_idioma = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[1]/a')
            gerenciamento_idioma.click()
            gerenciamento_idioma = gerenciamento_idioma.text
            print(gerenciamento_idioma)
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            gerenciamento_idioma = self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/table/thead/tr/th').text
            print(gerenciamento_idioma)
            gerenciamento_idioma_valor = self._driver.find_element_by_xpath('//*[@id="currentLanguagePor"]').get_attribute('checked')
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
            sobre = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[4]/a')
            print(sobre.text)
            sobre.click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            sobre = self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/h3').text
            info_dispositivo = self._driver.find_element_by_xpath('//*[@id="table_model"]/thead/tr/th').text
            print(info_dispositivo)

            info_dispositivo_fabricante = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[1]/td[1]/strong').text.strip(': ')
            print(info_dispositivo_fabricante)
            info_dispositivo_fabricante_valor = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[1]/td[2]').text
            print(info_dispositivo_fabricante_valor)

            info_dispositivo_modelo = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[1]/td[3]/strong').text.strip(': ')
            print(info_dispositivo_modelo)
            iinfo_dispositivo_modelo_valor = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[1]/td[4]').text
            print(iinfo_dispositivo_modelo_valor)

            info_dispositivo_firmware = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[2]/td[1]/strong').text
            print(info_dispositivo_firmware)
            info_dispositivo_firmware_valor = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[2]/td[2]').text
            print(info_dispositivo_firmware_valor)

            info_dispositivo_hardware = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[2]/td[3]/strong').text
            print(info_dispositivo_hardware)
            info_dispositivo_hardware_valor = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[2]/td[4]').text
            print(info_dispositivo_hardware_valor)

            info_dispositivo_serial = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[3]/td[1]/strong').text
            print(info_dispositivo_serial)
            info_dispositivo_serial_valor = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[3]/td[2]').text
            print(info_dispositivo_serial_valor)

            info_dispositivo_serialgpon = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[3]/td[3]/strong').text.strip(': ')
            print(info_dispositivo_serialgpon)
            info_dispositivo_serialgpon_valor = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[3]/td[4]').text
            print(info_dispositivo_serialgpon_valor)

            info_dispositivo_macwan = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[4]/td[1]/strong').text
            print(info_dispositivo_macwan)
            info_dispositivo_macwan_valor = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[4]/td[2]').text
            print(info_dispositivo_macwan_valor)

            info_dispositivo_maclan = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[4]/td[3]/strong').text.strip(': ')
            print(info_dispositivo_maclan)
            info_dispositivo_maclan_valor = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[4]/td[4]').text
            print(info_dispositivo_maclan_valor)

            print('\n\n\n == Criando JSON de saída... == ')
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
        except Exception as e:
            self._dict_result.update({"obs": f"Teste incorreto, {str(e)}"})
        finally:
            self.update_global_result_memory(flask_username, 'getFullConfig_425', dict_saida425)
            return self._dict_result



    def verificarSenhaPppDefaultFibra_426(self, flask_username):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self._address_ip, username='support', password='ffdfad94', timeout=2)
            print(self._address_ip)
            shell = ssh.invoke_shell()
            shell.send('tr69cli show\n')
            time.sleep(2)
            clientshow = shell.recv(65000).decode('utf-8')
            password = clientshow[clientshow.index('Password :')+10:clientshow.index('PeriodicInformEnable')].strip()

            if password == 'cliente':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Senha: cliente", "result":"passed"})
            else:
                self._dict_result.update({'result':'failed',"obs": f"Teste incorreto, retorno senha: {password}"})
        
        except (Exception, SSHException) as e:
            self._dict_result.update({"obs": e})

        return self._dict_result


    def checkWanInterface_x_427(self, flask_username, interface):
    
        try:
            dict_saida427 = {}
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="item14"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            self._driver.find_element_by_xpath('/html/body/blockquote/form/center/table/tbody/tr[4]/td[16]/input').click()
            time.sleep(2)
            wan_network = self._driver.find_element_by_xpath('//*[@id="enblv6Info"]/table/tbody/tr/td[1]').text
            wan_interface = Select(self._driver.find_element_by_xpath('//*[@id="IpProtocalMode"]')).first_selected_option.text
            
            dict_saida427 = {wan_network: wan_interface}
            print(dict_saida427)
            if wan_interface == 'IPv4&IPv6(Dual Stack)':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Dual Stack", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno: {wan_interface}"})

        except Exception as e:
            self._dict_result.update({"obs": e})

        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkWanInterface_x_427', dict_saida427)

            return self._dict_result

    
    def validarDHCPv6Wan_428(self, flask_username):
        self._dict_result.update({"obs": "Nao existe SLAAC", "Resultado_Probe": "OK", "result":"passed"})
        return self._dict_result


    def checkLANSettings_429(self, flask_username):
        try:
            dict_saida = {}    
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="folder15"]/table/tbody/tr/td/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="item18"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            prefix = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[2]/table[2]/tbody/tr/td[2]/input').get_attribute('value')
            print(prefix)
            dict_saida = {'Prefix': prefix}
            if prefix == 'fd00::/64':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": f"Prefix Delegation WAN: {prefix}", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno do Prefix Delegation WAN:{prefix}"})
        
        except Exception as e:
            self._dict_result.update({"obs": e})

        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkLANSettings_429', dict_saida)

            return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_431(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Type')
                    if iface_type == 'PPPoE': 
                        if sub_dict['VlanMuxId'] == '8,35': # ??? valor inconsistente ???
                            self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VlanId: 8,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno VlanMuxId: {sub_dict['VlanMuxId']}"})
                            break
                else:
                    self._dict_result.update({"obs": "Interface nao disponivel"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: {iface_type}, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_432(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_id = sub_dict.get('VlanMuxId')
                    if iface_id == '8,35': 
                        if sub_dict['Type'] == 'PPPoE':
                            self._dict_result.update({"obs": 'VlanId: 8,35, tipo: PPPoE', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Tipo: {sub_dict['Type']}"})
                            break
                else:
                    self._dict_result.update({"obs": "Interface nao disponivel"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_ADSL_vlanIdPPPoE_433(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                try:
                    nat = result['ppp0.1']['NAT']
                    if nat == 'Enabled':
                        self._dict_result.update({"obs": 'Interface PPPoE: NAT Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface PPPoE: NAT Desabilitado"})
                except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Interface não disponível"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result
    

    def checkMulticastSettings_434(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                try:
                    igmp = result['ppp0.1']['Igmp Src Enbl']
                    if igmp == 'Disabled':
                        self._dict_result.update({"obs": 'Interface PPPoE: Igmp Desabilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface PPPoE: Igmp Habilitado"})
                except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Interface não disponível"})
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
            print(cpe_config)
            usuario = result['Configurações']['Internet']['Usuário']
            print("teste 435:", usuario)
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                if usuario == 'cliente@cliente':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Usuário: cliente@cliente', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno: Usuário: {usuario}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result

    
    def vivo_1_passwordPppDefault_436(self, flask_username):
        try:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=self._address_ip, username='support', password='ffdfad94', timeout=2)
                print(self._address_ip)
                shell = ssh.invoke_shell()
                shell.send('tr69cli show\n')
                time.sleep(2)
                clientshow = shell.recv(65000).decode('utf-8')
                password = clientshow[clientshow.index('Password :')+10:clientshow.index('PeriodicInformEnable')].strip()

                if password == 'cliente':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Senha: cliente", "result":"passed"})
                else:
                    self._dict_result.update({'result':'failed',"obs": f"Teste incorreto, retorno senha: {password}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
            
        except (Exception, SSHException) as e:
            self._dict_result.update({"obs": e})

        return self._dict_result


    def checkWanInterface_x_437(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        print(result)
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                wan_interface = result['Network Protocal Selection:']
                if wan_interface == 'IPv4&IPv6(Dual Stack)':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Dual Stack", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno: {wan_interface}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})               
        return self._dict_result


    def validarDHCPv6Wan_438(self, flask_username):

        self._dict_result.update({"obs": "Nao existe SLAAC", "Resultado_Probe": "OK", "result":"passed"})
        return self._dict_result

    def checkLANSettings_439(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                ans_439 = result['Prefix']
                if 'fd00::/64' == ans_439:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix Delegation WAN: fd00::/64", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Prefix Delegation WAN:{ans_439}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})   
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_441(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Type')
                    if iface_type == 'PPPoE': 
                        if sub_dict['VlanMuxId'] == '0,35': # ??? valor inconsistente ???
                            self._dict_result.update({"obs": 'Encapsulamento: PPPoE, VlanId: 0,35', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno VlanMuxId: {sub_dict['VlanMuxId']}"})
                            break
                else:
                    self._dict_result.update({"obs": "Interface nao disponivel"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Encapsulamento: {iface_type}, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_442(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                for _, sub_dict in result.items():
                    iface_id = sub_dict.get('VlanMuxId')
                    if iface_id == '8,35': 
                        if sub_dict['Type'] == 'PPPoE':
                            self._dict_result.update({"obs": 'VlanId: 8,35, tipo: PPPoE', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Tipo: {sub_dict['Type']}"})
                            break
                else:
                    self._dict_result.update({"obs": "Interface nao disponivel"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_2_ADSL_vlanIdPPPoE_443(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                try:
                    nat = result['ppp0.1']['NAT']
                    if nat == 'Enabled':
                        self._dict_result.update({"obs": 'Interface PPPoE: NAT Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface PPPoE: NAT Desabilitado"})
                except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Interface não disponível"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result

    
    def checkMulticastSettings_444(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                try:
                    igmp = result['ppp0.1']['Igmp Src Enbl']
                    if igmp == 'Disabled':
                        self._dict_result.update({"obs": 'Interface PPPoE: Igmp Desabilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface PPPoE: IGMP Habilitado"})
                except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Interface não disponível"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} ACCESS:{cpe_config['ACCESS']} TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_2_usernamePppDefault_445(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        try:
            result = session.get_result_from_test(flask_username, 'getFullConfig_425')
            cpe_config = config_collection.find_one()
            usuario = result['Configurações']['Internet']['Usuário']
            print('\n #445 usuario:', usuario)
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
        try:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=self._address_ip, username='support', password='ffdfad94', timeout=2)
                print(self._address_ip)
                shell = ssh.invoke_shell()
                shell.send('tr69cli show\n')
                time.sleep(2)
                clientshow = shell.recv(65000).decode('utf-8')
                password = clientshow[clientshow.index('Password :')+10:clientshow.index('PeriodicInformEnable')].strip()

                if password == 'cliente':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Senha: cliente", "result":"passed"})
                else:
                    self._dict_result.update({'result':'failed',"obs": f"Teste incorreto, retorno senha: {password}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
            
        except (Exception, SSHException) as e:
            self._dict_result.update({"obs": e})

        return self._dict_result

    
    def validarDualStack_447(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 427 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_x_427')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 427 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':    
                wan_interface = result['Network Protocal Selection:']
                if wan_interface == 'IPv4&IPv6(Dual Stack)':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "IPv6: Dual Stack", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno: {wan_interface}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result

    def validarDHCPv6Wan_448(self, flask_username):
        cpe_config = config_collection.find_one()
        if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':   
            self._dict_result.update({"obs": "Nao existe SLAAC", "Resultado_Probe": "OK", "result":"passed"})
        else:
            self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result
    

    def prefixDelegationInet_449(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 429 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANSettings_429')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 429 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2' and cpe_config['ACCESS'] == 'COOPER' and cpe_config['TYPE'] == 'ADSL':   
                ans_449 = result['Prefix']
                if 'fd00::/64' == ans_449:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix Delegation WAN: fd00::/64", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Prefix Delegation WAN:{ans_449}"})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']} | ACCESS:{cpe_config['ACCESS']} | TYPE:{cpe_config['TYPE']}"})
        return self._dict_result


    def vivo_1_vlanIdIptvVivo1_450(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Mediaroom': 
                        if sub_dict['VlanMuxId'] == '20': 
                            self._dict_result.update({"obs": 'Mediaroom, VlanId: 20', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Mediaroom VlanMuxId: {sub_dict['VlanMuxId']}"})
                            break
                else:
                    self._dict_result.update({"obs": "Interface nao disponivel"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo_1_prioridadeIptv_451(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['REDE'] == 'VIVO_1':
                for _, sub_dict in result.items():
                    iface_type = sub_dict.get('Description')
                    if iface_type == 'Mediaroom': 
                        if sub_dict['Vlan8021p'] == '3':
                            self._dict_result.update({"obs": 'Mediaroom, Prioridade: 3', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno Prioridade: {sub_dict['Vlan8021p']}"})
                            break
                else:
                    self._dict_result.update({"obs": "Interface nao disponivel"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo_1_validarNatIptv_452(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if True: # cpe_config['REDE'] == 'VIVO_1':
                try:
                    nat = result['veip0.3']['NAT']
                    if nat == 'Enabled':
                        self._dict_result.update({"obs": 'Interface Mediaroom: NAT Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface Mediaroom: NAT Desabilitado"})
                except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Interface não disponível"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def vivo_1_igmpIptv_453(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_1':
                try:
                    igmp = result['veip0.3']['Igmp Src Enbl']
                    if igmp == 'Enabled':
                        self._dict_result.update({"obs": 'Interface Mediaroom: Igmp Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                    else:
                        self._dict_result.update({"obs": f"Teste incorreto, retorno Interface Mediaroom: Igmp Desabilitado"})
                except:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno Interface não disponível"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno REDE:{cpe_config['REDE']}"})
        return self._dict_result

    def vlanIdVodVivo2_454(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, values in result.items():
                    iface_type = values['Description']
                    vlan = values['VlanMuxId']
                    if iface_type == 'Multicast':
                        if vlan == '602':
                            self._dict_result.update({"obs": 'Name: Multicast, VLAN: 602', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: Multicast, VLAN: {vlan}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result

    
    def vivo2_validarNatIPTV_455(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 rode primeiro
        try:
            result = session.get_result_from_test(flask_username, 'checkWanInterface_420')

        except KeyError as exception:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})

        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_name = 'ipNotFound'
                    iface_type = sub_dict['Vlan8021p']
                    if iface_type == '3':
                        if sub_dict['VlanMuxId'] == '602':
                            iface_name = sub_dict['Description']
                            break

                for _, sub_dict in result.items():
                    iface_type = sub_dict['Description']
                    if iface_type == iface_name:
                        nat = sub_dict['NAT']
                        if nat == 'Enabled':
                            self._dict_result.update({"obs": 'Adm.State:  Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Adm.State: {nat} '})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name 1: {iface_type}, Name 2: {iface_name}'})

            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result

    def vivo_2_igmpVoD_456(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            cpe_config = config_collection.find_one()
            if cpe_config['REDE'] == 'VIVO_2':
                for _, sub_dict in result.items():
                    iface_type = sub_dict['Description']
                    if iface_type == 'Multicast':
                        if sub_dict['Igmp Src Enbl'] == 'Enabled':
                            self._dict_result.update({"obs": 'Interface: Multicast | IGMP: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Multicast | IGMP: {sub_dict["Igmp Src Enbl"]}'})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
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
                    iface_type = sub_dict['Description']
                    if iface_type == 'Multicast':
                        if sub_dict['VlanMuxId'] == '4000':
                            self._dict_result.update({"obs": 'Name: Multicast | VLAN: 4000', "result":'passed', "Resultado_Probe":"OK"})
                            break
                        else:
                            self._dict_result.update({"obs": f'Teste incorreto, retorno Name: ip5 | VLAN: {sub_dict["VlanMuxId"]} '})
                            break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Name: {iface_type}'})
            else:
                self._dict_result.update({"obs": f"REDE:{cpe_config['REDE']}"})
        return self._dict_result


    def natMulticastVivo2_458(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 423 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict['Description']
                if iface_type == 'Mediaroom':
                    if sub_dict['NAT'] == 'Disabled':
                        self._dict_result.update({"obs": 'Interface: Mediaroom | Adm.State: Desabilitado', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Mediaroom | Adm.State: {sub_dict["NAT"]} '})
                        break
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: {iface_type}'})
        return self._dict_result


    def checkIGMPVivo2_459(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 420 primeiro'})
        else:
            for _, sub_dict in result.items():
                iface_type = sub_dict['Description']
                if iface_type == 'Mediaroom':
                    if sub_dict['Igmp Src Enbl'] == 'Enabled':
                        self._dict_result.update({"obs": 'Interface: Mediaroom | IGMP: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
                        break
                    else:
                        self._dict_result.update({"obs": f'Teste incorreto, retorno Interface: Mediaroom | IGMP: {sub_dict["Igmp Src Enbl"]} '})
                        break
            else:
                self._dict_result.update({"obs":  f'Teste incorreto, retorno Interface: {iface_type}'})
        return self._dict_result


    def vivo1_vlanIdVoip_460(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for k, item in result.items():
                if True: # cpe_config['REDE'] == 'VIVO_1':
                    if item['Description'] == 'VoIP':
                        if item['VlanMuxId'] == '30': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "VoIP | VlanId: 30", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: VoIP, VlanId:{item['VlanMuxId']}"})
                            break
                elif cpe_config['REDE'] == 'VIVO_2':
                    if item['Description'] == 'VoIP':
                        if item['VlanMuxId'] == '601': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "VoIP | VlanId: 601", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: VoIP, VlanId:{item['VlanMuxId']}"})
                            break
                else:
                    self._dict_result.update({"obs": f"REDE: {cpe_config['REDE']}"})
        return self._dict_result


    def vivo2_prioridadeVoip_461(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for k, item in result.items():
                if True: # cpe_config['REDE'] == 'VIVO_1':
                    if item['Description'] == 'VoIP':
                        if item['Vlan8021p'] == '5': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "VoIP | Prioridade: 5", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: VoIP, Prioridade: {item['Vlan8021p']}"})
                            break
                elif cpe_config['REDE'] == 'VIVO_2':
                    if item['Description'] == 'VoIP':
                        if item['Vlan8021p'] == '601': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "VoIP | Prioridade: 601", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: VoIP, Prioridade: {item['Vlan8021p']}"})
                            break
                else:
                    self._dict_result.update({"obs": f"REDE: {cpe_config['REDE']}"})
        return self._dict_result


    def vivo1_validarNatVoip_462(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for k, item in result.items():
                if True: # cpe_config['REDE'] == 'VIVO_1':
                    if item['Description'] == 'VoIP':
                        if item['NAT'] == 'Enabled': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "VoIP | NAT: Habilitado", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: VoIP, NAT: {item['NAT']}"})
                            break
                elif cpe_config['REDE'] == 'VIVO_2':
                    if item['Description'] == 'VoIP':
                        if item['NAT'] == 'Enabled': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "VoIP | NAT: Habilitado", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: VoIP, NAT: {item['NAT']}"})
                            break
                else:
                    self._dict_result.update({"obs": f"REDE: {cpe_config['REDE']}"})
        return self._dict_result


    def vivo_1_igmpVoip_463(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 420 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkWanInterface_420')
        if len(result) == 0:
            self._dict_result.update({"obs": "Execute o teste 420 primeiro"})
        else:
            cpe_config = config_collection.find_one()
            for k, item in result.items():
                if True: # cpe_config['REDE'] == 'VIVO_1':
                    if item['Description'] == 'VoIP':
                        if item['Igmp Src Enbl'] == 'Enabled': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "VoIP | IGMP: Habilitado", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: VoIP, IGMP: {item['Igmp Src Enbl']}"})
                            break
                elif cpe_config['REDE'] == 'VIVO_2':
                    if item['Description'] == 'VoIP':
                        if item['Igmp Src Enbl'] == 'Enabled': 
                            self._dict_result.update({"Resultado_Probe": "OK", "obs": "VoIP | IGMP: Habilitado", "result":"passed"})
                            break
                        else:
                            self._dict_result.update({"obs": f"Teste incorreto, retorno: VoIP, IGMP: {item['Igmp Src Enbl']}"})
                            break
                else:
                    self._dict_result.update({"obs": f"REDE: {cpe_config['REDE']}"})
        return self._dict_result


    def checkLANDHCPSettings_x_464(self, flask_username):
        try:
            dict_saida464 = {}
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="folder15"]/table/tbody/tr/td/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            dict_saida464 = {}
            tabela = self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody//td')
            dict_saida464[tabela[0].text.strip(': ')] = tabela[1].find_element_by_tag_name('input').get_attribute('value')
            dict_saida464[tabela[2].text.strip(': ')] = tabela[3].find_element_by_tag_name('input').get_attribute('value')
            
            igmp_snooping = self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td')
            dict_saida464[igmp_snooping.text.strip(': ')] = igmp_snooping.find_element_by_tag_name('input').get_attribute('checked')

            tabela = self._driver.find_elements_by_xpath('//*[@id="igmpSnpInfo"]/table[1]/tbody//td')
            dict_saida464[tabela[0].text.strip(': ')] = tabela[0].find_element_by_tag_name('input').get_attribute('checked')
            dict_saida464[tabela[1].text.strip(': ')] = tabela[1].find_element_by_tag_name('input').get_attribute('checked')
            
            tabela = self._driver.find_elements_by_xpath('//*[@id="igmpSnpInfo"]/table[2]/tbody/tr[1]//td')
            dict_saida464[tabela[0].text.strip(': ')] = Select(tabela[1].find_element_by_tag_name('select')).first_selected_option.text
            
            lan_firewall = self._driver.find_element_by_xpath('//*[@id="firewallEnbl"]/table/tbody/tr/td')
            dict_saida464[lan_firewall.text.strip(': ')] = lan_firewall.find_element_by_tag_name('input').get_attribute('checked')
            
            tabela = self._driver.find_elements_by_xpath('//*[@id="dhcpInfo"]/table/tbody//td')
            dict_saida464[tabela[0].text.strip(': ')] = tabela[0].find_element_by_tag_name('input').get_attribute('checked')
            dict_saida464[tabela[1].text.strip(': ')] = tabela[1].find_element_by_tag_name('input').get_attribute('checked')
            dict_saida464[tabela[2].text.strip(': ')] = tabela[3].find_element_by_tag_name('input').get_attribute('value')
            dict_saida464[tabela[4].text.strip(': ')] = tabela[5].find_element_by_tag_name('input').get_attribute('value')
            dict_saida464[tabela[6].text.strip(': ')] = tabela[7].find_element_by_tag_name('input').get_attribute('value')

            dhcp_cond = self._driver.find_element_by_xpath('//*[@id="dhcpcondservEnbl"]/table/tbody/tr/td')
            dict_saida464[dhcp_cond.text] = dhcp_cond.find_element_by_tag_name('input').get_attribute('checked')

            tabela = self._driver.find_elements_by_xpath('//*[@id="dhcpcondservInfo"]/table/tbody//td')
            for n in range(0,13,2):
                dict_saida464[tabela[n].text.strip(': ')] = tabela[n+1].find_element_by_tag_name('input').get_attribute('value')
            for id_mode in tabela[15].find_elements_by_tag_name('input'):
                if id_mode.get_attribute('checked'):
                    dict_saida464[tabela[14].text.strip(': ')] = id_mode.get_attribute('value')
            for id_mode in tabela[17].find_elements_by_tag_name('input'):
                if id_mode.get_attribute('checked'):
                    dict_saida464[tabela[16].text.strip(': ')] = id_mode.get_attribute('value')
            dict_saida464[tabela[18].text.strip(': ')] = tabela[19].find_element_by_tag_name('input').get_attribute('value')

            second_ip = self._driver.find_element_by_xpath('//*[@id="lan2All"]/table/tbody/tr[2]/td')
            dict_saida464[second_ip.text] = second_ip.find_element_by_tag_name('input').get_attribute('checked')

            tabela = self._driver.find_elements_by_xpath('//*[@id="lan2Info"]/table/tbody//td')
            dict_saida464[tabela[0].text.strip(': ')+'_2'] = tabela[1].find_element_by_tag_name('input').get_attribute('value')
            dict_saida464[tabela[2].text.strip(': ')+'_2'] = tabela[3].find_element_by_tag_name('input').get_attribute('value')

            tabela = self._driver.find_elements_by_xpath('//*[@id="lanDns"]/table/tbody//td')
            dict_saida464[tabela[0].text.strip(': ')] = tabela[0].find_element_by_tag_name('input').get_attribute('checked')
            dict_saida464[tabela[1].text.strip(': ')] = tabela[1].find_element_by_tag_name('input').get_attribute('checked')

            print(dict_saida464)
            if dict_saida464['IP Address'] == '192.168.18.1':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": f"Gateway: {dict_saida464['IP Address']}", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Gateway: {dict_saida464['IP Address']}"})
        
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkLANDHCPSettings_x_464', dict_saida464)
            return self._dict_result
       

    def poolDhcpLan_465(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            start_addr = result['Start IP Address']
            end_addr = result['End IP Address']
            if start_addr == '192.168.18.2' and end_addr == '192.168.18.200':
                self._dict_result.update({"obs": 'IP Address Range OK', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'IP Address Range NOK. {start_addr} : {end_addr}'})
        return self._dict_result


    def leaseTime_466(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            ans_466 = result['Leased Time (hour)']
            if '4' == ans_466:
                self._dict_result.update({"obs": 'Lease Time: 4 horas', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Lease Time: {ans_466}'})      
        return self._dict_result

    
    def vendorIdIptvEnable_467(self, flask_username):
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        self._driver.quit()
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            vendorID_check = result['Enable DHCP Conditional Serving Pool']
            vendor_id = result['VendorID']
            cpe_config = config_collection.find_one()
            
            #1
            if vendorID_check == 'true':
                obs_result1 = f'VendorID esta Habilitado'
                self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
            else:
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                obs_result1 = f"Teste incorreto, retorno VendorID: {vendorID_check}"

            #2
            if True: #cpe_config['REDE'] == 'VIVO_1':
                if vendor_id == 'MSFT_IPTV,TEF_IPTV':
                    obs_result2 = f'Valor VendorID: {vendor_id}'
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                    obs_result2 = f"Teste incorreto, retorno Valor VendorID: {vendor_id}"
            else:
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
                obs_result2 = f"REDE:{cpe_config['REDE']}"
            
            #3
            # if cpe_config['REDE'] == 'VIVO_2':
            #     if vendor_id == 'GVT-STB,RSTIH89-500_HD,DSTIH78_GVT,VM1110,DSTIH79_GVT,VM1110_HD_HYBRID,DSITH79_GVT_HD':
            #         obs_result3 = f'Valor VendorID: {vendor_id}'
            #         self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
            #     else:
            #         self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
            #         obs_result3 = f"Teste incorreto, retorno Valor VendorID: {vendor_id}"
            # else:
            #     self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
            #     obs_result3 = f"REDE:{cpe_config['REDE']}"

            self._dict_result.update({"obs": f"467_1: {obs_result1} | 467_2: {obs_result2}"})# | 467_3: {obs_result3}"})
            
        return self._dict_result


    def poolDhcpIptv_468(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 464 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 467 primeiro'})
        else:
            ip_inicio = result['Pool Start']
            ip_fim = result['Pool End']
            if ip_inicio == '192.168.18.230' and ip_fim == '192.168.18.254':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'IP Address Range: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno IP Address Range: {ip_inicio} | {ip_fim}'})         
        return self._dict_result

    
    def igmpSnoopingLAN_469(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 464 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkLANDHCPSettings_x_464')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 464 primeiro'})
        else:
            igmp_check = result['Enable IGMP Snooping']
            if igmp_check == 'true':
                self._dict_result.update({"obs": 'IGMP Snooping: Habilitado', "result":'passed', "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno IGMP Snooping: {igmp_check}'})
       
        return self._dict_result     


    def verificarWifi24SsidDefault_470(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            result_ssid = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['SSID']
            ssid = re.findall("^VIVOFIBRA-\w{4}", result_ssid)
            #print("\n #470 SSID:", result_ssid, " ", ssid)
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
            #print("\n #471 WiFi:", rede_pv)
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
            modo_ope = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Avançadas']['Modo de Operação']
            #print("\n #472 Wifi:", modo_ope)
            if modo_ope == '802.11g/n':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Operação: 802.11g/n', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retornoModo de Operação: {modo_ope}'})
        return self._dict_result

    
    def frequencyPlan_473(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
        self.login_support()
        time.sleep(1)
        self._driver.switch_to.frame('menufrm') 
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[50]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[53]/table/tbody/tr/td/a').click()
        time.sleep(1)

        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        
        bandwidth24G = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[2]/table/tbody/tr[1]/td[2]/select').text.split()[0]
        channel24G_list = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr[2]/td[2]/select//option')]
        print(channel24G_list)
        cpe_config = config_collection.find_one()
        ref_list = cpe_config["REF_CHANNEL_2_4_20MHz"]     
        print(ref_list)

        if bandwidth24G == '20MHz':
            if channel24G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

        else:
            if channel24G_list == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

        return self._dict_result     
        


    def verificarWifi24AutoChannel_474(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            canal = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Avançadas'].get('Canal:')
            #print("\n #474: ", canal)
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
            larg_banda_canal = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Avançadas']['Largura de Banda do Canal']
            #print("\n #475: ", larg_banda_canal)
            if larg_banda_canal == '20MHz':
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
            #print("\n 476: ", seguranca)
            if seguranca == 'WPA2':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Segurança: WPA2', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retornoModo de Segurança: {seguranca}'})          
        return self._dict_result


    def verificarWifi24PasswordDefault_477(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
        self.login_support()
        time.sleep(1)
        self._driver.switch_to.frame('menufrm') 
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[50]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="item51"]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('basefrm')
        time.sleep(1)

        passphrase_value = self._driver.find_element_by_xpath('/html/body/blockquote[1]/form/div[9]/table/tbody/tr/td[2]/input').get_attribute('value')
        password = re.findall("^\w{8}", passphrase_value)

        if password:
            self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Passprhase: OK', "result":"passed"})
        else:
            self._dict_result.update({"obs": 'Teste incorreto, retorno Passphrase: NOK'})          

        self._driver.quit()
        return self._dict_result


    def cipherModeDefault_478(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
        self.login_support()
        time.sleep(1)
        self._driver.switch_to.frame('menufrm') 
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[50]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="item51"]/table/tbody/tr/td/a').click()
        time.sleep(1)
        self._driver.switch_to.parent_frame()  
        self._driver.switch_to.frame('basefrm')
        time.sleep(1)

        encryption = self._driver.find_element_by_xpath('/html/body/blockquote[1]/form/div[12]/table/tbody/tr/td[2]/select').get_attribute('value')
        print(encryption)
     
        if encryption in "AESaes":
            self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Encryption: AES', "result":"passed"})
        else:
            self._dict_result.update({"obs": f'Teste incorreto, retorno Encryption: {encryption}'})          
        self._driver.quit()

        return self._dict_result


    def verificarWifi24WPS_479(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            wps = result['Configurações']['Rede Wifi 2.4Ghz']['Configurações Básicas']['WPS']
            #print("\n 479: ", wps)
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
            #print("\n 480: ", result_ssid, ", ", ssid)
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
            #print("\n 481: ", rede_pv)
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
            #print("\n 482: ", modo_ope)
            if modo_ope == '802.11n/ac':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Modo de Operação: 802.11n/ac', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno Modo de Operação: {modo_ope}'})           
        return self._dict_result


    def frequencyPlan5GHz_483(self, flask_username):
        self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
        self.login_support()
        time.sleep(1)
        self._driver.switch_to.frame('menufrm') 
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[55]/table/tbody/tr/td/a/span').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[57]/table/tbody/tr/td/a').click()
        time.sleep(1)

        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')

        bandwidth5G = self._driver.find_element_by_xpath('/html/body/blockquote/form/table/tbody/tr[2]/td[2]/select').text.split()[0]

        channel5G = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table/tbody/tr[4]/td[2]/select//option')]

        cpe_config = config_collection.find_one()
        
        ref_list = cpe_config["REF_CHANNEL_5_40MHz"]      
        print('ref: ',ref_list)
        if bandwidth5G == '20MHz':
            if channel5G == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

       
        if bandwidth5G == '40MHz':
            if channel5G == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})
         
        if bandwidth5G == '80MHz':
            if channel5G == ref_list:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'check List Channels: OK', "result":"passed"})
            else:
                self._dict_result.update({"obs": 'Teste incorreto, retorno check List Channels: NOK'})

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
            if larg_banda_canal == '80MHz':
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
        try:
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm') 
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[55]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            aes = self._driver.find_element_by_xpath('/html/body/blockquote/form/div[10]/table/tbody/tr/td[2]/select').text.split()[0]
            print(aes)

            if aes in "AESaes":
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": 'Encryption: AES', "result":"passed"})
            else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno Encryption: {aes}'})
        except Exception as e:
            self._dict_result.update({"obs": e})
        
        self._driver.quit()
        return self._dict_result

    
    def verificarWifi5WPS_489(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            wps = result['Configurações']['Rede Wifi 5Ghz']['Configurações Básicas'].get('WPS:')
            if wps == 'Habilitado':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": 'WPS: Habilitado', "result":"passed"})
            else:
                self._dict_result.update({"obs": f'Teste incorreto, retorno WPS: {wps}'})          
        return self._dict_result


    def checkVoIPSettings_490(self, flask_username):
        
        try:
            dict_saida = {}
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm') 
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[60]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[62]/table/tbody/tr/td/a').click()

            time.sleep(1)

            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            # Page 1
            self._driver.find_element_by_xpath('/html/body/form[2]/table[2]/tbody/tr/td[3]/input').click()
            time.sleep(3)
            fax = ['Disable' for value in self._driver.find_elements_by_xpath('/html/body/form[2]/div[2]/table[9]/tbody/tr/td[2]/input') if value.get_attribute('name') == 'VoIP_FaxRelay' and value.get_attribute('checked') == None]
            time.sleep(1)
            dtmf = self._driver.find_element_by_xpath('/html/body/form[2]/div[2]/table[8]/tbody/tr/td[2]/select').text.split()[0]


            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm') 
            # Page 2
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[61]/table/tbody/tr/td/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)

            self._driver.find_element_by_xpath('/html/body/form/div/div/div/form/table[4]/tbody/tr/td[3]/input').click()
            time.sleep(1)
            list_codec1 = self._driver.find_element_by_xpath('/html/body/form/div/div/div/form/div[5]/table[2]/tbody/tr[1]/td[3]/select').get_attribute('value')
            time.sleep(1)
            list_codec2 = self._driver.find_element_by_xpath('/html/body/form/div/div/div/form/div[5]/table[2]/tbody/tr[2]/td[3]/select').get_attribute('value')

            dict_saida = {'T.38': fax[0], 'DTMF Method': dtmf, 'codec_1': list_codec1, 'codec_2': list_codec2}
            
            cpe_config = config_collection.find_one()

            if cpe_config['REDE'] == 'VIVO_1':
                if dict_saida['T.38'] == 'Disable':
                    obs_result1 =  f"Fax T38: Desabilitado"
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"}) 
                    obs_result1 = f"Teste incorreto, retorno Fax T38: {dict_saida['T.38']}"
            else: 
                obs_result1 = f"REDE:{cpe_config['REDE']}"
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
            
            if cpe_config['REDE'] == 'VIVO_2':
                if dict_saida['T.38'] == 'Disable':
                    obs_result2 =  f"Fax T38: Desabilitado"
                    self._dict_result.update({"Resultado_Probe": "OK", "result":"passed"})
                else:
                    obs_result2 = f"Teste incorreto, retorno Fax T38: {dict_saida['T.38']}"
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})

            else: 
                obs_result2 = f"REDE:{cpe_config['REDE']}"
                self._dict_result.update({"Resultado_Probe": "NOK", "result":"failed"})
            
            self._dict_result.update({"obs": f"490_1: {obs_result1} | 490_2: {obs_result2}"})
        except Exception as e:
            self._dict_result.update({"obs": str(e)})
        finally:
            self._driver.quit()

            self.update_global_result_memory(flask_username, 'checkVoIPSettings_490', dict_saida)
            return self._dict_result


    def verificarDtmfMethod_491(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            basic_setting = result['DTMF Method']
            if basic_setting == 'RFC2833':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "DTMF Method: RFC2833", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno DTMF Method: {basic_setting}"})
        return self._dict_result
    

    def prioridadeCodec_0_493(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            codec = result['codec_1']
            if codec == 'G.711ALaw':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Order: 0 = G.711ALaw", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Order: 0 = {codec} "})
        return self._dict_result

    
    def prioridadeCodec_1_494(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 490 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkVoIPSettings_490')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 490 primeiro'})
        else:
            codec = result['codec_2']

            if codec == 'G.729':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Order: 1 = G.729", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Order: 1 = {codec} "})
        return self._dict_result


    def checkNATALGSettings_495(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm') 
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[11]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[20]/table/tbody/tr/td/a/span').click()

            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[24]/table/tbody/tr/td/a').click()
            time.sleep(1)

            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)

            sip = self._driver.find_element_by_xpath('/html/body/blockquote/form/input').get_attribute('checked')
            print(sip)
            time.sleep(1)
            
            if sip == 'true': sip = 'Habilitado'
            else: sip = ' Desabilitado'

            cpe_config = config_collection.find_one()
            rede = cpe_config['REDE']

            if rede == 'VIVO_1':   
                if sip == 'Desabilitado':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": f'SIP: Desabilitado (Rede = {rede})', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno SIP: {sip} (Rede = {rede})'})
                return self._dict_result

            elif rede == 'VIVO_2':   
                if sip == 'Habilitado':
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": f'SIP == Habilitado (Rede = {rede})', "result":"passed"})
                else:
                    self._dict_result.update({"obs": f'Teste incorreto, retorno SIP: {sip} (Rede = {rede})'})
                return self._dict_result 
            
            else:
                self._dict_result.update({"obs": f'REDE: {rede})'})
        except Exception as e:
            self._dict_result.update({"obs": e})
        
        finally:
            self._driver.quit()
            return self._dict_result


    def checkSNMP_496(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm') 
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[71]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[78]/table/tbody/tr/td/a/span').click()

            time.sleep(1)

            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            
            snmp_name = [value.text for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr//td') if value.text != 'SNMP Agent']
            snmp = [value.get_attribute('checked') for value in self._driver.find_elements_by_xpath('/html/body/blockquote/form/table[1]/tbody/tr/td//input') ]

            snmp = snmp_name[snmp.index('true')]
            print(snmp)

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
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('menufrm') 
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[11]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/table/tbody/tr/td/div[39]/table/tbody/tr/td/a/span').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)
            
            upnp = self._driver.find_element_by_xpath('/html/body/blockquote/form/b/table/tbody/tr/td[1]/input').get_attribute('checked')

            print(upnp)

            if upnp == 'true':
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "UPnP: Habilitado", "result":"passed"})
            else:
                self._dict_result.update({"obs": "Teste incorreto, retorno UPnP: Desabilitado"})

        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result


    def linkLocalType_498(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            linkLocal = result['Status']['INTERNET']['IPv6'].get('Endereço IPv6 Link-Local - LAN:')
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
            linkGlobal = result['Status']['INTERNET']['IPv6'].get('Endereço IPv6 Global - WAN:')
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
            ans_500 = result['Prefix']
            if 'fd00::/64' == ans_500:
                self._dict_result.update({"Resultado_Probe": "OK", "obs": "Prefix Delegation WAN: fd00::/64", "result":"passed"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Prefix Delegation WAN:{ans_500}"})
        return self._dict_result
        