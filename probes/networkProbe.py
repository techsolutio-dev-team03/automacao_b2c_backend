""" import requests
import sys
import time
import os
import nmcli
import paramiko
from pythonping import ping
from paramiko_expect import SSHClientInteraction
import iperf3
from flask import jsonify, request
from probes import iptvProbe

class network:

###
    def ping(self, ip_hgu):
        try:
            execute_ping = ping(ip_hgu, count=1, timeout=1, verbose=True)
            status_ping = execute_ping.success()
            if status_ping:
                print("Ping executado com sucesso!!")
            else:
                print("Falha ao executar ping!!")
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "ping", "Probe#": "48",
                    "Description": "Executar ping via servidor", "Resultado": status_ping}
        except Exception as e:
            print(e)
            return {"Resultado_Probe": "NOK", "ControllerName": "network", "ProbeName": "ping", "Probe#": "48",
                    "Description": "Executar ping via servidor", "Resultado": "ERROR"}


####
    def downloadFile(self):
        try:
            url = 'http://201.95.254.137/download/300'
            diretorio = '/home/hulrich/PycharmProjects/pytest-html-reporter/cpe-data'
            localFilename = url.split('/')[-1]
            r = requests.get(url, stream=True)
            #
            start = time.time()

            f = open(diretorio + '/' +localFilename, 'wb')
            #
            for chunk in r.iter_content(chunk_size=512 * 1024):
                 if chunk:
                     f.write(chunk)
                     f.flush()
                     os.fsync(f.fileno())
            f.close()
            #
            tempo = time.time() - start
            file_stats = os.stat(diretorio + '/' +localFilename)
            tamanho = file_stats.st_size / (1024 * 1024)
            taxa = (tamanho / tempo) * 8

            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "downloadFile", "Probe#": "XX",
                     "Description": "Executar download Axyros", "Resultado": taxa}

        except Exception as e:
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "downloadFile", "Probe#": "XX",
                     "Description": "Executar download Axyros", "Resultado": e}

####
    def listConnections(self):
    # Exibe os SSIDs armazenado para conexão Wifi
        try:
            list = nmcli.connection()
            return{"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "listConnections", "Probe#": "XX",
             "Description": "Verificar redes conhecidas", "Resultado": list}

        except Exception as e:
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "listConnections", "Probe#": "XX",
                    "Description": "Verificar redes conhecidas", "Resultado": "NOK"}

####
    def deleteConnection(self, ssid):
    # Delta o SSID solicitado
        try:
            list = nmcli.connection.delete(ssid)
            return{"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "listConnections", "Probe#": "XX",
             "Description": "Deletar redes conhecidas", "Resultado": "200_OK"}

        except Exception as e:
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "listConnections", "Probe#": "XX",
                    "Description": "Deletar redes conhecidas", "Resultado": "NOK"}


####
    def execConnection(self, ssid, password):
    # Conectar em um SSID especifico
        try:
            conn = nmcli.device.wifi_connect(ssid, password)
            return{"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "New Connection", "Probe#": "XX",
             "Description": "Conectar rede nova", "Resultado": "200_OK"}

        except Exception as e:
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "New Connection", "Probe#": "XX",
                    "Description": "Conectar rede nova", "Resultado": "FALHA_AUTENTICACAO"}

####
    def deviceShow(self, iface):
    # Infomrações da conexão da placa de rede
        try:
            show = nmcli.device.show(iface)
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "Show Connection",
                    "Probe#": "XX",
                    "Description": "Conectar rede nova", "Resultado": show}

        except Exception as e:
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "Show Connection",
                    "Probe#": "XX",
                    "Description": "Conectar rede nova", "Resultado": "ERROR"}


####
    def listAPs(self):
    # Scan dos APs disponível mostrando infomrações deles
        try:
            list = nmcli.device.wifi()
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "Show APS",
                    "Probe#": "XX",
                    "Description": "Verificar redes disponiveis", "Resultado": list}

        except Exception as e:
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "Show APS",
                    "Probe#": "XX",
                    "Description": "erificar redes disponiveis", "Resultado": "ERROR"}

####
    def portMirrorHPE(self, ip_switch, usuario, senha, porta_origem, porta_destino, acao):
        # habilita espelhamento de porta no switch HPE 1920S
        # Parametro:
        #  acao = ativa ou desativa

        #######
        # Login
        conn = paramiko.SSHClient()
        conn.load_system_host_keys()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            conn.connect(hostname=ip_switch, username=usuario, password=senha)
        except:
            return {"Resultado_Probe": "NOK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha,
                    "porta_origem": porta_origem, "porta_destino": porta_destino, "acao": acao,
                    "ControllerName": "network", "ProbeName": "portMirrorHPE", "Probe#": "XX",
                    "Description": "Ativar ou desativar espelhamento de porta", "Resultado": "Erro ao se logar no equipamento."}

        ##########
        # Comandos
        try:
            with SSHClientInteraction(conn, timeout=10, display=False) as interact:
                interact.expect('\(HPE Routing\) >')
                interact.send('enable')
                interact.expect('\(HPE Routing\) #')
                interact.send('configure')
                interact.expect('\(HPE Routing\) \(Config\)#')

                #if ('Failed to configure the mirroring session.' in interact.current_output_clean):
                #    interact.send('no monitor session 1')
                #    interact.expect('\(HPE Routing\) \(Config\)#')
                #    interact.send('monitor session 1 destination interface ' + str(porta_destino))
                #    interact.expect('\(HPE Routing\) \(Config\)#')

                if (acao == "ativar"):
                    interact.send('monitor session 1 source interface ' + str(porta_origem))
                elif (acao == "desativar"):
                    interact.send('no monitor session 1 source interface ' + str(porta_origem))
                else:
                    return {"Resultado_Probe": "NOK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha,
                        "porta_origem": porta_origem, "porta_destino": porta_destino, "acao": acao,
                        "ControllerName": "network", "ProbeName": "portMirrorHPE", "Probe#": "XX",
                        "Description": "Ativar ou desativar espelhamento de porta",
                        "Resultado": "Acao nao suportada."}
                interact.expect('\(HPE Routing\) \(Config\)#')
                interact.send('monitor session 1 destination interface ' + str(porta_destino))
                interact.expect('\(HPE Routing\) \(Config\)#')
                interact.send('monitor session 1 mode')
                interact.expect('\(HPE Routing\) \(Config\)#')
                interact.send('exit')
                interact.expect('\(HPE Routing\) #')
                interact.send('write memory confirm')

                return {"Resultado_Probe": "OK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha,
                        "porta_origem": porta_origem, "porta_destino": porta_destino, "acao": acao,
                        "ControllerName": "network", "ProbeName": "portMirrorHPE", "Probe#": "XX",
                        "Description": "Ativar ou desativar espelhamento de porta", "Resultado": "200_OK"}
        except:
            return {"Resultado_Probe": "NOK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha, "porta_origem": porta_origem,
                    "porta_destino": porta_destino, "acao": acao, "ControllerName": "network", "ProbeName": "portMirrorHPE", "Probe#": "XX",
                    "Description": "Ativar ou desativar espelhamento de porta", "Resultado": "Erro durante a configuração do espelhamento."}

####
    def portChangeVLANHPE(self, ip_switch, usuario, senha, porta, vlan):
        # trava para impedir mudança de VLANs em portas fora dos DUTs
        # VLAN

        hguVLANRange = "15-30"
        hguVLANIni, hguVLANFim = hguVLANRange.split("-")

        obj = iptvProbe.iptv()

        if not (vlan >= hguVLANIni and vlan <= hguVLANFim):
            return {"Resultado_Probe": "NOK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha,
                    "porta": porta, "vlan": vlan, "ControllerName": "network", "ProbeName": "portChangeVLANHPE", "Probe#": "XX",
                    "Description": "Mudar VLAN da porta do switch HPE", "Resultado": "Fora da faixa de VLANs (" + hguVLANRange + ")."}

        # Portas
        porta_permitida = False

        for porta_dut in obj.pod_stb_switch_port:
            if porta_dut == porta:
                porta_permitida = True

        if porta_permitida == False:
            for porta_dut in obj.pod_hgu_switch_port:
                if porta_dut == porta:
                    porta_permitida = True

        if porta_permitida == False:
            return {"Resultado_Probe": "NOK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha,
                    "porta": porta, "vlan": vlan, "ControllerName": "network", "ProbeName": "portChangeVLANHPE", "Probe#": "XX",
                    "Description": "Mudar VLAN da porta do switch HPE", "Resultado": "Não permitida mudança nesta porta."}

        #######
        # Login
        conn = paramiko.SSHClient()
        conn.load_system_host_keys()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            conn.connect(hostname=ip_switch, username=usuario, password=senha)
        except:
            return {"Resultado_Probe": "NOK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha,
                    "porta": porta, "vlan": vlan, "ControllerName": "network", "ProbeName": "portChangeVLANHPE", "Probe#": "XX",
                    "Description": "Mudar VLAN da porta do switch HPE", "Resultado": "Erro ao se logar no equipamento."}

        ##########
        # Comandos
        try:
            with SSHClientInteraction(conn, timeout=10, display=False) as interact:
                interact.expect('\(HPE Routing\) >')
                interact.send('enable')
                interact.expect('\(HPE Routing\) #')
                interact.send('configure')
                interact.expect('\(HPE Routing\) \(Config\)#')
                interact.send('interface ' + str(porta))
                interact.expect('\(HPE Routing\).*')
                interact.send('vlan pvid ' + str(vlan))
                interact.expect('\(HPE Routing\).*')
                interact.send('vlan participation exclude ' + hguVLANRange)
                interact.expect('\(HPE Routing\).*')
                interact.send('vlan participation include ' + str(vlan))
                interact.expect('\(HPE Routing\).*')
                interact.send('exit')
                interact.expect('\(HPE Routing\).*')
                interact.send('exit')
                interact.expect('\(HPE Routing\).*')
                interact.send('write memory confirm')
                interact.expect('\(HPE Routing\).*')
                interact.send('logout')

                return {"Resultado_Probe": "OK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha,
                        "porta": porta, "vlan": vlan, "ControllerName": "network", "ProbeName": "portChangeVLANHPE", "Probe#": "XX",
                        "Description": "Mudar VLAN da porta do switch HPE", "Resultado": "VLAN modificada."}
        except:
            return {"Resultado_Probe": "NOK", "ip_switch": ip_switch, "usuario": usuario, "senha": senha,
                    "porta": porta, "vlan": vlan, "ControllerName": "network",
                    "Probe#": "XX", "ProbeName": "portChangeVLANHPE",
                    "Description": "Mudar VLAN da porta do switch HPE", "Resultado": "Erro durante a configuração."}

    ####
    def execIperf(self, server, port, duration, num_streams, protocol):

        try:
            print("OIOIO")
            client = iperf3.Client()
            client.duration = int(duration)
            client.server_hostname = server
            client.port = port
            client.num_streams = 2
            client.protocol = protocol
            result = client.run()
            velocUP = result.sent_Mbps
            velocDown = result.received_Mbps
            localhost = result.local_host
            remotehost = result.remote_host
            result_json = result.json
            result_iperf = {"Download": velocDown, "Upload": velocUP, "Client": localhost, "Server": remotehost,
                            "result": result_json}

            print(velocUP, velocDown, localhost)

            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "execIperf",
                      "Probe#": "XX", "Description": "Executar teste de velocidade", "Resultado": result_iperf}

        except Exception as e:
            return {"Resultado_Probe": "OK", "ControllerName": "network", "ProbeName": "execIperf",
                    "Probe#": "XX",
                    "Description": "Executar teste de velocidade", "Resultado": "ERROR"}
 """