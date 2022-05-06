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


    def ipv_x_setting(self, ipv_x):
        self._driver.switch_to.default_content()
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
        Select(self._driver.find_element_by_xpath('//*[@id="IpProtocolMode"]')).select_by_visible_text(ipv_x)
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(5)
        

    def dhcp_v6(self, dhcpv6_state):
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a').click()
        time.sleep(2)
        self._driver.find_element_by_xpath('//*[@id="folder15"]/table/tbody/tr/td/a').click()
        time.sleep(2)
        self._driver.find_element_by_xpath('//*[@id="item17"]/table/tbody/tr/td/a').click()
        time.sleep(2)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        checkbox = self._driver.find_element_by_xpath('/html/body/blockquote/form/table[2]/tbody/tr/td[1]/input')
        if checkbox.get_attribute('checked') and not dhcpv6_state:
            checkbox.click()
        if not checkbox.get_attribute('checked') and dhcpv6_state:
            checkbox.click()
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input').click()
        time.sleep(5)



    def __str__(self):
        return "HGU_AskeyBROADCOM"

