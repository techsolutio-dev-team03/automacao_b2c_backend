import time
from ..AskeyBROADCOM import HGU_AskeyBROADCOM
from HGUmodels.main_session import MainSession
from webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

session = MainSession()

class HGU_AskeyBROADCOM_firmwareUpdate(HGU_AskeyBROADCOM):
    
    def firmwareUpdate(self, flask_username, firmware_version):
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
                self._dict_result.update({'obs': f'falha no update: verifique o arquivo selecionado'})
            else:
                WebDriverWait(self._driver, 180).until(EC.url_to_be(f'http://{self._address_ip}/main.html'))
                time.sleep(5)
                for t in range (0,30):
                    try:
                        self._driver.get('http://' + self._address_ip + '/main.html')
                        self._dict_result.update({'obs': f'firmware update realizado com sucesso {firmware_version}'})
                        break
                    except:
                        time.sleep(10)
                        self._driver.refresh()
                    self._dict_result.update({'obs': f'falha ao reiniciar a HGU, tempo excedido. Verifique se o firmware foi atualizado'})
                time.sleep(5)  
        except Exception as e:
            self._dict_result.update({'obs': f'falha no update: {e}'})
        self._driver.quit()
        return self._dict_result


    def firmwareView(self, flask_username):
        try:
            self._driver.implicitly_wait(5)
            self._driver.get('http://' + self._address_ip + '/padrao')
            self.login_support()
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            firmware_version = self._driver.find_element_by_xpath('/html/body/blockquote/form/b/table/tbody/tr[4]/td[2]').text
            self._dict_result.update({'obs': f'{firmware_version}'})
        except Exception as e:
            self._dict_result.update({'obs': f'falha na verificação: {e}'})
        self._driver.quit()
        return self._dict_result