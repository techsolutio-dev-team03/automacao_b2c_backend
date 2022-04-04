import requests



BASE = "http://127.0.0.1:5000/"

parametros_Entrada = {
                            "ip":"192.168.15.1",
                            "username":"admin",
                            "password":"mvo8gfm9"
                        }
passo1 = requests.post(BASE + "api/v1/gui/logoutWizard",json=parametros_Entrada)
print(passo1.text)
passo1 = passo1.json()
print()
print(passo1)