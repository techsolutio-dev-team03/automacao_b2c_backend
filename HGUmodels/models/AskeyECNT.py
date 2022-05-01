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


    def ipv6_only_setting(self):
        self._driver.get('http://' + self._address_ip + '/padrao')
        self.login_support()
        time.sleep(3)
        self._driver.switch_to.frame('menuFrm')
        self._driver.find_element_by_xpath('/html/body/div[2]/div/fieldset/div[2]/a').click()
        time.sleep(1)
        self._driver.switch_to.default_content()
        self._driver.switch_to.frame('mainFrm')
        self._driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
        time.sleep(2)
        self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[2]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click()
        time.sleep(2)
          

    def ipv4_ipv6_setting(self):
        self._driver.find_element_by_xpath('//*[@id="WanIPIntfList"]/table/tbody/tr[1]/td[2]/a').click()
        time.sleep(2)
        self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/fieldset[4]/div[1]/input[1]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="WanIPIntfSettingForm"]/div[2]/input[2]').click()
        time.sleep(2)


    def __str__(self):
        return "HGU_AskeyECNT"


