import time
from ..MItraStarBROADCOM import HGU_MItraStarBROADCOM
from HGUmodels.main_session import MainSession
from webdriver.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

session = MainSession()

class HGU_MItraStarBROADCOM_firmwareUpdate(HGU_MItraStarBROADCOM):
    
     def firmwareUpdate(self, flask_username, firmware_version, reset):
        # print(firmware_version, reset)

        if reset == "Realizar o reset":
            try:
                self._driver.implicitly_wait(5)
                self._driver.get('http://' + self._address_ip + '/')
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('menufrm')
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[3]/a').click()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                self.login_admin()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                self._driver.find_element_by_xpath('//*[@id="btn-clicktocall"]/span').click() # está apenas reinicializando, não fazendo reset de fábrica, basta alterar o botao clicado aqui
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                time.sleep(2)
                self._driver.find_element_by_xpath('//*[@id="btnReset"]').click()
                time.sleep(10)
                for t in range (0,25):
                        print(t)
                        try:
                            self._driver.get('http://' + self._address_ip + '/')
                            time.sleep(1)
                            # self._driver.switch_to.default_content()
                            # self._driver.switch_to.frame('basefrm')
                            # WebDriverWait(self._driver, 20).until(EC.presence_of_element_located(By.XPATH, '//*[@id="status"]/tbody/tr[3]/th/span'))
                            self._dict_result.update({'Resultado_reset': 'OK'})
                            break
                        except Exception as e:
                            print(str(e))
                            time.sleep(10)
                            # self._driver.refresh()
                        self._dict_result.update({'Resultado_reset': 'NOK'})
            except Exception as e:
                # print(str(e))
                self._dict_result.update({'Resultado_reset': 'NOK'})
            time.sleep(45)

        print("versao:", firmware_version)
        if firmware_version != "Manter atual" and firmware_version != "":  
            time.sleep(5)
            try:
                self._driver.implicitly_wait(5)
                self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
                self.login_support()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('menufrm')
                self._driver.find_element_by_xpath('//*[@id="folder70"]/table/tbody/tr/td/a/span').click()
                self._driver.find_element_by_xpath('//*[@id="folder84"]/table/tbody/tr/td/a/span').click()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                file = self._driver.find_element_by_xpath('/html/body/blockquote/form/table/tbody/tr/td[2]/input')
                file.send_keys(f'/home/automacao/Projects/firmware/{self._model_name}/{firmware_version}')
                self._driver.find_element_by_xpath('/html/body/blockquote/form/p/input').click()
                WebDriverWait(self._driver, 210).until(EC.presence_of_element_located((By.XPATH, '/html/body/blockquote')))
                resultado = self._driver.find_element_by_xpath('/html/body/blockquote').text
                print(resultado)
                if 'La subida del archivo ha fallado. El archivo seleccionado contiene una imagen ilegal.' in resultado:
                    self._dict_result.update({'Resultado_firmware': f'NOK, falha no update: verifique o arquivo selecionado'})   
                else:
                    WebDriverWait(self._driver, 300).until(EC.url_to_be(f'http://{self._address_ip}/login.html'))
                    self._dict_result.update({'Resultado_firmware': f'OK, firmware update realizado com sucesso {firmware_version}'})
            except Exception as e:
                self._dict_result.update({'Resultado_firmware': f'NOK, falha no update: {e}'})   
            time.sleep(45)
                
        # Testes preliminares
        
        try: 
            self._driver.implicitly_wait(5)
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            internet = self._driver.find_element_by_xpath('//*[@id="wan"]').text.split('\n')[1].strip(' ')
            tv = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[13]/td[1]/div/strong').text
            telefone = self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[15]/td[1]/div[1]').text.split('\n')[1].strip(' ')
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('menufrm')
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[4]/a').click()
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            firmware = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[2]/td[2]').text.strip(' ')
            dict_saida = {'internet': internet, 'tv': tv, 'telefone': telefone, 'firmware':  firmware}
            self._dict_result.update({'Resultado_conectividade': dict_saida})
        except Exception as e:
            self._dict_result.update({'Resultado_conectividade': f'Erro no teste: {e}'})
        
        self._driver.quit()
        return self._dict_result  
 

