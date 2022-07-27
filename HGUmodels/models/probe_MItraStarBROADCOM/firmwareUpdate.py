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
    
    def firmwareUpdate(self, flask_username, firmware_version):
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
                self._dict_result.update({'obs': f'falha no update: verifique o arquivo selecionado'})
            else:
                self._driver.switch_to.default_content()
                self._driver.switch_to.frame('basefrm')
                WebDriverWait(self._driver, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user"]')))
                self._dict_result.update({'obs': f'firmware update realizado com sucesso {firmware_version}'})
        except Exception as e:
            self._dict_result.update({'obs': f'falha no update: {e}'})
        self._driver.quit()
        return self._dict_result


    def firmwareView(self, flask_username):
        try:
            self._driver.implicitly_wait(5)
            self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
            self.login_support()
            self._driver.switch_to.default_content()
            self._driver.switch_to.frame('basefrm')
            firmware_version = self._driver.find_element_by_xpath('/html/body/blockquote/form/b/table/tbody/tr[4]/td[2]').text
            self._dict_result.update({'obs': f'{firmware_version}'})
        except Exception as e:
            self._dict_result.update({'obs': f'falha na verificação: {e}'})
        self._driver.quit()
        return self._dict_result