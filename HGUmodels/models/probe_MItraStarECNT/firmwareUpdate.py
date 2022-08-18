import time
from ..MItraStarECNT import HGU_MItraStarECNT
from HGUmodels.main_session import MainSession
from webdriver.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

session = MainSession()

class HGU_MItraStarECNT_firmwareUpdate(HGU_MItraStarECNT):

    def firmwareUpdate(self, flask_username, firmware_version, reset):
        # print(firmware_version, reset)

        if reset == "Realizar o reset":
            try:
                self._driver.implicitly_wait(5)
                self._driver.get('http://' + self._address_ip + '/')
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('menufrm')
                self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]').click()
                self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Resets"]').click()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                self.login_admin()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                self._driver.find_element_by_xpath('//*[@id="MLG_Resets_Reboot"]').click() # está apenas reinicializando, não fazendo reset de fábrica, basta alterar o botao clicado aqui
                iframe = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                time.sleep(2)
                self._driver.find_element_by_xpath('//*[@id="MLG_Pop_Reboot_Yes"]').click()
                time.sleep(10)
                for t in range (0,20):
                        try:
                            self._driver.get('http://' + self._address_ip + '/')
                            WebDriverWait(self._driver, 10).until(EC.url_to_be(f'http://{self._address_ip}/cgi-bin/sophia_index.cgi'))
                            self._dict_result.update({'Resultado_reset': 'OK'})
                            break
                        except:
                            print(f'tentativa {t}')
                            time.sleep(10)
                            self._driver.refresh()
                        self._dict_result.update({'Resultado_reset': 'NOK'})
                time.sleep(15)
            except Exception as e:
                # print(str(e))
                self._dict_result.update({'Resultado_reset': 'NOK'})

        print("versao:", firmware_version)
        if firmware_version != "Manter atual" and firmware_version != "":  
            time.sleep(5)      
            try:
                self._driver.implicitly_wait(5)
                self._driver.get('http://' + self._address_ip + '/padrao')
                self.login_support()
                self._driver.switch_to.default_content()
                element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="maintenance"]')
                hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
                hover.perform()
                self._driver.find_element_by_xpath('//*[@id="maintenance-firewareUpgrade"]/a').click()
                self._driver.switch_to.frame('mainFrame')
                file = self._driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/ul/li[1]/div[2]/ul[2]/li[2]/input')
                file.send_keys(f'/home/automacao/Projects/firmware/{self._model_name}/{firmware_version}')
                self._driver.find_element_by_xpath('//*[@id="Upload_Id"]').click()
                WebDriverWait(self._driver, 180).until(EC.url_to_be(f'http://{self._address_ip}/cgi-bin/logIn_mhs.cgi'))
                time.sleep(5)
                for t in range (0,30):
                    try:
                        self._driver.find_element_by_xpath('//*[@id="login"]')
                        self._dict_result.update({'Resultado_firmware': f'OK, firmware update realizado com sucesso {firmware_version}'})
                        break
                    except:
                        time.sleep(10)
                        self._driver.refresh()
                    self._dict_result.update({'Resultado_firmware': 'NOK, falha ao reiniciar a HGU, tempo excedido. Verifique se o firmware foi atualizado'})
                time.sleep(5)            
            except Exception as e:
               self._dict_result.update({'Resultado_firmware': f'NOK, falha no update: {e}'})

        # Testes preliminares
        time.sleep(2)
        try: 
            self._driver.implicitly_wait(5)
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            internet = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[3]/td[1]/div').text.split('\n')[1].strip(' ')
            tv = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[13]/td[1]/div/strong').text
            telefone = self._driver.find_element_by_xpath('//*[@id="VOIP"]/td[1]/div[1]').text.split('\n')[1].strip(' ')
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="MLG_Menu_About_Power_Box"]').click()
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            firmware = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[2]/td[2]').text.strip(' ')
            dict_saida = {'internet': internet, 'tv': tv, 'telefone': telefone, 'firmware':  firmware}
            self._dict_result.update({'Resultado_conectividade': dict_saida})
        except Exception as e:
            self._dict_result.update({'Resultado_conectividade': f'Erro no teste: {e}'})
        
        self._driver.quit()
        return self._dict_result  
   
   
        

