from HGUmodels.factory import HGUModelFactory
from webdriver.webdriver import WebDriver


class Ipv6:

    #172
    def ipv6_wan_enabled(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "ipv6 wan enabled", 
                       "Probe#": "172", 
                       "Description": "Acessar páginas com WAN Dual Stack e DHCPv6 Stateless"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        url_list = ['https://ipv6.google.com/', 
                    'https://www.v6.facebook.com/', 
                    'http://v6.testmyipv6.com', 
                #    'http://ipv6.onet.pl', 
                    'http://www.cofone.eu/']

        return hgu.ipv6_wan_enabled(flask_username, url_list, 'IPv4&IPv6(Dual Stack)', dhcpv6 = True)


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


    #190
    def accessCaixa(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "accessCaixa", 
                       "Probe#": "190", 
                       "Description": "Acessar página da Caixa com IPv4 e DHCPv6 Desabilitado"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        test_url = 'http://www.caixa.gov.br'

        return hgu.ipv_x_url_test(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


    #191
    def accessSantander(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "accessSantander", 
                       "Probe#": "191", 
                       "Description": "Acessar página do Santander com IPv4 e DHCPv6 Desabilitado"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        test_url = 'http://www.santander.com.br'

        return hgu.ipv_x_url_test(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


    #192
    def accessVivo(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "accessVivo", 
                       "Probe#": "192", 
                       "Description": "Acessar página da Vivo com IPv4 e DHCPv6 Desabilitado"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        test_url = 'http://www.vivo.com.br'

        return hgu.ipv_x_url_test(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


    #193
    def connectSkype(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()
        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "connectSkype", 
                       "Probe#": "193", 
                       "Description": "Utilizar o Skype"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        return hgu.connectSkype_193(flask_username, 'IPv4 Only', dhcpv6 = False)


   #195
    def accessIpv6Test(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "accessIpv6Test", 
                       "Probe#": "195", 
                       "Description": "Nao acessar página ipv6-test com IPv4 e DHCPv6 Desabilitado"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        test_url = 'https://ipv6.test-ipv6.com'

        return hgu.ipv_x_url_test_not(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


   #196
    def accessV6Test(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "accessV6Test", 
                       "Probe#": "196", 
                       "Description": "Nao acessar página testmyipv6 com IPv4 e DHCPv6 Desabilitado"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        test_url = 'http://v6.testmyipv6.com'

        return hgu.ipv_x_url_test_not(flask_username, test_url, 'IPv4 Only', dhcpv6 = False)


    # 203
    def ipv4ExecIperf(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "ipv4_exec_iperf", 
                       "Probe#": "203", 
                       "Description": "Teste iperf IPv4 de PC para servidor publico"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        iperf_server = 'iperf.he.net'

        return hgu.ipv4ExecIperf_203(flask_username, iperf_server, 'IPv4 Only', dhcpv6 = False)


   # 212
    def ipv4DownloadCentOS(self, ip, username, password, flask_username, model_name, **kwargs): ### TUDO OK
        driver = WebDriver.get_driver()

        dict_result = {'result':'failed', 
                       'obs':None, 
                       "Resultado_Probe": "NOK", 
                       "ControllerName": "ipv6", 
                       "ProbeName": "ipv4DownloadCentOS", 
                       "Probe#": "ipv4DownloadCentOS", 
                       "Description": "Download do CentOS em IPv4"}

        hgu = HGUModelFactory.getHGU(probe='ipv6Probe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     driver=driver, 
                                     dict_result=dict_result)

        print(hgu)
        iperf_server = 'iperf.he.net'

        return hgu.ipv4DownloadCentOS_212(flask_username, iperf_server, 'IPv4 Only', dhcpv6 = False)