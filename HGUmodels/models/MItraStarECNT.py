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
        user_input.send_keys('admin')
        time.sleep(1)
        pass_input = self._driver.find_element_by_id('LoginPassword')
        pass_input.send_keys(self._password)
        time.sleep(1)
        login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]')
        login_button.click()
        time.sleep(2)

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


    def ipv_x_setting(self, ipv_x):
        if ipv_x == 'IPv4&IPv6(Dual Stack)': ipv_x = 'IPv6/IPv4 Dual Stack'
        self._driver.switch_to.default_content()
        element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
        hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
        hover.perform()
        time.sleep(2)
        self._driver.find_element_by_id('network-broadband').click()
        time.sleep(6)
        self._driver.switch_to.frame('mainFrame')
        self._driver.find_element_by_xpath('//*[@id="editBtn"]').click()
        time.sleep(3)
        self._driver.switch_to.default_content()
        Select(self._driver.find_element_by_xpath('//*[@id="ipVerRadio_Text"]')).select_by_visible_text(ipv_x)
        time.sleep(2)
        # SLAAC
        if ipv_x == 'IPv6/IPv4 Dual Stack': self._driver.find_element_by_xpath('//*[@id="Pppv6Dynamic_DHCP"]/ul/li[2]/input[2]').click()
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[2]').click()
        time.sleep(10)

          
    def dhcp_v6(self, dhcpv6_state):
        self._driver.switch_to.default_content()
        element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
        hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
        hover.perform()
        time.sleep(1)
        self._driver.find_element_by_id('network-homeNetworking').click()
        time.sleep(3)
        self._driver.switch_to.frame('mainFrame')
        self._driver.find_element_by_xpath(' //*[@id="t4"]/span').click()
        time.sleep(6)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('mainFrame')
        if dhcpv6_state:
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[5]/div[2]/ul/li[2]/input[2]').click()
        else:
            self._driver.find_element_by_xpath('/html/body/div[2]/div/form/div/div[2]/ul/li[5]/div[2]/ul/li[2]/input[1]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="Apply_ID"]').click()
        time.sleep(10)


    def dhcp_stateless(self):
        self._driver.switch_to.default_content()
        element_to_hover_over = self._driver.find_element_by_xpath('//*[@id="network"]/span[1]')
        hover = ActionChains(self._driver).move_to_element(element_to_hover_over)
        hover.perform()
        time.sleep(1)
        self._driver.find_element_by_id('network-homeNetworking').click()
        time.sleep(3)
        self._driver.switch_to.frame('mainFrame')
        self._driver.find_element_by_xpath(' //*[@id="t4"]/span').click()
        time.sleep(6)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('mainFrame')
        #TODO verificar qual o campo que teve ser configurado com estado stateless
        #self._driver.find_element_by_xpath('').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="Apply_ID"]').click()
        time.sleep(10)

    def __str__(self):
        return "HGU_MItraStarECNT"

