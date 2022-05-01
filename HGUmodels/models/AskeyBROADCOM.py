import time
from ..interface import HGUModelInterface
from selenium.webdriver.support.select import Select

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


    def ipv6_only_setting(self):
        self._driver.get('http://' + self._address_ip + '/padrao')
        time.sleep(5)
        self.login_support()
        time.sleep(5)
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a').click()
        time.sleep(2)
        self._driver.find_element_by_xpath('//*[@id="item14"]/table/tbody/tr/td/a').click()
        time.sleep(2)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/table/tbody/tr[5]/td[15]/input').click()
        time.sleep(2)
        Select(self._driver.find_element_by_xpath('//*[@id="IpProtocolMode"]')).select_by_visible_text('IPv6 Only')
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(2)
        

    def ipv4_ipv6_setting(self):
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/table/tbody/tr[5]/td[15]/input').click()
        time.sleep(1)
        Select(self._driver.find_element_by_xpath('//*[@id="IpProtocolMode"]')).select_by_visible_text('IPv4&IPv6(Dual Stack)')
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(2)



    def __str__(self):
        return "HGU_AskeyBROADCOM"

