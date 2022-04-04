from ..interface import HGUModelInterface
import time

class HGU_AskeyECNT(HGUModelInterface):

    def login_support(self):
        user_input = self._driver.find_element_by_id('txtUser')
        user_input.send_keys(self._username)
        pass_input = self._driver.find_element_by_id('txtPass')
        pass_input.send_keys(self._password)
        login_button = self._driver.find_element_by_id('btnLogin')
        login_button.click()
        time.sleep(3)


