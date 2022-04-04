# -*- coding: utf-8 -*-
#
import ast
import sys

from zeep import Client
from zeep import xsd
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
import logging.config

### DEBUG PARA VERIFICAR COMUNICAÇÃO SOAP ###
# logging.config.dictConfig({
#     'version': 1,
#     'formatters': {
#         'verbose': {
#             'format': '%(name)s: %(message)s'
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'zeep.transports': {
#             'level': 'DEBUG',
#             'propagate': True,
#             'handlers': ['console'],
#         },
#     }
# })
#
class SDO:
    def __init__(self, iphdm, porthdm, username, password):
        self.ip = iphdm
        self.port = porthdm
        self.username = username
        self.password = password
        self.connectionError = ''
        self.msgConnection = ''
        self.isOnline = ''
        self.msgTagExecution_PingDiag = ''
        self.msgErrorDetail_PingDiag = ''
        self.msgErrorLog_PingDiag = ''
        self.msgTagExecution_SPV = ''
        self.msgErrorDetail_SPV = ''
        self.msgErrorLog_SPV = ''
        self.msgTagExecution_SPV_ERROR = ''
        self.msgTagExecution_GPV = ''
        self.msgErrorDetail_GPV = ''
        self.msgErrorLog_GPV = ''
        self.msgTagExecution_GPV_ERROR = ''
        self.msgTagExecution_012 = ''
        self.msgErrorDetail_022 = ''
        self.msgErrorLog_022 = ''
        try:
            transport = Transport(timeout=2)
            SDO = "http://" + self.ip + ":" + self.port + "/SynchDeviceOpsImpl/SynchDeviceOperationsNBIService?wsdl"
            self.client = Client(SDO, wsse=(UsernameToken(self.username, self.password)), transport=transport)
            self.connectionError = 'False'
            self.msgTagExecution = 'EXECUTED'
            self.msgErrorLog = 'NONE'
            self.msgErrorDetail = 'MSG_003-WSDL INFORMADO COM SUCESSO SDO'
        except:
            e = sys.exc_info()[1]
            print(e)
            self.msgTagExecution = 'ERROR'
            self.msgErrorLog = str(e)
            self.msgErrorDetail = 'MSG_003-ERRO AO INFORMAR WSDL SDO'
#
    def issueConnectionRequest(self, OUI, productClass, protocol, seriaNumber):
        nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                       'serialNumber': seriaNumber}
        print(nbiDeviceId)
        parameter = int(3500)
        try:
            connect = self.client.service.issueConnectionRequest(arg0=nbiDeviceId, arg1=parameter)
            self.isOnline = str(connect['success'])
            self.msgTagExecution_01 = 'EXECUTED'
            self.msgErrorLog_01 = 'ONLINE'
            self.msgErrorDetail_01 = 'MSG_002-SUCESSO DISPOSITIVO ONLINE'
            return self.isOnline
        except:
            e = sys.exc_info()[1]
            print(e)
            self.isOnline = 'False'
            self.msgTagExecution_01 = 'ERROR'
            self.msgErrorLog_01 = str(e)
            self.msgErrorDetail_01 = 'ERROR_007-ERROR DISPOSITIVO OFFLINE'
            return self.isOnline
#
    def getParameterValue(self, OUI, productClass, protocol, serialNumber, object):
        try:
            #object = 'InternetGatewayDevice.ManagementServer.PeriodicInformInterval'
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol, 'serialNumber': serialNumber}
            timeout = 30000
            nBIOptions = {'disableCaptureConstraint': 'true', 'executionTimeoutSeconds': '120',
                          'expirationTimeoutSeconds': '60',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555', 'policyClass': 'policytest', 'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false', 'updateCachedDataRecord': 'true'}
            #getParameterValue = self.client.service.getParameterValues(arg0=nbiDeviceId, arg1=object, arg2=nBIOptions, arg3=timeout)
            getParameterValue = self.client.service.getParameterValues(arg0=nbiDeviceId, arg1=object, arg2=nBIOptions, arg3=timeout)
            self.msgTagExecution_GPV = 'EXECUTED'
            #print(getParameterValue)
            return getParameterValue
        except TypeError:
            print("'NoneType' object is not iterable")
        except:
            e = sys.exc_info()[1]
            self.msgTagExecution_GPV_ERROR = 'ERROR'
            self.msgErrorLog_GPV = str(e)
            self.msgErrorDetail_GPV = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR GPV'

    def setParameterValue(self, OUI, productClass, protocol, serialNumber, input):
        # print(input)
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol, 'serialNumber': serialNumber}
            parameter = {
                'parameterKey': '?',
                'parameterValueStructs':input
            }
            timeout = 50000
            nBIOptions = {'disableCaptureConstraint': 'true', 'executionTimeoutSeconds': '300',
                          'expirationTimeoutSeconds': '240',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555', 'policyClass': 'policytest', 'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false', 'updateCachedDataRecord': 'true'}
            self.parameterValue = self.client.service.setParameterValues(arg0=nbiDeviceId, arg1=parameter, arg2=nBIOptions, arg3=timeout)
            self.msgTagExecution_SPV = 'EXECUTED'
            #print(self.msgTagExecution_SPV)

        except:
            e = sys.exc_info()[1]
            self.msgTagExecution_SPV_ERROR = 'ERROR'
            self.msgErrorLog_SPV = str(e)
            self.msgErrorDetail_SPV = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR SPV'

    def pingDiagnostics(self, OUI, productClass, protocol, serialNumber, objeto):
        #Custom function Ping Diagnostics -> FunctionCode = 9530
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol, 'serialNumber': serialNumber}
            numberExecuteFunction = 9530
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            #parameter = str({"destAddress":"www.google.com.br", "qtdRequisitions":"2"})
            parameter = str({"destAddress": objeto, "qtdRequisitions": "4"})
            #print(parameter)
            ansPingDiag = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), parameter),
                                                         arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            #print(ansPingDiag)
            ansPingDiag = ast.literal_eval(ansPingDiag)
            # print('---------------------------------------------------------------')
            # print('                      PING RESULTS      ')
            # print('---------------------------------------------------------------')
            global varList
            varList = []
            for key, value in ansPingDiag.items():
                temp = [key, value]
                varList.append(temp)
            #for i in varList:
                #print(i)
            #print('-=' * 32)
            self.msgTagExecution_PingDiag = 'EXECUTED'
            return varList
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            #print('PRINT DO EXCEPT = ' + e)
            self.msgTagExecution_PingDiag_ERROR = 'ERROR'
            self.msgErrorLog_PingDiag = str(e)
            self.msgErrorDetail_PingDiag = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR PingDiag'

    def checkOnline(self, OUI, productClass, protocol, seriaNumber):
        nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                       'serialNumber': seriaNumber}
        parameter = int(10000)
        nBIOptions = {'disableCaptureConstraint': 'true',
                      'executionTimeoutSeconds': '1200',
                      'expirationTimeoutSeconds': '180',
                      'failOnConnectionRequestFailure': 'true',
                      'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                      'opaqueTransactionId': 'teste555',
                      'policyClass': 'policytest',
                      'priority': '100',
                      'replaceDeviceCachedDataRecord': 'false',
                      'updateCachedDataRecord': 'true'}
        try:
            connect = self.client.service.checkOnline(arg0=nbiDeviceId, arg1=nBIOptions, arg2=parameter)
            self.msgTagExecution_01 = 'EXECUTED'
            self.msgErrorLog_01 = 'ONLINE'
            self.msgErrorDetail_01 = 'MSG_002-SUCESSO DISPOSITIVO ONLINE'
        except:
            e = sys.exc_info()[1]
            self.isOnline = 'False'
            self.msgTagExecution_01 = 'ERROR'
            self.msgErrorLog_01 = str(e)
            self.msgErrorDetail_01 = 'ERROR_007-ERROR DISPOSITIVO OFFLINE'

    def getHGU_DIAGNOSTICS_CUSTOM(self, OUI, productClass, protocol, serialNumber):
        # Custom function Ping Diagnostics -> FunctionCode = 9530
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 12000
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            #print(timeout)
            HGU_DIAG = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), '{}'),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            print(HGU_DIAG)
            self.msgTagExecution_PingDiag = 'EXECUTED'
            return HGU_DIAG
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
            self.msgTagExecution_PingDiag_ERROR = 'ERROR'
            self.msgErrorLog_PingDiag = str(e)
            self.msgErrorDetail_PingDiag = 'ERROR_006-remoteHDM-ERROR AO EXECUTAR PingDiag'

    def getWifiStatus(self, OUI, productClass, protocol, serialNumber):
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9554
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            getWifiStatus = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), '{}'),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            print(getWifiStatus)
            return getWifiStatus
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))

    def getParameterAttributes(self, OUI, productClass, protocol, serialNumber, objeto):
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            getParameterAttributes = self.client.service.getParameterAttributes(arg0=nbiDeviceId, arg1=objeto, arg2=nBIOptions, arg3=timeout)
            # print(getParameterAttributes)
            return getParameterAttributes
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))

    def getLANHosts(self, OUI, productClass, protocol, serialNumber):
        # Custom function getLANHosts -> FunctionCode = 9517
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9517
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            getLANHosts = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), '{}'),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            # print(getLANHosts)
            return getLANHosts
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))

    def getPPPoECredentials(self, OUI, productClass, protocol, serialNumber):
        # Custom function getPPPoECredentials -> FunctionCode = 9523
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9523
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            getPPPoECredentials = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), '{}'),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            # print(getPPPoECredentials)
            return getPPPoECredentials
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))

    def setPPPoECredentials(self, OUI, productClass, protocol, serialNumber, credentials):
        # Custom function setPPPoECredentials -> FunctionCode = 9522
        try:
            print(credentials)
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9522
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '1800',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            setPPPoECredentials = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), str(credentials)), arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            # print(setPPPoECredentials)
            return setPPPoECredentials
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
        # except zeep.exceptions.Fault as fault:
        #     print(fault.message)
        #     print(fault.code)
        #     print(fault.actor)
        #     print(fault.detail)

    def getPortMapping(self, OUI, productClass, protocol, serialNumber):
        # Custom function getPortMapping -> FunctionCode = 9513
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9513
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '1800',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            getPortMapping = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), '{}'), arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            # print(getPortMapping)
            return getPortMapping
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
        # except zeep.exceptions.Fault as fault:
        #     print(fault.message)
        #     print(fault.code)
        #     print(fault.actor)
        #     print(fault.detail)

    def addPortMapping(self, OUI, productClass, protocol, serialNumber, options):
        # Custom function addPortMapping -> FunctionCode = 9512
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9512
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '1800',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            addPortMapping = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), str(options)), arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            # print(addPortMapping)
            return addPortMapping
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
        # except zeep.exceptions.Fault as fault:
        #     print(fault.message)
        #     print(fault.code)
        #     print(fault.actor)
        #     print(fault.detail)

    def setVoIP(self, OUI, productClass, protocol, serialNumber, parameters):
        # Custom function setVoIP -> FunctionCode = 9512
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9512
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '1800',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            setVoIP = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), str(parameters)), arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            # print(setVoIP)
            return setVoIP
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
        # except zeep.exceptions.Fault as fault:
        #     print(fault.message)
        #     print(fault.code)
        #     print(fault.actor)
        #     print(fault.detail)

    def setWifi(self, OUI, productClass, protocol, serialNumber, wifi_settings):
        # Custom function wifi_settings -> FunctionCode = 9556
        try:
            print(wifi_settings)
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9556
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '1800',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            setWifi = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), str(wifi_settings)), arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            # print(setWifi)
            return setWifi
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
        # except zeep.exceptions.Fault as fault:
        #     print(fault.message)
        #     print(fault.code)
        #     print(fault.actor)
        #     print(fault.detail)

    def cancelVoIP(self, OUI, productClass, protocol, serialNumber, parameter):
        # Custom function cancelVoIP -> FunctionCode = 9540
        try:
            print(parameter)
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9540
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '1800',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 30000
            cancelVoIP = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), str(parameter)), arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            # print(cancelVoIP)
            return cancelVoIP
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))

    def downloadDiagnostics(self, OUI, productClass, protocol, serialNumber, downloadURL): ### VERIFICAR SAIDA!!!!!!!!!!!
        # Custom function DownloadDiagnostics -> FunctionCode = 9110
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9110
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '3800000',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 5000000
            downloadDiagnostics = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), str(downloadURL)),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            print(downloadDiagnostics)
            return downloadDiagnostics
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
            return e

    def getDHCP(self, OUI, productClass, protocol, serialNumber):
        # Custom function getDHCP -> FunctionCode = 9509
        try:
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9509
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '180',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 50000
            getDHCP = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=xsd.AnyObject(xsd.String(), '{}'),arg2=numberExecuteFunction, arg3=nBIOptions,arg4=timeout)
            # print(getDHCP)
            return getDHCP
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))

    def setDHCP(self, OUI, productClass, protocol, serialNumber, parameters):
        # Custom function setDHCP -> FunctionCode = 9508
        try:
            print(parameters)
            nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                           'serialNumber': serialNumber}
            numberExecuteFunction = 9508
            nBIOptions = {'disableCaptureConstraint': 'true',
                          'executionTimeoutSeconds': '1800',
                          'expirationTimeoutSeconds': '180',
                          'failOnConnectionRequestFailure': 'true',
                          'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                          'opaqueTransactionId': 'teste555',
                          'policyClass': 'policytest',
                          'priority': '100',
                          'replaceDeviceCachedDataRecord': 'false',
                          'updateCachedDataRecord': 'true'}
            timeout = 40000
            setDHCP = self.client.service.executeFunction(arg0=nbiDeviceId, arg1=parameters, arg2=numberExecuteFunction, arg3=nBIOptions, arg4=timeout)
            # print(setDHCP)
            return setDHCP
        except TypeError:
            print('list index out of range')
        except:
            e = sys.exc_info()[1]
            print(e)
            print('PRINT DO EXCEPT = ' + str(e))
        # except zeep.exceptions.Fault as fault:
        #     print(fault.message)
        #     print(fault.code)
        #     print(fault.actor)
        #     print(fault.detail)

    def resetFactory(self, OUI, productClass, protocol, seriaNumber):
        nbiDeviceId = {'OUI': OUI, 'productClass': productClass, 'protocol': protocol,
                       'serialNumber': seriaNumber}
        nBIOptions = {'disableCaptureConstraint': 'true',
                      'executionTimeoutSeconds': '1800',
                      'expirationTimeoutSeconds': '180',
                      'failOnConnectionRequestFailure': 'true',
                      'NBISingleDeviceOperationCallBackInfo': {'retry': 'false'},
                      'opaqueTransactionId': 'teste555',
                      'policyClass': 'policytest',
                      'priority': '100',
                      'replaceDeviceCachedDataRecord': 'false',
                      'updateCachedDataRecord': 'true'}
        timeout = int(900000)
        try:
            connect = self.client.service.factoryReset(arg0=nbiDeviceId, arg1=nBIOptions, arg2=timeout)
            self.isOnline = str(connect['success'])
            self.msgTagExecution_01 = 'EXECUTED'
            self.msgErrorLog_01 = 'ONLINE'
            self.msgErrorDetail_01 = 'MSG_002-SUCESSO DISPOSITIVO ONLINE'
            return self.isOnline
        except:
            e = sys.exc_info()[1]
            print(e)
            self.isOnline = 'False'
            self.msgTagExecution_01 = 'ERROR'
            self.msgErrorLog_01 = str(e)
            self.msgErrorDetail_01 = 'ERROR_007-ERROR DISPOSITIVO OFFLINE'
            return self.isOnline