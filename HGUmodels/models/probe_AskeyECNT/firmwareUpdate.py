import time
from ..AskeyECNT import HGU_AskeyECNT
from HGUmodels.main_session import MainSession
from webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

session = MainSession()

class HGU_AskeyECNT_firmwareUpdate(HGU_AskeyECNT):
    
    def firmwareUpdate(self, flask_username, firmware_version, reset):
        # print(firmware_version, reset)

        if reset == "Realizar o reset":
            try:
                self._driver.implicitly_wait(5)
                self._driver.get('http://' + self._address_ip + '/')
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[3]/a').click()
                self.login_admin()
                self._driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/a/span').click() 
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                time.sleep(2)
                self._driver.find_element_by_xpath('//*[@id="btnaAccept"]/span').click()
                time.sleep(1)
                for t in range (0,40):
                        try:
                            self._driver.get('http://' + self._address_ip + '/')
                            self._dict_result.update({'Resultado_reset': 'OK'})
                            break
                        except:
                            time.sleep(10)
                            self._driver.refresh()
                        self._dict_result.update({'Resultado_reset': 'NOK'})
            except Exception as e:
                # print(str(e))
                self._dict_result.update({'Resultado_reset': 'NOK'})

        print("versao:", firmware_version)
        if firmware_version != "Manter atual" and firmware_version != "":  
            time.sleep(2)      
            try:
                self._driver.implicitly_wait(5)
                self._driver.get('http://' + self._address_ip + '/padrao')
                self.login_support()
                self._driver.switch_to.frame('menuFrm')
                self._driver.find_element_by_xpath('/html/body/div[5]/div/fieldset/div[3]/a').click()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('mainFrm')
                file = self._driver.find_element_by_xpath('//*[@id="fileUpgradeByHTTP"]')
                file.send_keys(f'/home/automacao/Projects/firmware/{self._model_name}/{firmware_version}')
                self._driver.find_element_by_xpath('//*[@id="btnUpgradeByHTTP"]').click()
                WebDriverWait(self._driver, 180).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/fieldset/p[1]/em')))
                resultado = self._driver.find_element_by_xpath('/html/body/div/fieldset/p[1]/em').text
                print(resultado)
                if resultado == 'failure':
                    self._dict_result.update({'obs': f'falha no update: verifique o arquivo selecionado'})
                elif resultado == 'success':
                    time.sleep(5)
                    for t in range (0,21):
                        try:
                            self._driver.get('http://' + self._address_ip + '/padrao')
                            self._dict_result.update({'Resultado_firmware': f'OK, firmware update realizado com sucesso {firmware_version}'})
                            break
                        except:
                            time.sleep(10)
                            self._driver.refresh()
                        self._dict_result.update({'Resultado_firmware': 'NOK, falha ao reiniciar a HGU, tempo excedido. Verifique se o firmware foi atualizado'})
                    time.sleep(5)     
                    self._dict_result.update({'Resultado_firmware': f'OK, firmware update realizado com sucesso {firmware_version}'})
                else:
                    self._dict_result.update({'Resultado_firmware': f'NOK, falha no update'})
            except Exception as e:
                self._dict_result.update({'Resultado_firmware': f'NOK, falha no update: {e}'})

        # Testes preliminares
        time.sleep(2)
        try: 
            self._driver.implicitly_wait(5)
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(1)
            internet = self._driver.find_element_by_xpath('//*[@id="divPpp"]').text.split('\n')[1].strip(' ')
            tv = self._driver.find_element_by_xpath('//*[@id="divVod"]/strong').text
            telefone = self._driver.find_element_by_xpath('//*[@id="divTelStatus"]').text.split('\n')[1].strip(' ')
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[4]/a').click()
            firmware = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[2]/td[2]').text.strip(' ')
            dict_saida = {'internet': internet, 'tv': tv, 'telefone': telefone, 'firmware':  firmware}
            self._dict_result.update({'Resultado_conectividade': dict_saida})

        except Exception as e:
            self._dict_result.update({'Resultado_conectividade': f'Erro no teste: {e}'})
        
        self._driver.quit()
        return self._dict_result