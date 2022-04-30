from audioop import lin2lin
from gc import collect
from http import client
from re import sub
import re
import time
from datetime import datetime
# from turtle import up
# from tkinter.messagebox import NO
from ..AskeyECNT import HGU_AskeyECNT
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

import paramiko
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException
from paramiko.ssh_exception import SSHException
import socket
from selenium.common.exceptions import UnexpectedAlertPresentException

from HGUmodels.main_session import MainSession

from HGUmodels import wizard_config

session = MainSession()

mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()

class HGU_AskeyECNT_wizardProbe(HGU_AskeyECNT):

    def accessWizard_373(self, flask_username):
            #TODO: Fazer logica no frontend para garantir que o teste 401 seja executado em conjunto
            result = session.get_result_from_test(flask_username, 'accessWizard_401')
            if len(result) == 0:
                self._dict_result.update({"obs": 'Execute o teste 401 primeiro'})
            else:
                ans_500 = result['Resultado_Probe']
                if 'OK' == ans_500:
                    self._dict_result.update({"Resultado_Probe": "OK", "obs": "Teste OK", "result":"passed"})
                else:
                    self._dict_result.update({"obs": f"Teste incorreto, retorno: {ans_500}"})
            return self._dict_result
            

    def logoutWizard_374(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.get('http://' + self._address_ip + '/login.asp')
            self.login_support()
            time.sleep(2)
            try:
                self._driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/a').click()
                self._dict_result.update({"obs": "Logout efetuado com sucesso", "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Nao foi possivel efetuar o logout"})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result


    def checkRedeGpon_375(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/login.asp')

            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            time.sleep(1)
            gpon = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]//div')]
            dict_saida = {
                "Status":
                    {
                        gpon:
                            {div[0].split(':')[0]: div[0].split(':')[1],
                            div[1].split(':')[0]: div[1].split(':')[1],
                            div[2].split(':')[0]: div[2].split(':')[1],
                            }
                    }
            }
            print(dict_saida)
            link = dict_saida['Status']['GPON']['Link']
            self._driver.quit()

            if link == 'Não Estabelecido':
                self._dict_result.update({"obs": "Link: Não Estabelecido", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Link: {link}"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self.update_global_result_memory(flask_username, 'checkRedeGpon_375', dict_saida)
            return self._dict_result
    

    def changePPPoESettingsWrong_376(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.get('http://' + self._address_ip + '/login.asp')
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            time.sleep(1)
            config_internet = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="txtUsername"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
            self._driver.find_element_by_xpath('//*[@id="btnSave"]').click()
            time.sleep(1)
            try:
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/span') or self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[2]/span'):
                    self._dict_result.update({"obs": "Verificacao OK", "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Teste falhou"})
            self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  


    def changePPPoESettingsWrong_377(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.get('http://' + self._address_ip + '/login.asp')
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            config = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            time.sleep(1)
            config_internet = self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[1]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="txtUsername"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtUsername"]').send_keys('vivo@cliente')
            self._driver.find_element_by_xpath('//*[@id="txtPassword"]').clear()
            self._driver.find_element_by_xpath('//*[@id="txtPassword"]').send_keys('vivo')
            self._driver.find_element_by_xpath('//*[@id="btnSave"]').click()
            time.sleep(15)
            try:
                time.sleep(8)
                if self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[4]/td/label/font').text == 'Conectado':
                    if self._driver.find_element_by_xpath('//*[@id="txtUsername"]').get_attribute('value') == 'vivo@cliente':
                        self._dict_result.update({"obs": "Usuario aceito"})
                    else:
                        self._dict_result.update({"obs": f"Teste falhou, usuario nao foi aceito", "result":"passed", "Resultado_Probe": "OK"})
            except UnexpectedAlertPresentException as e:                
                self._dict_result.update({"obs": f"Teste falhou. {e}", "result":"passed", "Resultado_Probe": "OK"})
            finally:
                self._driver.quit()
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            return self._dict_result  


    
    def connectWizardhttps_379(self,flask_username):
        try:
            try:
                self._driver.get('https://' + self._address_ip + '/')
                time.sleep(1)
                self._dict_result.update({"obs": "Acesso via HTTPS OK", "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Nao foi possivel acessar via HTTPS"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})

        except Exception as e:
            self._dict_result.update({"obs": e})
        
        finally:
            self._driver.quit()
            return self._dict_result


    def checkPPPoEStatus_380(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/index_cliente.asp')
            time.sleep(1)
            gpon = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]//div')]
            dict_saida = {
                "Status":
                    {
                        gpon:
                            {div[0].split(':')[0]: div[0].split(':')[1],
                            div[1].split(':')[0]: div[1].split(':')[1],
                            div[2].split(':')[0]: div[2].split(':')[1],
                            }
                    }
            }
            print(dict_saida)
            self._dict_result.update({"obs": dict_saida, "result":"passed", "Resultado_Probe": "OK"})
        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result


    def getFullConfig_382(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            idioma = result['Gerenciamento']['Idioma']
            if idioma == 'Português':
                self._dict_result.update({"obs": "Idioma: Português", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Idioma: {idioma}"})
        return self._dict_result


    def execPingWizard_384(self, flask_username):

        destino = '8.8.8.8',
        tentativas = "1"
        try:
            self._driver.get('http://' + self._address_ip + '/login.asp')
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[6]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="txtDest"]').send_keys(destino)
            self._driver.find_element_by_xpath('//*[@id="txtNum"]').send_keys(tentativas)
            self._driver.find_element_by_xpath('//*[@id="btnTest"]').click()
            time.sleep(5)
            result = self._driver.find_element_by_xpath('//*[@id="txtResult"]').get_property('value')
            self._driver.quit()
            self._dict_result.update({"obs": f"Resultado: {result}", "result":"passed", "Resultado_Probe": "OK"})
        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})

        except Exception as e:
            self._dict_result.update({"obs": e})

        finally:
            return self._dict_result


    def statusWizardInet_387(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            statusInternet = result['Status']['Internet']
            ppp, ipv4, ipv4_wizard_list = statusInternet['PPP:'], statusInternet['IPv4'], wizard_config.INTERNET_IPV4

            ipv6, ipv6_wizard_list = statusInternet['IPv6'], wizard_config.INTERNET_IPV6

            if set(ipv4) == set(ipv4_wizard_list) and set(ipv6) == set(ipv6_wizard_list) and ppp != '':
                self._dict_result.update({"obs": "Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste inscorreto, retorno PPP: {ppp} IPv4: {ipv4} | IPv6: {ipv6}"})

        return self._dict_result


    def registerWizardVoip_388(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            ifaceVoip = result['Status']['Telefone']['Rede:']
            registerVoIP = result['Status']['Telefone']['Telefone:']

            if ifaceVoip == 'Disponível' and (registerVoIP != 'Não Registrado' or registerVoIP == ''):
                self._dict_result.update({"obs": f"Rede: Disponível | Telefone: {registerVoIP}", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Rede: Disponível | Telefone: {registerVoIP}"})

        return self._dict_result

    def statusWizardIptv_389(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['TV']
            iptv = wizard_config.IPTV
            if set(status) == set(iptv):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno TV: {status}"})
            
        return self._dict_result


    def statusWizardVoip_390(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            status = result['Status']['Telefone']
            voip = wizard_config.VOIP

            if set(status) == set(voip):
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno VoIP: {status}"})
            
        return self._dict_result

    def testeSiteWizard_399(self, flask_username):
        site1 = 'http://menuvivofibra.br'
        site2 = f'http://{self._address_ip}/index_instalador.asp'
        site3 = 'http://instaladorvivofibra.br'
        
        try:
            self._driver.get(site1)
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado1 = 'ok'
        except:
            resultado1 = 'falhou'
        
        try:
            self._driver.get(site2)
            time.sleep(2)
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys('support')
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado2 = 'ok'
        except:
            resultado2 = 'falhou'

        try:
            self._driver.get(site3)
            time.sleep(1)
            self._driver.switch_to.frame('mainFrame')
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            elementos = self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[1]')
            resultado3 = 'ok'
        except:
            resultado3 = 'falhou'
 
        self._driver.quit()
        if resultado1 == 'ok' and resultado2 == 'ok' and resultado3 == 'ok':
            self._dict_result.update({"obs": "URLs de redirecionamento ok", "result":"passed", "Resultado_Probe": "OK"})
        else:
            self._dict_result.update({"obs": f"Teste incorreto, retorno URLs: {site1}: {resultado1}; {site2}: {resultado2}; {site3}: {resultado3}"})
        return self._dict_result


    def checkBridgeMode_21(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/login.asp')
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            login_button = self._driver.find_element_by_id('btnLogin')
            time.sleep(1)
            login_button.click()
            time.sleep(1)
            self._driver.find_element_by_link_text('Configurações').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/ul/li[2]/ul/li[7]/a').click()
            config_modowan = [value.get_attribute('text') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[3]/form/table/tbody/tr[1]/td[2]/select//option') ]
            if "Bridge" in config_modowan:
                self._dict_result.update({"obs": f"Modo WAN: {config_modowan}", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Modo WAN: {config_modowan}"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})

        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result
    
    def checkRedeGpon_36(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 375 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'checkRedeGpon_375')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 375 primeiro'})
        else:
            link = result['Status']['GPON']['Link']
            if link == 'Estabelecido':
                self._dict_result.update({"obs": "Link Estabelecido", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Link: {link}"})
    
        return self._dict_result

    
    def accessPadrao_79(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('mainFrm')
            self._driver.find_element_by_xpath('//*[@id="tbGPONinfo"]')
            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
        except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
            self._dict_result.update({"obs": 'Nao foi possivel realizar o login'})
        finally:
            self._driver.quit()
            return self._dict_result


    def checkPPPoEStatus_146(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/login.asp')
            time.sleep(1)
            self._driver.switch_to.default_content()
            user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/input')
            user_input.send_keys(self._username)
            pass_input = self._driver.find_element_by_id('txtPass')
            pass_input.send_keys(self._password)
            self._driver.find_element_by_id('btnLogin').click()
            time.sleep(1)
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[3]/td[1]//div')]
            dict_saida = {
                "Status":
                    {
                        "Internet":
                            {div[0].split(':')[0]: div[0].split(':')[1],
                           
                            }
                    }
            }
            print(dict_saida)
            ppp = dict_saida["Status"]["Internet"]["PPP"]
            if ppp == 'Conectado':
                self._dict_result.update({"obs": "PPP: Conectado", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno PPP: {ppp}"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result