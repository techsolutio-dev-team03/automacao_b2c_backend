from HGUmodels.factory import HGUModelFactory
from webdriver.webdriver import WebDriver

class firmware:
    def firmware_update_gui(self, ip, username, password, flask_username, model_name, **kwargs):
        print('*'*50)
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "Router advertisement packet", 
                       "Probe#": "178", 
                       "Description": "Verificar nos pacotes Router Advertisement Flag m = 0 e Flag o = 1"}


        hgu = HGUModelFactory.getHGU(probe='firmware',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     driver=driver,
                                     password=password,
                                     dict_result=dict_result)
        return hgu.firmwareUpdate(flask_username)