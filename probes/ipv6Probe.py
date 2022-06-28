from HGUmodels.factory import HGUModelFactory
from webdriver.webdriver import WebDriver
from appium import webdriver
# import unittest
# from appium.webdriver.common.appiumby import AppiumBy


class Ipv6:

    # #172
    # def ipv6_wan_enabled(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
    #     driver = WebDriver.get_driver()

    #     dict_result = {'result':'failed', 
    #                    'obs':None, 
    #                    "Resultado_Probe": "NOK", 
    #                    "ControllerName": "ipv6", 
    #                    "ProbeName": "ipv6 wan enabled", 
    #                    "Probe#": "172", 
    #                    "Description": "Acessar páginas com WAN Dual Stack e DHCPv6 Stateless"}

    #     hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
    #                                  address_ip=ip, 
    #                                  model_name=model_name, 
    #                                  username=username, 
    #                                  password=password, 
    #                                  driver=driver, 
    #                                  dict_result=dict_result)

    #     print(hgu)
    #     url_list = ['https://ipv6.google.com/', 
    #                 'https://www.v6.facebook.com/', 
    #                 'http://v6.testmyipv6.com', 
    #             #    'http://ipv6.onet.pl', 
    #                 'http://www.cofone.eu/']

    #     return hgu.ipv6_wan_enabled(flask_username, url_list, 'IPv4&IPv6(Dual Stack)', dhcpv6 = True)


    #178
    def icmpv6_router_advt_flag_m_o(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "Router advertisement packet", 
                       "Probe#": "178", 
                       "Description": "Verificar nos pacotes Router Advertisement Flag m = 0 e Flag o = 1"}

        hgu = HGUModelFactory.getHGU(probe='wireSharkProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)


        return hgu.icmpv6_router_advt_flag_m_o(flask_username)


 #184
    def dhcpv6_dhclient_no_avail(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "Capturar as mensagens DHCPv6", 
                       "Probe#": "184", 
                       "Description": "Captura as mensagens de DHCPv6: o HGU deve responder status code NoAddrAvail (2)"}

        hgu = HGUModelFactory.getHGU(probe='wireSharkProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)


        return hgu.dhcpv6_dhclient_no_avail(flask_username)


 #185
    def router_solicitation(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "Mensagens de Router Solicitation na Lan", 
                       "Probe#": "185", 
                       "Description": "Mensagens de Router Solicitation na Lan"}

        hgu = HGUModelFactory.getHGU(probe='wireSharkProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)


        return hgu.router_solicitation(flask_username)

    #190 - Fora do escopo
    # def accessCaixa(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
    #     driver = WebDriver.get_driver()

    #     dict_result = {'result':'failed', 
    #                    'obs':None, 
    #                    "Resultado_Probe": "NOK", 
    #                    "ControllerName": "ipv6", 
    #                    "ProbeName": "accessCaixa", 
    #                    "Probe#": "190", 
    #                    "Description": "Acessar página da Caixa com IPv4 e DHCPv6 Desabilitado"}

    #     hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
    #                                  address_ip=ip, 
    #                                  model_name=model_name, 
    #                                  username=username, 
    #                                  password=password, 
    #                                  driver=driver, 
    #                                  dict_result=dict_result)

    #     print(hgu)
    #     test_url = 'http://www.caixa.gov.br'

    #     return hgu.ipv_x_url_test(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


    # 191 - Fora do escopo
    # def accessSantander(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
    #     driver = WebDriver.get_driver()

    #     dict_result = {'result':'failed', 
    #                    'obs':None, 
    #                    "Resultado_Probe": "NOK", 
    #                    "ControllerName": "ipv6", 
    #                    "ProbeName": "accessSantander", 
    #                    "Probe#": "191", 
    #                    "Description": "Acessar página do Santander com IPv4 e DHCPv6 Desabilitado"}

    #     hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
    #                                  address_ip=ip, 
    #                                  model_name=model_name, 
    #                                  username=username, 
    #                                  password=password, 
    #                                  driver=driver, 
    #                                  dict_result=dict_result)

    #     print(hgu)
    #     test_url = 'http://www.santander.com.br'

    #     return hgu.ipv_x_url_test(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


    #192 - Fora do escopo
    # def accessVivo(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
    #     driver = WebDriver.get_driver()

    #     dict_result = {'result':'failed', 
    #                    'obs':None, 
    #                    "Resultado_Probe": "NOK", 
    #                    "ControllerName": "ipv6", 
    #                    "ProbeName": "accessVivo", 
    #                    "Probe#": "192", 
    #                    "Description": "Acessar página da Vivo com IPv4 e DHCPv6 Desabilitado"}

    #     hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
    #                                  address_ip=ip, 
    #                                  model_name=model_name, 
    #                                  username=username, 
    #                                  password=password, 
    #                                  driver=driver, 
    #                                  dict_result=dict_result)

    #     print(hgu)
    #     test_url = 'http://www.vivo.com.br'

    #     return hgu.ipv_x_url_test(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


#    #195 - Fora do escopo
#     def accessIpv6Test(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
#         driver = WebDriver.get_driver()

#         dict_result = {'result':'failed', 
#                        'obs':None, 
#                        "Resultado_Probe": "NOK", 
#                        "ControllerName": "ipv6", 
#                        "ProbeName": "accessIpv6Test", 
#                        "Probe#": "195", 
#                        "Description": "Nao acessar página ipv6-test com IPv4 e DHCPv6 Desabilitado"}

#         hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
#                                      address_ip=ip, 
#                                      model_name=model_name, 
#                                      username=username, 
#                                      password=password, 
#                                      driver=driver, 
#                                      dict_result=dict_result)

#         print(hgu)
#         test_url = 'https://ipv6.test-ipv6.com'

#         return hgu.ipv_x_url_test_not(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


#    #196 - Fora do escopo
#     def accessV6Test(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
#         driver = WebDriver.get_driver()

#         dict_result = {'result':'failed', 
#                        'obs':None, 
#                        "Resultado_Probe": "NOK", 
#                        "ControllerName": "ipv6", 
#                        "ProbeName": "accessV6Test", 
#                        "Probe#": "196", 
#                        "Description": "Nao acessar página testmyipv6 com IPv4 e DHCPv6 Desabilitado"}

#         hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
#                                      address_ip=ip, 
#                                      model_name=model_name, 
#                                      username=username, 
#                                      password=password, 
#                                      driver=driver, 
#                                      dict_result=dict_result)

#         print(hgu)
#         test_url = 'http://v6.testmyipv6.com'

#         return hgu.ipv_x_url_test_not(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


#     # 203
#     def ipv4ExecIperf(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
#         driver = WebDriver.get_driver()

#         dict_result = {'result':'failed', 
#                        'obs':None, 
#                        "Resultado_Probe": "NOK", 
#                        "ControllerName": "ipv6", 
#                        "ProbeName": "ipv4_exec_iperf", 
#                        "Probe#": "203", 
#                        "Description": "Teste iperf IPv4 de PC para servidor publico"}

#         hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
#                                      address_ip=ip, 
#                                      model_name=model_name, 
#                                      username=username, 
#                                      password=password, 
#                                      driver=driver, 
#                                      dict_result=dict_result)

#         print(hgu)
#         iperf_server = 'iperf.he.net'

#         return hgu.ipv4ExecIperf_203(flask_username, iperf_server, 'IPv4 Only', dhcpv6 = False)


   # 212
    def ipv4DownloadCentOS(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "ipv4DownloadCentOS", 
                       "Probe#": "212A", 
                       "Description": "Download do CentOS em IPv4"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        return hgu.ipv4DownloadCentOS_212(flask_username, 'IPv4 Only', dhcpv6 = False)


    # 218 
    def connectSkype(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "connectSkype", 
                       "Probe#": "218", 
                       "Description": "Utilizar o Skype"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        return hgu.connectSkype_218(flask_username, 'IPv4&IPv6(Dual Stack)', dhcpv6 = True)


    # 230 
    def iPerf2PCsClientServer(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "iPerf2PCsServerClient", 
                       "Probe#": "230", 
                       "Description": "IPerf entre 2 PCs: PC1: Server, PC2: Client WiFi"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        return hgu.iPerf2PCsClientServer_230(flask_username, 'IPv4&IPv6(Dual Stack)', dhcpv6 = True)


   # 231 
    def iPerf2PCsServerClient(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "iPerf2PCsServerClient", 
                       "Probe#": "230", 
                       "Description": "IPerf entre 2 PCs: PC1: Server, PC2: Client WiFi"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        return hgu.iPerf2PCsServerClient_231(flask_username, 'IPv4&IPv6(Dual Stack)', dhcpv6 = True)


    # 255 
    def iPerf2PCsClientServerIpv6(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "iPerf2PCsServerClientIpv6", 
                       "Probe#": "255", 
                       "Description": "IPerf entre 2 PCs: PC1: Server, PC2: Client WiFi. IPv6"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        return hgu.iPerf2PCsClientServerIpv6_255(flask_username, 'IPv6 Only', dhcpv6 = True)


   # 256
    def iPerf2PCsServerClientIpv6(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "iPerf2PCsServerClientIpv6", 
                       "Probe#": "256", 
                       "Description": "IPerf entre 2 PCs: PC1: Server, PC2: Client WiFi. IPv6"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        return hgu.iPerf2PCsServerClientIpv6_256(flask_username, 'IPv6 Only', dhcpv6 = True)


    # def teste_android(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO NOK
    #     from appium import webdriver
    #     from appium.webdriver.common.mobileby import MobileBy
    #     from selenium.webdriver.support.ui import WebDriverWait
    #     from selenium.webdriver.support import expected_conditions as EC
    #     import time

    #     desired_caps = {
    #         "deviceName": "Nexus 7",
    #         "platformName": "Android",
    #         "version" : "7.1",
    #         "app": "https://testingbot.com/appium/sample.apk"
    #     }

    #     driver = webdriver.Remote("http://1e7eaf1bb807bbe6712c24897a6c997c:bb9109cd931e7be68e00d4761189418d@hub.testingbot.com/wd/hub", desired_caps)

    #     inputA = WebDriverWait(driver, 30).until(
    #         EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, "inputA"))
    #     )
    #     inputA.send_keys("10")

    #     inputB = WebDriverWait(driver, 30).until(
    #         EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, "inputB"))
    #     )
    #     inputB.send_keys("5")

    #     sum = WebDriverWait(driver, 30).until(
    #         EC.element_to_be_clickable((MobileBy.ACCESSIBILITY_ID, "sum"))
    #     )

    #     if sum!=None and sum.text=="15":
    #         assert True
    #     else:
    #         assert False

    #     driver.quit()