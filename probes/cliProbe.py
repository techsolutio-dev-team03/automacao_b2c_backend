import paramiko
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException
from paramiko.ssh_exception import SSHException
import sys
import time
import socket
import requests
import re
import hashlib
import pybase64
from HGUmodels.factory import HGUModelFactory

class ErrorTimerLock(Exception):
    pass

class cli:

    def reboot(self, ip_hgu, user, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {ip_hgu} \n{'#' * 50}")
            ssh.connect(hostname=ip_hgu, username=user, password=password, timeout=2)
            teste = ssh.invoke_shell()
            teste.send('sh\n')
            time.sleep(2)
            teste.send('cd /\n')
            time.sleep(2)
            teste.send('reboot /\n')
            time.sleep(2)
            output = teste.recv(65000)
            #print(output.decode())
            #print('teste')
            print("Authentication successfuly, connect to HGU")
            return {"Resultado_Probe": "OK", "ControllerName": "cli", "ProbeName": "reboot", "Probe#": "48",
                    "Description": "Executar reboot via ssh", "Resultado": "200_OK"}
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "reboot", "Probe#": "48",
                    "Description": "Executar reboot via ssh", "Resultado": "Falha_Autenticacao"}
        except socket.timeout:
            print("Unable to establish SSH connection: Timeout de conexão")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "reboot", "Probe#": "48",
                    "Description": "Executar reboot via ssh", "Resultado": "Timeout_Connection"}
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "reboot", "Probe#": "48",
                    "Description": "Executar reboot via ssh", "Resultado": str(sshException)}
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "reboot", "Probe#": "48",
                    "Description": "Executar reboot via ssh", "Resultado": str(badHostKeyException)}
        finally:
            ssh.close()


    #409
    def ntpServer(self, ip, username, password, flask_username, model_name, **kwargs):


        dict_result = {
            'result':'failed', 
            'obs': None, 
            "Resultado_Probe": "NOK", 
            "ControllerName": "cli", 
            "ProbeName": "ntpServer", 
            "Probe#": "48", 
            "Description": "Verificar server NTP"}
            

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.NTPServer_409()


###
    def getAuthUserName(self, ip_hgu, user, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {ip_hgu} \n{'#' * 50}")
            ssh.connect(hostname=ip_hgu, username=user, password=password, timeout=2)
            teste = ssh.invoke_shell()
            teste.send('rg\n')
            time.sleep(2)
            teste.send('voice \n')
            time.sleep(2)
            teste.send('show \n')
            time.sleep(2)
            output = teste.recv(65000)
            out_str = output.decode('utf-8')
            str_list = out_str.splitlines()
            print(str_list)
            for key in str_list:
                print(key)
                if key.startswith('AuthUserName'):
                    fields = key.split(' ')
                    authUsername = fields[2]

            print("Authentication successfuly, connect to HGU")
            return {"Resultado_Probe": "OK", "ControllerName": "cli", "ProbeName": "sipNumber", "Probe#": "xxx",
                    "Description": "Verificar sipNumber", "Resultado": authUsername}
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "sipNumber", "Probe#": "xxx",
                    "Description": "Verificar sipNumber", "Resultado": "Falha_Autenticacao"}
        except socket.timeout:
            print("Unable to establish SSH connection: Timeout de conexão")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "sipNumber", "Probe#": "xxx",
                    "Description": "Verificar sipNumber", "Resultado": "Timeout_Connection"}
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "sipNumber", "Probe#": "xxx",
                    "Description": "Verificar sipNumber", "Resultado": str(sshException)}
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "ntpServer", "Probe#": "xxx",
                    "Description": "Verificar sipNumber", "Resultado": str(badHostKeyException)}
        finally:
            ssh.close()

    #410
    def timeZone(self, ip, username, password, flask_username, model_name, **kwargs):

        dict_result = {
            'result':'failed', 
            'obs': None, 
            "Resultado_Probe": "NOK", 
            "ControllerName": "cli", 
            "ProbeName": "timeZone", 
            "Probe#": "48", 
            "Description": "Verificar Time Zone"}

        hgu = HGUModelFactory.getHGU(probe='settingsProbe',
                                     address_ip=ip, 
                                     model_name=model_name, 
                                     username=username, 
                                     password=password, 
                                     dict_result=dict_result)
        return hgu.timeZone_410()


    def connectSsh(self, ip_hgu, user, password):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {ip_hgu} \n{'#' * 50}")
            ssh.connect(hostname=ip_hgu, username=user, password=password, timeout=2)
            teste = ssh.invoke_shell()
            #print(output.decode())
            #print('teste')
            time.sleep(5)
            print("Authentication successfuly, connect to HGU")
            return {"Resultado_Probe": "OK", "ControllerName": "cli", "ProbeName": "ssh", "Probe#": "48",
                    "Description": "Estabelecer uma sessão SSH", "Resultado": "200_OK"}
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "ssh", "Probe#": "48",
                    "Description": "Estabelecer uma sessão SSH", "Resultado": "Falha_Autenticacao"}
        except socket.timeout:
            print("Unable to establish SSH connection: Timeout de conexão")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "ssh", "Probe#": "48",
                    "Description": "Estabelecer uma sessão SSH", "Resultado": "Timeout_Connection"}
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "ssh", "Probe#": "48",
                    "Description": "Estabelecer uma sessão SSH", "Resultado": str(sshException)}
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "ssh", "Probe#": "48",
                    "Description": "Estabelecer uma sessão SSH", "Resultado": str(badHostKeyException)}
        finally:
            ssh.close()

###
    def execWget(self, ip_hgu, user, password, url):
        try:
            result = 'NOK'
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {ip_hgu} \n{'#' * 50}")
            ssh.connect(hostname=ip_hgu, username=user, password=password, timeout=2)
            teste = ssh.invoke_shell()
            teste.send('sh\n')
            time.sleep(2)
            teste.send('wget ' + url + ' /\n')
            time.sleep(2)
            output = teste.recv(65000)
            output_str = output.decode('utf-8')
            ans = output_str.splitlines()
            for i in ans:
                print(i)
                if i == '~ # wget ' + url + ' /':
                    result = '200_OK'
            print("Authentication successfuly, connect to HGU")
            return {"Resultado_Probe": "OK", "ControllerName": "cli", "ProbeName": "wget", "Probe#": "48",
                    "Description": "Executar wget cli", "Resultado": result}
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "wget", "Probe#": "48",
                    "Description": "Executar wget cli", "Resultado": "Falha_Autenticacao"}
        except socket.timeout:
            print("Unable to establish SSH connection: Timeout de conexão")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "wget", "Probe#": "48",
                    "Description": "Executar wget cli", "Resultado": "Timeout_Connection"}
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "wget", "Probe#": "48",
                    "Description": "EExecutar wget cli", "Resultado": str(sshException)}
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "reboot", "Probe#": "48",
                    "Description": "Executar wget cli", "Resultado": str(badHostKeyException)}
        finally:
            ssh.close()

###
    def execWput(self, ip_hgu, user, password, url):
        try:
            result = 'NOK'
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"\n{'#' * 50}\nConectando ao Dispositivo {ip_hgu} \n{'#' * 50}")
            ssh.connect(hostname=ip_hgu, username=user, password=password, timeout=2)
            teste = ssh.invoke_shell()
            teste.send('sh\n')
            time.sleep(2)
            teste.send('wput ' + url + ' /\n')
            time.sleep(2)
            output = teste.recv(65000)
            output_str = output.decode('utf-8')
            ans = output_str.splitlines()
            for i in ans:
                print(i)
                if i == '/bin/sh: wput: not found':
                    result = '200_OK'
            print("Authentication successfuly, connect to HGU")
            return {"Resultado_Probe": "OK", "ControllerName": "cli", "ProbeName": "wput", "Probe#": "48",
                    "Description": "Executar wget cli", "Resultado": result}
        except AuthenticationException:
            print("Authentication failed, please verify your credentials: %s")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "wput", "Probe#": "48",
                    "Description": "Executar wget cli", "Resultado": "Falha_Autenticacao"}
        except socket.timeout:
            print("Unable to establish SSH connection: Timeout de conexão")
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "wput", "Probe#": "48",
                    "Description": "Executar wget cli", "Resultado": "Timeout_Connection"}
        except SSHException as sshException:
            print("Unable to establish SSH connection: %s" % sshException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "wput", "Probe#": "48",
                    "Description": "EExecutar wget cli", "Resultado": str(sshException)}
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)
            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "ProbeName": "reboot", "Probe#": "48",
                    "Description": "Executar wget cli", "Resultado": str(badHostKeyException)}
        finally:
            ssh.close()

    def execHGUHTTPGetFiltrar(self, ip_hgu, user, passw, pagina, filtro):
        # composicao das URLs abaixo para Mitra GPT-2541GNAC-N1.
        cookie = False

        try:
            url_padrao = 'http://' + ip_hgu + '/padrao'
            url_sid = 'http://' + ip_hgu + '/padrao_adv.html'
            url_auth = 'http://' + ip_hgu + '/login-padrao.cgi'
            url_busca = 'http://' + ip_hgu + '/'+pagina
            url_logout = 'http://' + ip_hgu + '/logout.cmd'

            session = requests.Session()
            #print("0 - passou")

            ret = session.get(url_padrao)
            #print("1 - " + ret.content.decode())
            if (ret.content.decode().find("timerlock.html") >= 0):
                raise ErrorTimerLock

            ret = session.get(url_sid)
            #print("2 - " + ret.content.decode())
            if (ret.content.decode().find("timerlock.html") >= 0):
                raise ErrorTimerLock

            sid = self.procuraVal('var sid += +\"(.+?)\"', ret.content.decode())
            #print("3 - sid:"+sid)

            passwd = sid + ':' + passw
            #print("4 - url_sid:" + passwd)

            new_passwd = hashlib.md5(bytes(passwd, encoding='utf8')).hexdigest()
            string = user + ':' + new_passwd
            #print("5 - string:" + string)

            encodedData = pybase64.b64encode(str.encode(string))
            #print("6 - encondedData:" + str(encodedData))

            payload = {'sessionKey': encodedData, 'user': '', 'pass': ''}
            session.post(url_auth, data=payload)
            cookie = session.cookies
            # print("7 - url_auth:" + url_auth + " payload:" + str(payload) + " cookies:" + str(cookie))

            ret = session.post(url_busca, data=payload)
            #print("8 - url_busca" + " " + ret.content.decode())

            if (ret.content.decode().find("timerlock.html") >= 0):
                raise ErrorTimerLock

            Resposta = self.procuraVal(filtro, ret.content.decode())

            if (Resposta):
                if cookie:
                    session.get(url_logout, cookies=cookie)

                return {"Resultado_Probe": "OK", "ControllerName": "cli", "Resposta": Resposta, "filtro": filtro, "ProbeName": "execHGUHTTPGetFiltrar", "Probe#": "XX",
                    "Description": "Executar get na pagina do HGU e filtrar inforcao desejada.", "Resultado": "200_OK"}
            else:
                Resposta=ret.content.decode()

                if cookie:
                    session.get(url_logout, cookies=cookie)

                return {"Resultado_Probe": "NOK", "ControllerName": "cli", "Resposta": Resposta, "filtro": filtro, "ProbeName": "execHGUHTTPGetFiltrar", "Probe#": "XX",
                    "Description": "Executar get na pagina do HGU e filtrar inforcao desejada.", "Resultado": "Informacao nao encontrada."}

        except ErrorTimerLock:
            url_timer = "http://" + ip_hgu + "/timerlock.html"
            ret = session.get(url_timer)
            Resposta = self.procuraVal("var authFailRemain += +'(.+?)'\r\n", ret.content.decode())
            Resposta = "Erro de autenticação. Tentar novamente em " + str(Resposta) + " segundos."

            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "Resposta": Resposta, "ProbeName": "execHGUHTTPGetFiltrar",
                "Probe#": "XX", "Description": "Executar get na pagina do HGU e filtrar inforcao desejada.", "Resultado": "Erro ao se conectar no HGU."}

        except:
            if cookie:
                session.get(url_logout, cookies=cookie)

            return {"Resultado_Probe": "NOK", "ControllerName": "cli", "Resposta": Resposta, "ProbeName": "execHGUHTTPGetFiltrar",
                "Probe#": "XX", "Description": "Executar get na pagina do HGU e filtrar inforcao desejada.", "Resultado": "Ocorreu erro na filtragem da informacao."}

    def procuraVal(self, procurar, texto):
        retorno = re.search(procurar, texto)

        if retorno:
            retorno = retorno.group(1)
            return retorno.strip()

        return False;