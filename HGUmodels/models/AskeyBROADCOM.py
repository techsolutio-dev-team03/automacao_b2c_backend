import time
from ..interface import HGUModelInterface

class HGU_AskeyBROADCOM(HGUModelInterface):
    
    def login_support(self):
        self._driver.switch_to.frame('mainFrame')
        time.sleep(2)
        user_input = self._driver.find_element_by_xpath('//*[@id="txtUser"]')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_xpath('//*[@id="txtPass"]')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_xpath('//*[@id="btnLogin"]')
        time.sleep(2)
        login_button.click()
        time.sleep(1)


    def login_admin(self):
        self._driver.switch_to.frame('mainFrame')
        time.sleep(2)
        user_input = self._driver.find_element_by_xpath('//*[@id="txtUser"]')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_xpath('//*[@id="txtPass"]')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_xpath('//*[@id="btnLogin"]')
        time.sleep(2)
        login_button.click()
        time.sleep(1)