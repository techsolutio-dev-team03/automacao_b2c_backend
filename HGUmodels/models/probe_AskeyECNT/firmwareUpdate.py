import time
from ..AskeyECNT import HGU_AskeyECNT
from HGUmodels.main_session import MainSession
from webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
                        self._dict_result.update({'obs': f'firmware update realizado com sucesso {firmware_version}'})
                        break
                    except:
                        time.sleep(10)
                        self._driver.refresh()
                    self._dict_result.update({'obs': f'falha ao reiniciar a HGU, tempo excedido. Verifique se o firmware foi atualizado'})
                time.sleep(5)     
                self._dict_result.update({'obs': f'firmware update realizado com sucesso {firmware_version}'})
            else:
                self._dict_result.update({'obs': f'falha no update'})
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
            self._driver.switch_to.frame('mainFrm')
            firmware_version = self._driver.find_element_by_xpath('//*[@id="td_SWVer"]').text
            self._dict_result.update({'obs': f'{firmware_version}'})
        except Exception as e:
            self._dict_result.update({'obs': f'falha na verificação: {e}'})
        self._driver.quit()
        return self._dict_result