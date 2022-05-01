import time
from ..interface import HGUModelInterface
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.select import Select



class HGU_MItraStarBROADCOM(HGUModelInterface):

    def login_support(self):
        time.sleep(2)
        user_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/form/div[3]/input[2]')
        user_input.send_keys(self._username)
        time.sleep(1)
        pass_input = self._driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/form/div[3]/input[3]')
        pass_input.send_keys(self._password)
        time.sleep(1)
        login_button = self._driver.find_element_by_xpath('/html/body/div[2]/div/div/div[3]/form/div[3]/input[4]')
        login_button.click()
        time.sleep(5)

    # def open_change_password_mitraStar(self):
    #     time.sleep(10)
    #     self._driver.switch_to.frame("menufrm")
    #     link = self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Management"]')
    #     link.click()
    #     time.sleep(1)
    #     link = self._driver.find_element_by_xpath('//*[@id="MLG_Menu_Account_Settings"]')
    #     link.click()
    #     time.sleep(1)

    def admin_authentication_mitraStat(self):
        time.sleep(5)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame("basefrm")
        time.sleep(1)
        user_input = self._driver.find_element_by_xpath('//*[@id="user"]')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_xpath('//*[@id="pass"]')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_xpath('//*[@id="acceptLogin"]/span')
        time.sleep(1)
        login_button.click()
        time.sleep(1)


    def ipv6_only_setting(self):
        self._driver.get('http://' + self._address_ip + '/padrao_adv.html')
        self.login_support()
        time.sleep(10)
        self._driver.switch_to.frame('menufrm')
        self._driver.find_element_by_xpath('//*[@id="folder10"]/table/tbody/tr/td/a/span').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="item14"]/table/tbody/tr/td/a').click()
        time.sleep(2)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('basefrm')
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/table/tbody/tr[4]/td[16]/input').click()
        time.sleep(2)
        # wan_network = self._driver.find_element_by_xpath('//*[@id="enblv6Info"]/table/tbody/tr/td[1]').text
        Select(self._driver.find_element_by_xpath('//*[@id="IpProtocalMode"]')).select_by_visible_text('IPv6 Only')
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(2)
        

    def ipv4_ipv6_setting(self):
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/table/tbody/tr[4]/td[16]/input').click()
        time.sleep(1)
        Select(self._driver.find_element_by_xpath('//*[@id="IpProtocalMode"]')).select_by_visible_text('IPv4&IPv6(Dual Stack)')
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('/html/body/blockquote/form/center/input[2]').click()
        time.sleep(2)


    def __str__(self):
        return f"HGU_MItraStarBROADCOM {self._address_ip}"


              

