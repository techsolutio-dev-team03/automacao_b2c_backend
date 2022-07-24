import time
from ..MItraStarECNT import HGU_MItraStarECNT
from HGUmodels.main_session import MainSession
from webdriver.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains 

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
            time.sleep(10)
            self._dict_result.update({'obs': f'firmware update realizado com sucesso {firmware_version}'})
        except Exception as e:
            self._dict_result.update({'obs': f'falha no update: {e}'})
        self._driver.quit()
        return self._dict_result