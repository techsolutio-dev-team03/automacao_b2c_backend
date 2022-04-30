import time
from ..interface import HGUModelInterface

class HGU_AskeyBROADCOM(HGUModelInterface):
    
    def login_support(self):
        self._driver.switch_to.frame('loginfrm')
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
        self.check_before_login()
        time.sleep(2)
        user_input = self._driver.find_element_by_xpath('//*[@id="txtUser"]')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_xpath('//*[@id="txtPass"]')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_xpath('//*[@id="btnLogin"]')
        time.sleep(2)
        login_button.click()
        time.sleep(1)


    def check_before_login(self):
        try:
            if self._driver.find_element_by_xpath('//*[@id="status"]/tbody/tr[1]/th/span').text == 'GPON':
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/a').click()
                time.sleep(1)
                self._driver.find_element_by_xpath('//*[@id="accordion"]/li[2]/ul/li[1]/a').click()
        except:
            pass


    def __str__(self):
        return "HGU_AskeyBROADCOM"

