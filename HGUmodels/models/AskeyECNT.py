from ..interface import HGUModelInterface
import time


class HGU_AskeyECNT(HGUModelInterface):

    def login_support(self):
        user_input = self._driver.find_element_by_id('txtUser')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_id('txtPass')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_id('btnLogin')
        time.sleep(1)

        login_button.click()
        time.sleep(3)


    def login_admin(self):
        time.sleep(2)
        user_input = self._driver.find_element_by_id('txtUser')
        user_input.send_keys('admin')
        time.sleep(1)
        pass_input = self._driver.find_element_by_id('txtPass')
        pass_input.send_keys(self._password)
        time.sleep(1)
        login_button = self._driver.find_element_by_id('btnLogin')
        login_button.click()
        time.sleep(1)


    def ipv_x_setting(self, ipv_x):
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menuFrm')
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('mainFrm')
        self._driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
        time.sleep(2)
        if ipv_x == 'IPv4 Only': self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[3]').click()
        if ipv_x == 'IPv6 Only': self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[2]').click()
        if ipv_x == 'IPv4&IPv6(Dual Stack)': 
            self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[1]').click()
            # Seleciona modo SLAAC:
            self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[3]/input[1]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click()
        time.sleep(3)
          

    def dhcp_v6(self, dhcpv6_state):
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menuFrm')
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[3]').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('mainFrm')
        if dhcpv6_state == True: self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[2]').click()
        if dhcpv6_state == False: self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[1]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="btnIPv6"]').click()
        time.sleep(3)


    def dhcp_stateless(self):
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menuFrm')
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[1]/a[3]').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('mainFrm')
        self._driver.find_element_by_xpath('//*[@id="IPv6Form"]/fieldset[2]/div[1]/input[2]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="btnIPv6"]').click()
        time.sleep(3)

    def __str__(self):
        return "HGU_AskeyECNT"


