from HGUmodels.factory import HGUModelFactory
from webdriver.webdriver import WebDriver

class firmware:
    def firmware_update_gui(self, ip, username, password, flask_username, model_name, firmware_version, reset_req, **kwargs):
        driver = WebDriver.get_driver()

        dict_result = {'Resultado_reset':'Reset não realizado', 
                       'Resultado_firmware':'Alteração de firmware não realizada', 
                       "Resultado_conectividade":{}
                       }

        hgu = HGUModelFactory.getHGU(probe='firmware',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     driver=driver,
                                     password=password,
                                     dict_result=dict_result)
        
        return hgu.firmwareUpdate(flask_username, firmware_version, reset_req)