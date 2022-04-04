# -*- coding: utf-8 -*-
#
from zeep import Client
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken
import sys
#
class NSI:
    def __init__(self, iphdm, porthdm, username, password):
        self.ip = iphdm
        self.port = porthdm
        self.username = username
        self.password = password
        self.connectionError = ''
        self.msgConnection = ''
        self.connectionError1 = ''
        self.msgConnection1 = ''
        self.device = ''

        try:
            transport = Transport(timeout=2)
            serviceImpl = "http://" + self.ip + ":" + self.port + "/NBIServiceImpl/NBIService?wsdl"
            self.client = Client(serviceImpl, wsse=(UsernameToken(self.username, self.password)), transport=transport)
            self.connectionError = 'False'
            self.msgConnection = 'Successfull to connect with #serviceImpl# webservice'
        except:
            e = sys.exc_info()[1]
            self.connectionError = 'True'
            self.msgConnection = 'Error to connect with serviceImpl webservice'
#
#
#
    def findByDeviceGUID(self, deviceGUID):
        self.deviceGUID = str(deviceGUID)
        try:
            connect = self.client.service.findDeviceByGUID(arg0=self.deviceGUID)
            self.connectionError1 = 'False'
            self.msgConnection1 = 'Successfull to find atributos do device utilizando findByDeviceGUID'
            self.device = {"OUI": connect['deviceId']['OUI'],
                           "productClass": connect['deviceId']['productClass'],
                           "protocol": connect['deviceId']['protocol'],
                           "serialNumber": connect['deviceId']['serialNumber'],
                           "activated": connect['activated'],
                           "iPAddress": connect['IPAddress'],
                           "lastActivationTime": connect['lastActivationTime'],
                           "lastContactTime": connect['lastContactTime'],
                           "macAddress": connect['macAddress'],
                           "manufacturer": connect['manufacturer'],
                           "modelName": connect['modelName'],
                           "softwareVersion": connect['softwareVersion'],
                           "subscriberID": connect['subscriberID']}
        except:
            e = sys.exc_info()[1]
            print(e)
            self.connectionError1 = 'True'
            self.msgConnection1 = 'ERROR to find atributos do device utilizando findByDeviceGUID'


    def setServiceTag(self, deviceGUID, nameTag, valueTag):
        self.deviceGUID = str(deviceGUID)
        self.nameTag = str(nameTag)
        self.valueTag = str(valueTag)
        serviceTagName = {'name' : self.nameTag, 'value' : self.valueTag, 'copyOnFactoryReset': 'false'}
        try:
            self.client.service.setServiceTag(arg0=deviceGUID, arg1=serviceTagName)
            self.connectionError2 = 'False'
            self.msgConnection2 = 'SUCCESSFULL TO CONFIGURE SERVICE TAG'
        except:
            e = sys.exc_info()[1]
            print(e)
            self.connectionError2 = 'True'
            self.msgConnection2 = 'ERROR TO CONFIGURE SERVICE TAG'