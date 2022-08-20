import time
from ..AskeyBROADCOM import HGU_AskeyBROADCOM
from HGUmodels.main_session import MainSession
from webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

session = MainSession()

class HGU_AskeyBROADCOM_firmwareUpdate(HGU_AskeyBROADCOM):
 
    def firmwareUpdate(self, flask_username, firmware_version, reset):
        print(firmware_version, reset)

        if reset == "Realizar o reset":
            try:
                self._driver.implicitly_wait(5)
                self._driver.get('http://' + self._address_ip + '/')
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('mainFrame')
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/a').click()
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[3]/a').click()
                # self._driver.switch_to.default_content()
                # self._driver.switch_to.frame('mainFrame')
                self.login_admin()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('mainFrame')
                self._driver.find_element_by_xpath('//*[@id="btn-clicktocall"]/span').click() # está apenas reinicializando, não fazendo reset de fábrica, basta alterar o botao clicado aqui
                iframe = self._driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/iframe')
                self._driver.switch_to.frame(iframe)
                time.sleep(2)
                self._driver.find_element_by_xpath('//*[@id="btnaAccept"]/span').click()
                time.sleep(10)
                for t in range (0,25):
                        print(t)
                        try:
                            self._driver.get('http://' + self._address_ip + '/')
                            time.sleep(1)
                            # self._driver.switch_to.default_content()
                            # self._driver.switch_to.frame('mainFrame')
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
            time.sleep(5)


        print("versao:", firmware_version)
        if firmware_version != "Manter atual" and firmware_version != "":  
            time.sleep(10)
            try:
                self._driver.implicitly_wait(5)
                self._driver.get('http://' + self._address_ip + '/padrao')
                self.login_support()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('menufrm')
                self._driver.find_element_by_xpath('//*[@id="folder66"]/table/tbody/tr/td/a').click()
                self._driver.find_element_by_xpath('//*[@id="folder80"]/table/tbody/tr/td/a').click()
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                file = self._driver.find_element_by_xpath('/html/body/blockquote/form/table/tbody/tr/td[2]/input')
                file.send_keys(f'/home/automacao/Projects/firmware/{self._model_name}/{firmware_version}')
                self._driver.find_element_by_xpath('//*[@id="cmdUpload"]').click()
                WebDriverWait(self._driver, 180).until(EC.presence_of_element_located((By.XPATH, '/html/body/blockquote')))
                resultado = self._driver.find_element_by_xpath('/html/body/blockquote').text
                print(resultado)
                if 'Image uploading failed. The selected file contains an illegal image.' in resultado:
                    self._dict_result.update({'Resultado_firmware': f'NOK, falha no update: verifique o arquivo selecionado'})   
                else:
                    WebDriverWait(self._driver, 180).until(EC.url_to_be(f'http://{self._address_ip}/main.html'))
                    time.sleep(5)
                    for t in range (0,30):
                        try:
                            self._driver.get('http://' + self._address_ip + '/main.html')
                            self._dict_result.update({'Resultado_firmware': f'OK, firmware update realizado com sucesso {firmware_version}'})
                            break
                        except:
                            time.sleep(10)
                            self._driver.refresh()
                        self._dict_result.update({'Resultado_firmware': f'NOK, falha ao reiniciar a HGU, tempo excedido. Verifique se o firmware foi atualizado'})
                    time.sleep(5)  
            except Exception as e:
                self._dict_result.update({'Resultado_firmware': f'NOK, falha no update: {e}'})  
            time.sleep(5)

        # Testes preliminares
        try: 
            self._driver.implicitly_wait(5)
            self._driver.get('http://' + self._address_ip + '/')
            time.sleep(3)
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[1]/a').click()
            internet = self._driver.find_element_by_xpath('//*[@id="divPpp"]').text.split('\n')[1].strip(' ')
            tv = self._driver.find_element_by_xpath('//*[@id="divVod"]/strong').text
            telefone = self._driver.find_element_by_xpath('//*[@id="divTelStatus"]').text.split('\n')[1].strip(' ')
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrame')
            self._driver.find_element_by_xpath('//*[@id="accordion"]/li[4]/a').click()
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('mainFrame')
            firmware = self._driver.find_element_by_xpath('//*[@id="table_model"]/tbody/tr[2]/td[2]').text.strip(' ')
            dict_saida = {'internet': internet, 'tv': tv, 'telefone': telefone, 'firmware':  firmware}
            self._dict_result.update({'Resultado_conectividade': dict_saida})
        except Exception as e:
            self._dict_result.update({'Resultado_conectividade': f'Erro no teste: {e}'})
        time.sleep(5)

        self._driver.quit()
        return self._dict_result  

