from flask_restful import Resource, reqparse
from flask import jsonify, request
from probes import appiumProbe


class appium(Resource):
    def get(self, method):
        if method == 'connectWifi':
            obj = appiumProbe.appium()
            ans = obj.connectWifi()
            return jsonify(ans)
        elif method == 'runSpeedTestOokla':
            obj = appiumProbe.appium()
            ans = obj.runSpeedTestOokla()
            return jsonify(ans)



    def post(self, method):
        if method == 'execConnectWifi':
            ssid = request.json['ssid']
            senhaWifi = request.json['senhaWifi']
            deviceName = request.json['deviceName']
            obj = appiumProbe.appium()
            ans = obj.execConnectWifi(ssid, senhaWifi, deviceName)
            return jsonify(ans)
        elif method == 'execForgetWifi':
            ssid = request.json['ssid']
            deviceName = request.json['deviceName']
            obj = appiumProbe.appium()
            ans = obj.execForgetWifi(ssid, deviceName)
            return jsonify(ans)
        elif method == 'checkDeviceInfo':
            deviceName = request.json['deviceName']
            obj = appiumProbe.appium()
            ans = obj.checkDeviceInfo(deviceName)
            return jsonify(ans)
        elif method == 'execTurnOn_OffWifi':
            deviceName = request.json['deviceName']
            obj = appiumProbe.appium()
            ans = obj.execTurnOn_OffWifi(deviceName)
            return jsonify(ans)
        elif method == 'checkWifiStatus':
            deviceName = request.json['deviceName']
            ssid = request.json['ssid']
            obj = appiumProbe.appium()
            ans = obj.checkWifiStatus(deviceName, ssid)
            return jsonify(ans)
        elif method == 'execAndroidWebNavigation':
            deviceName = request.json['deviceName']
            site = request.json['site']
            obj = appiumProbe.appium()
            ans = obj.execAndroidWebNavigation(deviceName, site)
            return jsonify(ans)
        elif method == 'execVoIPCall':
            deviceName = request.json['deviceName']
            callNumber = request.json['callNumber']
            obj = appiumProbe.appium()
            ans = obj.execVoIPCall(deviceName, callNumber)
            return jsonify(ans)
        elif method == 'execVoIPReceive':
            deviceName = request.json['deviceName']
            obj = appiumProbe.appium()
            ans = obj.execVoIPReceive(deviceName)
            return jsonify(ans)


        else:
            return {"name_teste": "Doesnt Exist", "response": "none"}