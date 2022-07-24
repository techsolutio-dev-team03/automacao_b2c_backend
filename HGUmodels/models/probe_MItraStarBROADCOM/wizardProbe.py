#from asyncio import exceptions
from cgi import print_form
from os import name
import re
import time
# from jinja2 import pass_context
#from typing import final
import paramiko
from paramiko.ssh_exception import AuthenticationException
import socket
from ..MItraStarBROADCOM import HGU_MItraStarBROADCOM
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.select import Select
from HGUmodels.config import TEST_NOT_IMPLEMENTED_WARNING
from HGUmodels.utils import chunks
from daos.mongo_dao import MongoConnSigleton
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException, NoSuchFrameException, UnexpectedAlertPresentException, ElementClickInterceptedException

from HGUmodels import wizard_config

from HGUmodels.main_session import MainSession

session = MainSession()


mongo_conn = MongoConnSigleton(db='config', collection='cpe_config')
config_collection = mongo_conn.get_collection()

dict_test_result_memory = {}

class HGU_MItraStarBROADCOM_wizardProbe(HGU_MItraStarBROADCOM):
    def accessWizard_373(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 401 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'accessWizard_401')
        print(result)
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
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(2)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            try:
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('header')
                self._driver.find_element_by_xpath('/html/body/div/div[1]/p/a[3]').click()
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
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(2)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("menufrm")
            time.sleep(1)
            
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("basefrm")
            gpon = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/th/span').text
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]//div')]
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

            if link == 'Não Estabelecido':
                self._dict_result.update({"obs": "Link: Não Estabelecido", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Link: {link}"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            self.update_global_result_memory(flask_username, 'checkRedeGpon_375', dict_saida)
            return self._dict_result
  

    def changePPPoESettingsWrong_376(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(2)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("basefrm")
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="username"]').clear()
            self._driver.find_element_by_xpath('//*[@id="password"]').clear()
            self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/form/table/tfoot/tr/td/a[2]/span').click()
            time.sleep(1)
            try:
                if self._driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/form/table/tbody/tr[2]/td[2]/span') or self._driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/form/table/tbody/tr[3]/td[2]/span'):
                    self._dict_result.update({"obs": "Verificacao OK", "result":"passed", "Resultado_Probe": "OK"})
            except:
                self._dict_result.update({"obs": "Teste falhou"})
        except Exception as e:
            self._dict_result.update({"obs": e})
        finally:
            self._driver.quit()
            return self._dict_result 


    def changePPPoESettingsWrong_377(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            self._driver.implicitly_wait(10)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            self.admin_authentication_mitraStat()
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('//*[@id="username"]').clear()
            self._driver.find_element_by_xpath('//*[@id="password"]').clear()
            self._driver.find_element_by_xpath('//*[@id="username"]').send_keys('vivo@cliente')
            self._driver.find_element_by_xpath('//*[@id="password"]').send_keys('vivo')
            self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/form/table/tfoot/tr/td/a[2]/span').click()
            try:
                WebDriverWait(self._driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/iframe')))
                iframe = self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                self._driver.find_element_by_xpath('/html/body/div/table/tbody/tr[4]/td/a/span').click()
                time.sleep(30)
                # self._driver.switch_to.default_content()
                # self._driver.switch_to.frame('basefrm')
                # self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').clear()
                # self._driver.find_element_by_xpath('//*[@id="RN_UserName"]').send_keys('cliente@cliente')
                # self._driver.find_element_by_xpath('//*[@id="RN_Password"]').clear()
                # self._driver.find_element_by_xpath('//*[@id="RN_Password"]').send_keys('cliente')
                # self._driver.find_element_by_xpath('//*[@id="conteudo-gateway"]/form/table/tfoot/tr/td/a[2]/span').click()
                # time.sleep(30)
                self._dict_result.update({"obs": "Usuario inválido", "result":"passed", "Resultado_Probe": "OK"})
            except TimeoutException as e:
                self._dict_result.update({"obs": f'Usuario aceito. {e}'})
        except Exception as e:
            self._dict_result.update({"obs": str(e)})
        finally:
            self._driver.quit()
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
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("menufrm")
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("basefrm")
            gpon = self._driver.find_element_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/th/span').text
            div = [value.text.replace('\n', '') for value in self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]//div')]
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
            print('aqui:', idioma)
            if idioma == 'Português':
                self._dict_result.update({"obs": "Idioma: Português", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Idioma: {idioma}"})
        return self._dict_result



    def execPingWizard_384(self, flask_username):

        destino = '8.8.8.8',
        tentativas = "1"
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('/html/body/div/div/div/ul/li[2]/ul/li[1]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(2)
            self.admin_authentication_mitraStat()
            time.sleep(1)

            # feito ate aqui
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("menufrm")
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[6]/a').click()
            time.sleep(1)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame("basefrm")
            self._driver.find_element_by_xpath('//*[@id="diagAddr"]').send_keys(destino)
            self._driver.find_element_by_xpath('//*[@id="diagPingNum"]').send_keys(tentativas)
            self._driver.find_element_by_xpath('//*[@id="Test_diag"]').click()
            time.sleep(5)
            result = self._driver.find_element_by_xpath('/html/body/div/div[1]/div[1]/div[1]/form/div/table/tbody/tr[6]/td/textarea').get_property('value')
            self._dict_result.update({"obs": f"Resultado: {result}", "result":"passed", "Resultado_Probe": "OK"})
        except NoSuchElementException as exception:
            self._dict_result.update({"obs": exception})

        except Exception as e:
            self._dict_result.update({"obs": e})

        finally:
            self._driver.quit()
            return self._dict_result


    def statusWizardInet_387(self, flask_username):
        #TODO: Fazer logica no frontend para garantir que o teste 425 seja executado em conjunto
        result = session.get_result_from_test(flask_username, 'getFullConfig_425')
        if len(result) == 0:
            self._dict_result.update({"obs": 'Execute o teste 425 primeiro'})
        else:
            statusInternet = result['Status']['INTERNET']
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
            registerVoIP = result['Status']['Telefone']['Telefone1:']

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
            
            print('STATUS:', status['Rede:'], status['Telefone1:'])
            print('VOIP:', voip)

            if status['Rede:'] == 'Disponível' and status['Telefone1:'] == 'Endereço IP de VoIP:':
                self._dict_result.update({"obs": f"Teste OK", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno VoIP: {status}"})
        return self._dict_result


    def testeSiteWizard_399(self, flask_username):
        site1 = 'http://menuvivofibra.br'
        site2 = f'http://{self._address_ip}/instalador'
        site3 = 'http://instaladorvivofibra.br'
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('site1 = ' + site1)
        print('site2 = ' + site2)
        print('site3 = ' + site3)
        print('-=-' * 20)
        
        try:
            self._driver.get(site1)
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]')
            for elemento in elementos: print(elemento.text, "\n")
            resultado1 = 'ok'
        except:
            resultado1 = 'falhou'
        print('site1: ', resultado1)
        print('-=-' * 20)
        
        try:
            self._driver.get(site2)
            time.sleep(1)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]')
            for elemento in elementos: print(elemento.text, "\n")
            resultado2 = 'ok'
        except:
            resultado2 = 'falhou'
        print('site2: ', resultado2)
        print('-=-' * 20)

        try:
            self._driver.get(site3)
            time.sleep(1)
            elementos = self._driver.find_elements_by_xpath('/html/body/div/div[1]/table/tbody/tr[1]/td[1]')
            for elemento in elementos: print(elemento.text, "\n")
            resultado3 = 'ok'
        except:
            resultado3 = 'falhou'
        print('site3: ', resultado3)
        print('-=-' * 20)
 
        self._driver.quit()
        if resultado1 == 'ok' and resultado2 == 'ok' and resultado3 == 'ok':
            self._dict_result.update({"obs": "URLs de redirecionamento ok", "result":"passed", "Resultado_Probe": "OK"})
        else:
            self._dict_result.update({"obs": f"Teste incorreto, retorno URLs: {site1}: {resultado1}; {site2}: {resultado2}; {site3}: {resultado3}"})
        return self._dict_result



    def checkBridgeMode_21(self, flask_username):
        try:
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
            time.sleep(1)
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[7]/a').click()
            time.sleep(2)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            time.sleep(2)
            self.admin_authentication_mitraStat()
            time.sleep(1)
            self._driver.switch_to.default_content()
            time.sleep(1)
            self._driver.switch_to.frame('basefrm')
            time.sleep(1)

            config_modowan = [value.text for value in self._driver.find_elements_by_xpath('/html/body/div/div/div[1]/div[3]/form/table/tbody/tr[1]/td[2]//select') ]
            print('2', config_modowan)
            if "Bridge" in config_modowan[0]:
                self._dict_result.update({"obs": f"Modo WAN: {config_modowan}", "result":"passed", "Resultado_Probe": "OK"})
            else:
                self._dict_result.update({"obs": f"Teste incorreto, retorno Modo WAN: {config_modowan}"})

        except NoSuchElementException as exception:
            self._dict_result.update({"obs": str(exception)})

        except Exception as e:
            self._dict_result.update({"obs": str(e)})
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
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            time.sleep(1)
            self._driver.switch_to.frame('header')
            time.sleep(2)
            self._driver.find_element_by_xpath('//*[@id="logoutFrm"]/input').click()
            self._driver.quit()

            self._dict_result.update({"Resultado_Probe": "OK",'result':'passed', "obs": 'Login efetuado com sucesso'})
        except (InvalidSelectorException, NoSuchElementException, NoSuchFrameException) as exception:
            self._dict_result.update({"obs": 'Nao foi possivel realizar o login'})
        finally:
            self._driver.quit()
            return self._dict_result

    def checkPPPoEStatus_146(self, flask_username):
        self._dict_result.update({"obs": "Teste ainda não implementado"})
        return self._dict_result