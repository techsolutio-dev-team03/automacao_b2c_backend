import time
from ..interface import HGUModelInterface
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.select import Select

class HGU_MItraStarECNT(HGUModelInterface):

    def login_support(self):
        time.sleep(2)
        user_input = self._driver.find_element_by_id('Loginuser')
        user_input.send_keys(self._username)
        time.sleep(1)
        pass_input = self._driver.find_element_by_id('LoginPassword')
        pass_input.send_keys(self._password)
        time.sleep(1)
        login_button = self._driver.find_element_by_id('Login_ID')
        login_button.click()
        time.sleep(1)
    
    def login_admin(self):
        time.sleep(2)
        user_input = self._driver.find_element_by_id('Loginuser')
        user_input.send_keys(self._username)
        time.sleep(1)
        pass_input = self._driver.find_element_by_id('LoginPassword')
        pass_input.send_keys(self._password)
        time.sleep(1)
        login_button = self._driver.find_element_by_id('Login_ID')
        login_button.click()
        time.sleep(1)

    def open_change_password_mitraStar(self):
        time.sleep(10)
        self._driver.switch_to.frame("menufrm")
        link = self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]')
        link.click()
        time.sleep(1)
        link = self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Account_Settings"]')
        link.click()
        time.sleep(1)

    def admin_authentication_mitraStat(self):
        self._driver.switch_to.default_content()
        time.sleep(1)
        self._driver.switch_to.frame("basefrm")
        user_input = self._driver.find_element_by_xpath('//*[@id="Loginuser"]')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_xpath('//*[@id="LoginPassword"]')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
        time.sleep(1)
        login_button.click()
        time.sleep(1)


    def ipv6_only_setting(self):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
        hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
        hover.perform()
        self._driver.find_element_by_xpath('//*[@id="network-broadband"]/a').click()
        time.sleep(5)
        self._driver.switch_to.frame('mainFrame')
        self._driver.find_element_by_xpath('//*[@id="editBtn"]').click()
        time.sleep(2)
        self._driver.switch_to.default_content()
        Select(self._driver.find_element_by_xpath('//*[@id="ipVerRadio_Text"]')).select_by_visible_text('IPv6 Only')
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[2]').click()
        time.sleep(5)
          

    def ipv4_ipv6_setting(self):
        self._driver.switch_to.frame('mainFrame')
        self._driver.find_element_by_xpath('//*[@id="editBtn"]').click()
        time.sleep(2)
        self._driver.switch_to.default_content()
        Select(self._driver.find_element_by_xpath('//*[@id="ipVerRadio_Text"]')).select_by_visible_text('IPv6/IPv4 Dual Stack')
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[2]').click()
        time.sleep(5)

    def __str__(self):
        return "HGU_MItraStarECNT"

