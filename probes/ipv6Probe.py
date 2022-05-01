from HGUmodels.factory import HGUModelFactory
from webdriver.webdriver import WebDriver


class Ipv6:

    #210
    def accessSantander(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "gui", 
                       "ProbeName": "accessSantander", 
                       "Probe#": "210", 
                       "Description": "Acessar página do Santander"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        test_url = 'http://www.santander.com.br'

        return hgu.ipv6_only_url_test(flask_username, test_url)