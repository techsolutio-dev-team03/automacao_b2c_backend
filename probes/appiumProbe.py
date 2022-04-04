import time, datetime
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class appium:
    ### APP APOWERMIRROR
    def __init__(self):
        self.ip = []
        self.username = []
        self.password = []


    def runSpeedTestOokla(self):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('-=-' * 20)
        # teste = {
        #     "deviceName": "OnePlus 7",
        #     "platformName": "android",
        #     "appPackage": "org.zwanoo.android.speedtest",
        #     "appActivity": "com.ookla.mobile4.screens.main.MainActivity",
        #     "noReset": True
        # }

        teste = {
            "deviceName": "Galaxy S10+",
            "platformName": "android",
            "appPackage": "org.zwanoo.android.speedtest",
            "appActivity": "com.ookla.mobile4.screens.main.MainActivity",
            "noReset": True
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', teste)
            time.sleep(3)
            el1 = driver.find_element_by_id("org.zwanoo.android.speedtest:id/go_button")
            el1.click()
            time.sleep(30)
            el2 = driver.find_element_by_xpath('//android.widget.FrameLayout[@content-desc="DOWNLOAD"]/android.view.ViewGroup/android.widget.TextView[3]')
            el3 = driver.find_element_by_xpath('//android.widget.FrameLayout[@content-desc="UPLOAD"]/android.view.ViewGroup/android.widget.TextView[3]')
            el4 = driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Ping"]/android.view.ViewGroup/android.widget.TextView[2]')
            el5 = driver.find_element_by_xpath('//android.view.ViewGroup[@content-desc="Jitter"]/android.view.ViewGroup/android.widget.TextView[2]')
            el6 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[3]/android.view.ViewGroup/android.widget.TextView[2]')

            download = el2.get_attribute('text')
            upload = el3.get_attribute('text')
            ping = el4.get_attribute('text')
            jitter = el5.get_attribute('text')
            perda = el6.get_attribute('text')
            print('Download: ' + download + 'Mbps\n')
            print('Upload: ' + upload + 'Mbps\n')
            print('Ping: ' + ping + '\n')
            print('Jitter: ' + jitter + '\n')
            print('Perda: ' + perda + '\n')
            json_saida = {
                "Resultado":
                    {
                        "Download":download,
                        "Upload":upload,
                        "Ping":ping,
                        "Jitter":jitter,
                        "Perda":perda
                    }
            }
            print(json_saida)
            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "runSpeedTestOokla", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": json_saida}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "runSpeedTestOokla", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "runSpeedTestOokla", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": str(e)}

    def execTurnOn_OffWifi(self, deviceName):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('deviceName = ' + deviceName)
        print('-=-' * 20)
        entrada = {
            "deviceName": deviceName,
            "platformName": "android",
            "appPackage": "com.android.settings",
            "appActivity": ".Settings",
            "noReset": True
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', entrada)
            el1 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.TextView[1]')
            el1.click()
            print('Clicou em conexões... ')
            time.sleep(6)
            el2 = driver.find_element_by_xpath('//android.widget.Switch[@content-desc="Wi-Fi"]') ### DESLIGA OU LIGA WIFI
            el2.click()
            print('Clicou no botão liga/desliga wifi... ')
            result = '200_OK'

            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "execTurnOn_OffWifi", "Probe#": "XXXXXXX", "Description": "Liga ou desliga Wifi via celular", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "execTurnOn_OffWifi", "Probe#": "XXXXXXX", "Description": "Liga ou desliga Wifi via celular", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "execTurnOn_OffWifi", "Probe#": "XXXXXXX", "Description": "Liga ou desliga Wifi via celular", "Resultado": str(e)}

    def execConnectWifi(self, ssid, senhaWifi, deviceName):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ssid = ' + ssid)
        print('senha = ' + senhaWifi)
        print('deviceName = ' + deviceName)
        print('-=-' * 20)
        entrada = {
            "deviceName": deviceName,
            "platformName": "android",
            "appPackage": "com.android.settings",
            "appActivity": ".Settings",
            "noReset": True
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', entrada)
            el1 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.TextView[1]')
            el1.click()
            print('Clicou em Conexões... ')
            time.sleep(6)
            el2 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.TextView')
            el2.click()
            print('Clicou em WiFi... ')
            time.sleep(6)
            el3 = driver.find_element_by_xpath('//*[@text="'+ssid+'"]')
            el3.click()
            print('Procurando Rede escolhida... ')
            time.sleep(2)
            el4 = driver.find_element_by_id('com.android.settings:id/edittext')
            el4.send_keys(senhaWifi)
            print('Autenticando na rede escolhida... ')
            time.sleep(2)
            el5 = driver.find_element_by_id('com.android.settings:id/text_input_end_icon')
            el5.click()
            print('Exibindo senha... ')
            time.sleep(2)
            el6 = driver.find_element_by_id('com.android.settings:id/shared_password_container')
            el6.click()
            print('Clicou em Conectar... ')
            time.sleep(8)
            el7 = driver.find_element_by_xpath('//*[@text="' + ssid + '"]')
            el7.click()
            print('Buscando a rede novamente... ')
            time.sleep(6)
            el = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.TextView[2]').text
            print('Status da conexão: ')
            print(el)
            el8 = driver.find_element_by_id('com.android.settings:id/wifi_details')
            el8.click()
            print('Clicou na engrenagem para mais detalhes... ')
            time.sleep(5)
            el9 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.ImageView')
            el9.click()
            print('Clicou em mais detalhes IP... ')
            el10 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]').text
            print(el10)
            el11 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[2]').text
            print(el11)
            el12 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]').text
            print(el12)
            el13 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[2]').text
            print(el13)
            el14 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView').text
            print(el14)
            el15 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.TextView').text
            print(el15)

            json_saida = {
                "Configurações da Rede":
                    {
                        "Status": el,
                        el10: el11,
                        el12: el13,
                        el14: el15
                    }
            }
            print(json_saida)
            time.sleep(2)

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "execConnectWifi", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": json_saida}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "execConnectWifi", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "execConnectWifi", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": str(e)}

    def execForgetWifi(self, ssid, deviceName):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('ssid = ' + ssid)
        print('deviceName = ' + deviceName)
        print('-=-' * 20)
        entrada = {
            "deviceName": deviceName,
            "platformName": "android",
            "appPackage": "com.android.settings",
            "appActivity": ".Settings",
            "noReset": True
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', entrada)
            el1 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.TextView[1]')
            el1.click()
            print('Clicou em Conexões... ')
            time.sleep(6)
            el2 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.TextView')
            el2.click()
            print('Clicou em WiFi... ')
            time.sleep(6)
            el3 = driver.find_element_by_xpath('//*[@text="' + ssid + '"]')
            el3.click()
            print('Procurando Rede escolhida... ')
            time.sleep(2)
            el8 = driver.find_element_by_id('com.android.settings:id/wifi_details')
            el8.click()
            print('Clicou na engrenagem para mais detalhes... ')
            time.sleep(5)
            el5 = driver.find_element_by_id('com.android.settings:id/forget_button')
            el5.click()
            print('Clicou no botão esquecer rede... ')
            time.sleep(5)
            if driver.find_element_by_id('com.android.settings:id/switch_text'):
                result = '200_OK'
            else:
                result = '400_NOK'

            driver.quit()
            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "execForgetWifi", "Probe#": "XXXXXXX", "Description": "Esquece a rede Wifi conectada via celular", "Resultado": result}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "execForgetWifi", "Probe#": "XXXXXXX", "Description": "Esquece a rede Wifi conectada via celular", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "execForgetWifi", "Probe#": "XXXXXXX", "Description": "Esquece a rede Wifi conectada via celular", "Resultado": str(e)}

    def checkDeviceInfo(self, deviceName):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('deviceName = ' + deviceName)
        print('-=-' * 20)
        entrada = {
            "deviceName": deviceName,
            "platformName": "android",
            "appPackage": "com.android.settings",
            "appActivity": ".Settings",
            "noReset": True
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', entrada)
            m1 = TouchAction(driver).press(x=480, y=2125).move_to(x=480, y=170).release().perform()
            print('Arrastou pra cima #1 ... ')
            time.sleep(1)
            m1 = TouchAction(driver).press(x=450, y=2000).move_to(x=450, y=180).release().perform()
            print('Arrastou pra cima #2 ... ')
            time.sleep(1)
            m3 = TouchAction(driver).press(x=460, y=2100).move_to(x=460, y=160).release().perform()
            print('Arrastou pra cima #3 ... ')
            time.sleep(2)
            el1 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[8]/android.widget.RelativeLayout/android.widget.TextView[1]')
            el1.click()
            print('Clicou em Sobre o dispositivo... ')
            time.sleep(6)
            el2 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.TextView')
            el2.click()
            print('Clicou em informações de Status... ')
            time.sleep(6)
            el3 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView[1]').text
            print(el3)
            el4 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView[2]').text
            print(el4)
            el5 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[5]/android.widget.RelativeLayout/android.widget.TextView[1]').text
            print(el5)
            el6 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[5]/android.widget.RelativeLayout/android.widget.TextView[2]').text
            print(el6)

            json_saida = {
                "Informações do Dispositivo":
                    {
                        el3:el4,
                        el5:el6
                    }
            }


            # el3 = driver.find_element_by_xpath(
            #     '')
            # el3.click()
            # print('Linha #3')
            # time.sleep(6)





            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "checkDeviceInfo", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": json_saida}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkDeviceInfo", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkDeviceInfo", "Probe#": "XXXXXXX", "Description": "Executa teste de velocidade Ookla via celular", "Resultado": str(e)}

    def checkWifiStatus(self, deviceName, ssid):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('deviceName = ' + deviceName)
        print('ssid = ' + ssid)
        print('-=-' * 20)
        entrada = {
            "deviceName": deviceName,
            "platformName": "android",
            "appPackage": "com.android.settings",
            "appActivity": ".Settings",
            "noReset": True
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', entrada)
            el1 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.TextView[1]')
            el1.click()
            print('Clicou em Conexões... ')
            time.sleep(6)
            el2 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android.widget.TextView')
            el2.click()
            print('Clicou em WiFi... ')
            time.sleep(6)
            el3 = driver.find_element_by_xpath('//*[@text="' + ssid + '"]')
            el3.click()
            print('Procurando Rede escolhida... ')
            time.sleep(2)
            el = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.TextView[2]').text
            print('Status da conexão: ')
            print(el)
            el8 = driver.find_element_by_id('com.android.settings:id/wifi_details')
            el8.click()
            print('Clicou na engrenagem para mais detalhes... ')
            time.sleep(2)
            el9 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.ImageView')
            el9.click()
            print('Clicou em mais detalhes IP... ')
            el10 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]').text
            print(el10)
            el11 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[2]').text
            print(el11)
            el12 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]').text
            print(el12)
            el13 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[2]').text
            print(el13)
            el14 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView').text
            print(el14)
            el15 = driver.find_element_by_xpath(
                '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/android.widget.LinearLayout[3]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.LinearLayout/android.widget.TextView').text
            print(el15)

            json_saida = {
                "Configurações da Rede":
                    {
                        "Status": el,
                        el10: el11,
                        el12: el13,
                        el14: el15
                    }
            }
            print(json_saida)
            time.sleep(2)


            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": json_saida}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": str(e)}

    def execAndroidWebNavigation(self, deviceName, site):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('deviceName = ' + deviceName)
        print('site = ' + site)
        print('-=-' * 20)
        entrada = {
            "deviceName": deviceName,
            "platformName": "android",
            'browserName': 'Chrome'
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', entrada)
            # if OperationalSystem == 'Windows':
            #     PATH = 'Setup/Selenium/chromedriver.exe'
            # else:
            #     PATH = 'Setup/Selenium/chromedriver'

            driver.get("http://www.google.com")

            timings = driver.execute_script('return performance.timing')
            print(timings)



            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": "json_saida"}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": str(e)}

    def execVoIPCall(self, deviceName, callNumber):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('deviceName = ' + deviceName)
        print('callNumber = ' + str(callNumber))
        print('-=-' * 20)
        entrada = {
            "deviceName": deviceName,
            "platformName": "android",
            "appPackage": "com.grandstream.wave",
            "appActivity": "com.softphone.HomeActivity",
            "noReset": True
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', entrada)
            # if OperationalSystem == 'Windows':
            #     PATH = 'Setup/Selenium/chromedriver.exe'
            # else:
            #     PATH = 'Setup/Selenium/chromedriver'

            # dig_1 = driver.find_element_by_id('com.grandstream.wave:id/Digit1')
            # dig_2 = driver.find_element_by_id('com.grandstream.wave:id/Digit2')
            # dig_3 = driver.find_element_by_id('com.grandstream.wave:id/Digit3')
            # dig_4 = driver.find_element_by_id('com.grandstream.wave:id/Digit4')
            # dig_5 = driver.find_element_by_id('com.grandstream.wave:id/Digit5')
            # dig_6 = driver.find_element_by_id('com.grandstream.wave:id/Digit6')
            # dig_7 = driver.find_element_by_id('com.grandstream.wave:id/Digit7')
            # dig_8 = driver.find_element_by_id('com.grandstream.wave:id/Digit8')
            # dig_9 = driver.find_element_by_id('com.grandstream.wave:id/Digit9')
            # dig_0 = driver.find_element_by_id('com.grandstream.wave:id/Digit0')
            # dial = driver.find_element_by_id('com.grandstream.wave:id/dial_btn_text')

            ### LONG PRESS ###
            # actions = TouchAction(driver)
            # actions.long_press(element)
            # actions.perform()

            for digit in callNumber:
                teste = driver.find_element_by_id('com.grandstream.wave:id/Digit'+digit+'').click()
                print('Clicando no dígito ' + str(digit))

            calling = driver.find_element_by_id('com.grandstream.wave:id/Adress').text
            print('Discando para ' + str(calling))
            time.sleep(1)
            dial = driver.find_element_by_id('com.grandstream.wave:id/dial_btn_text').click()
            print('Ligando... ')


            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": "json_saida"}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": str(e)}

    def execVoIPReceive(self, deviceName):
        print()
        print()
        print('-=-' * 20)
        print('\t\t --- INICIANDO ROBO AUTOMAÇÃO ---')
        print('-=-' * 20)
        print('\n\n -- PARAMETROS DE ENTRADA --')
        print('deviceName = ' + deviceName)
        print('-=-' * 20)
        entrada = {
            "deviceName": deviceName,
            "platformName": "android",
            "appPackage": "com.grandstream.wave",
            "appActivity": "com.softphone.HomeActivity",
            "noReset": True
        }

        try:
            driver = webdriver.Remote('http://localhost:4723/wd/hub', entrada)
            # if OperationalSystem == 'Windows':
            #     PATH = 'Setup/Selenium/chromedriver.exe'
            # else:
            #     PATH = 'Setup/Selenium/chromedriver'

            # dig_1 = driver.find_element_by_id('com.grandstream.wave:id/Digit1')
            # dig_2 = driver.find_element_by_id('com.grandstream.wave:id/Digit2')
            # dig_3 = driver.find_element_by_id('com.grandstream.wave:id/Digit3')
            # dig_4 = driver.find_element_by_id('com.grandstream.wave:id/Digit4')
            # dig_5 = driver.find_element_by_id('com.grandstream.wave:id/Digit5')
            # dig_6 = driver.find_element_by_id('com.grandstream.wave:id/Digit6')
            # dig_7 = driver.find_element_by_id('com.grandstream.wave:id/Digit7')
            # dig_8 = driver.find_element_by_id('com.grandstream.wave:id/Digit8')
            # dig_9 = driver.find_element_by_id('com.grandstream.wave:id/Digit9')
            # dig_0 = driver.find_element_by_id('com.grandstream.wave:id/Digit0')
            # dial = driver.find_element_by_id('com.grandstream.wave:id/dial_btn_text')

            ### LONG PRESS ###
            # actions = TouchAction(driver)
            # actions.long_press(element)
            # actions.perform()

            ### ATENDER ###
            # com.grandstream.wave:id/accept

            print('Aguardando ligação ... ')
            time.sleep(3)
            wait = WebDriverWait(driver, 20 * 60)
            element = wait.until(EC.element_to_be_clickable((By.ID, "com.grandstream.wave:id/accept")))
            time.sleep(3)
            element.click()
            print('Ligação atendida com SUCESSO! ')


            return {"Resultado_Probe": "OK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": "json_saida"}
        except NoSuchElementException as exception:
            print(exception)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": str(exception)}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "appium", "ProbeName": "checkWifiStatus", "Probe#": "XXXXXXX", "Description": "Verifica informações da rede wifi conectada", "Resultado": str(e)}