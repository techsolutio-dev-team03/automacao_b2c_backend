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
    
    def firmwareUpdate(self, flask_username, firmware_version):
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
            element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="maintenance"]')
            hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
            hover.perform()
            self._driver.find_element_by_xpath('//*[@id="maintenance-firewareUpgrade"]/a').click()
            self._driver.switch_to.frame('mainFrame')
            firmware_version = self._driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/ul/li[1]/div[2]/ul[1]/li/font').text
            self._dict_result.update({'obs': f'{firmware_version}'})
        except Exception as e:
            self._dict_result.update({'obs': f'falha na verificação: {e}'})
        self._driver.quit()
        return self._dict_result