import subprocess
import os
import datetime, time


class tsharkCapture:

    def capture(self, time, iface, path, file):
        try:
            #file = 'capturaTshark.pcap'
            #path = '/home/hulrich/PycharmProjects/pytest-html-reporter/cpe-data/'

            argumentos = ' -i ' + iface + ' -a duration:' + time + ' -w ' + path + file

            if (os.name == 'nt'):
                path_exe = 'C:\\Program Files\\Wireshark\\'
                comando = 'tshark.exe'
                cmd = (argumentos).split()
                cmd.insert(0,path_exe+comando)
            else:
                cmd = ['tshark ' + argumentos]

            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            return{"Resultado_Probe": "OK", "ControllerName": "tshark", "ProbeName": "capture", "Probe#": "48",
             "Description": "Executar captura", "Resultado": "captura_inciada"}
        except:
            return {"Resultado_Probe": "NK", "ControllerName": "tshark", "ProbeName": "capture", "Probe#": "48",
                    "Description": "Executar captura", "Resultado": "error_captura"}

    def captureCustom(self, time, iface, path, file, filter):

        if (filter == ""):
            return {"Resultado_Probe": "NOK", "ControllerName": "tshark", "ProbeName": "captureCustom", "Probe#": "48",
            "Description": "Executar captura custom", "Resultado": "Filtro nao informado."}

        try:
            #file = 'capturaTshark.pcap'
            #path = '/home/hulrich/PycharmProjects/pytest-html-reporter/cpe-data/'
            argumentos = ' -i ' + iface + ' -f -a duration:' + time + ' -w ' + path + file

            if (os.name == 'nt'):
                path_exe = 'C:\\Program Files\\Wireshark\\'
                comando = 'tshark'
                cmd = (argumentos).split()
                cmd.insert(0,path_exe+comando)
                cmd.insert(4,filter)
            else:
                cmd = ['tshark.exe ' + argumentos]

            #print(cmd)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            return{"Resultado_Probe": "OK", "ControllerName": "tshark", "ProbeName": "capture", "Probe#": "48",
             "Description": "Executar captura", "Resultado": "captura_inciada"}
        except:
            return {"Resultado_Probe": "NOK", "ControllerName": "tshark", "ProbeName": "capture", "Probe#": "48",
                    "Description": "Executar captura", "Resultado": "error_captura"}


