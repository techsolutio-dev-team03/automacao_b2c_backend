import time
from ..AskeyECNT import HGU_AskeyECNT
from HGUmodels.main_session import MainSession
from webdriver.webdriver import WebDriver

session = MainSession()

class HGU_AskeyECNT_firmwareUpdate(HGU_AskeyECNT):
    
    def firmwareUpdate(self, flask_username, firmware_version):
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
            time.sleep(10)
            self._dict_result.update({'obs': f'firmware update realizado com sucesso {firmware_version}'})
        except Exception as e:
            self._dict_result.update({'obs': f'falha no update: {e}'})
        self._driver.quit()
        return self._dict_result