from flask_restful import Resource, reqparse
from flask import jsonify, request
from probes import guiProbe
import requests
from threading import Thread
from bson.objectid import ObjectId
from pymongo import MongoClient
from daos.mongo_dao import MongoConnSigleton

mongo_conn = MongoConnSigleton()

class gui(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ip', type=str)

    def get(self, method):
        args = self.parser.parse_args()
        ip = args['ip']

        obj = guiProbe.gui()

        if method == "getUrlWebGuiDefault":
            ans = obj.getUrlWEBGuiDefault(ip)
        elif method == 'habilitaSSH':
            ans = obj.habilitaSSH()
        elif method == 'openingVideo':
            ans = obj.openingVideo()
        elif method == 'accessWizard':
            ans = obj.accessWizard()

    def post(self, method):

        obj = guiProbe.gui()

        #temporary fix
        username = request.get_json()['username']
        password = request.get_json()['password']
        ip = request.get_json()['ip']
        
        #Get all variables
        user_dict = {
            "username" : request.get_json()['username'],
            "password" : request.get_json()['password'],
            "ip" : request.get_json()['ip'],
            "model_name" : request.get_json()['modelo'],
            "flask_username" : request.get_json()['flask_username']
        }
       
        mongo_dict = {
            "test_battery_id" : request.get_json()['test_battery_id'],
            "caderno" : request.get_json()['caderno'],
            "test_num" : request.get_json()['test_num'],
            "test_name" : request.get_json()['test_name'],
        }

        result = getattr(obj, method)(**user_dict)
        
        test_result = result.get('result', None)
        obs = result.get('obs', None)
        ans = {'test_result': result}
        mongo_conn.update_one_test_by_id(**mongo_dict, test_result=test_result, obs=obs)
        return jsonify(ans)

        if method == 'habilitaSSH':
            print(request.form['ip'])
            ans = obj.habilitaSSH()

        elif method == 'checkACSUrlManaged':
            ip = request.json['ip']
            ans = obj.checkACSUrlManaged(ip,username,password)
        elif method == 'logoutWizard':
            ip = request.json['ip']
            ans = obj.logoutWizard(ip,username,password)
        elif method == 'getFullConfig':
            ip = request.json['ip']
            ans = obj.getFullConfig(ip,username,password)
        elif method == 'connectWizardhttps':
            ip = request.json['ip']
            ans = obj.connectWizardhttps(ip,username,password)
        elif method == 'checkPPPoEStatus':
            ip = request.json['ip']
            ans = obj.checkPPPoEStatus(ip)
        elif method == 'checkRedeGpon':
            ip = request.json['ip']
            ans = obj.checkRedeGpon(ip)
        elif method == 'testeSite':
            site1 = request.json['site1']
            site2 = request.json['site2']
            site3 = request.json['site3']
            ans = obj.testeSite(site1,site2,site3)
        elif method == 'checkBridgeMode':
            ip = request.json['ip']
            ans = obj.checkBridgeMode(ip, username, password)
        elif method == 'checkFacebook':
            ans = obj.checkFacebook()
        elif method == 'checkInstagram':
            ans = obj.checkInstagram()
        elif method == 'checkTwitter':
            ans = obj.checkTwitter()
        elif method == 'getFullConfigPadrao':
            ip = request.json['ip']
            ans = obj.getFullConfigPadrao(ip, username, password)
        elif method == 'checkRemoteAccess':
            ip = request.json['ip']
            ans = obj.checkRemoteAccess(ip, username, password)
        elif method == 'checkWanInterface_x':
            ip = request.json['ip']
            interface = request.json['interface']
            ans = obj.checkWanInterface_x(ip, username, password, interface)
        elif method == 'checkVoIPSettings':
            ip = request.json['ip']
            ans = obj.checkVoIPSettings(ip, username, password)
        elif method == 'checkNatSettings':
            ip = request.json['ip']
            ans = obj.checkNatSettings(ip, username, password)
        elif method == 'checkLANSettings':
            ip = request.json['ip']
            ans = obj.checkLANSettings(ip, username, password)
        elif method == 'checkNATALGSettings':
            ip = request.json['ip']
            ans = obj.checkNATALGSettings(ip, username, password)
        elif method == 'checkMulticastSettings':
            ip = request.json['ip']
            ans = obj.checkMulticastSettings(ip, username, password)
        elif method == 'checkLANDHCPSettings_x':
            ip = request.json['ip']
            port = request.json['port']
            ans = obj.checkLANDHCPSettings_x(ip, username, password, port)
        elif method == 'checkWifiSettingsPadrao':
            ip = request.json['ip']
            ans = obj.checkWifiSettingsPadrao(ip, username, password)
        elif method == 'connectFakeWizard':
            site1 = request.json['site1']
            ans = obj.connectFakeWizard(site1)
        elif method == 'checkYoutube':
            ans = obj.checkYoutube()
        elif method == 'runSpeedTest':
            ans = obj.runSpeedTest()
        elif method == 'accessBancoBrasil':
            ans = obj.accessBancoBrasil()
        elif method == 'accessBancoBradesco':
            ans = obj.accessBancoBradesco()
        elif method == 'accessTestMyIPv6':
            ans = obj.accessTestMyIPv6()
        elif method == 'accessTestIPv6':
            ans = obj.accessTestIPv6()
        elif method == 'accessVivo':
            ans = obj.accessVivo()
        elif method == 'accessBancoSantander':
            ans = obj.accessBancoSantander()
        elif method == 'accessBancoCaixa':
            ans = obj.accessBancoCaixa()
        elif method == 'checkUPnPSettings':
            ip = request.json['ip']
            ans = obj.checkUPnPSettings(ip, username, password)
        elif method == 'checkForbiddenURLs':
            ip = request.json['ip']
            ans = obj.checkForbiddenURLs(ip)
        elif method == 'checkRefusedURLs':
            ip = request.json['ip']
            ans = obj.checkRefusedURLs(ip)
        ### ------------------------------------------ ###
        ###         FUNÇÕES DE CONFIGURAÇÃO
        ### ------------------------------------------ ###
        elif method == 'shutdownInterfacePPPoE':
            ip = request.json['ip']
            ans = obj.shutdownInterfacePPPoE(ip, username, password)
        elif method == 'execSoftResetGUI':
            ip = request.json['ip']
            ans = obj.execSoftResetGUI(ip, username, password)
        elif method == 'changeWifi24_Password':
            ip = request.json['ip']
            senhaWifi = request.json['senhaWifi']
            ans = obj.changeWifi24_Password(ip, username, password, senhaWifi)
        elif method == 'execDisableIPv6':
            ip = request.json['ip']
            ans = obj.execDisableIPv6(ip, username, password)
        elif method == 'execDisableIPv4':
            ip = request.json['ip']
            ans = obj.execDisableIPv4(ip, username, password)
        elif method == 'execEnableDualStack':
            ip = request.json['ip']
            ans = obj.execEnableDualStack(ip, username, password)
        elif method == 'enablePPPoE':
            ip = request.json['ip']
            ans = obj.enablePPPoE(ip, username, password)
        elif method == 'execRebootGUI':
            ip = request.json['ip']
            ans = obj.execRebootGUI(ip, username, password)
        elif method == 'changeWifi24_SSID':
            ip = request.json['ip']
            ssid = request.json['ssid']
            ans = obj.changeWifi24_SSID(ip, username, password, ssid)
        elif method == 'changeWifi5_SSID':
            ip = request.json['ip']
            ssid = request.json['ssid']
            ans = obj.changeWifi5_SSID(ip, username, password, ssid)
        elif method == 'changeWifi5_Password':
            ip = request.json['ip']
            senhaWifi = request.json['senhaWifi']
            ans = obj.changeWifi5_Password(ip, username, password, senhaWifi)
        elif method == 'execDisableWifi24':
            ip = request.json['ip']
            ans = obj.execDisableWifi24(ip, username, password)
        elif method == 'execEnableWifi24':
            ip = request.json['ip']
            ans = obj.execEnableWifi24(ip, username, password)
        elif method == 'execDisableWifi5':
            ip = request.json['ip']
            ans = obj.execDisableWifi5(ip, username, password)
        elif method == 'execEnableWifi5':
            ip = request.json['ip']
            ans = obj.execEnableWifi5(ip, username, password)
        elif method == 'changeAdminPasswordWithoutCurrent':
            ip = request.json['ip']
            username = request.json['username']
            old_password = request.json['old_password']
            new_password = request.json['new_password']
            ans = obj.changeAdminPasswordWithoutCurrent(ip, username, old_password, new_password)
        elif method == 'changeAdminPasswordWithoutReconfirm':
            ip = request.json['ip']
            username = request.json['username']
            old_password = request.json['old_password']
            new_password = request.json['new_password']
            ans = obj.changeAdminPasswordWithoutReconfirm(ip, username, old_password, new_password)
        elif method == 'changeChannelWifi24Wizard':
            ip = request.json['ip']
            channel = request.json['channel']
            ans = obj.changeChannelWifi24Wizard(ip, username, password, channel)
        elif method == 'changeChannelWifi5Wizard':
            ip = request.json['ip']
            channel = request.json['channel']
            ans = obj.changeChannelWifi5Wizard(ip, username, password, channel)
        elif method == 'hideWifi24Wizard':
            ip = request.json['ip']
            ans = obj.hideWifi24Wizard(ip, username, password)
        elif method == 'hideWifi5Wizard':
            ip = request.json['ip']
            ans = obj.hideWifi5Wizard(ip, username, password)
        elif method == 'unhideWifi24Wizard':
            ip = request.json['ip']
            ans = obj.unhideWifi24Wizard(ip, username, password)
        elif method == 'unhideWifi5Wizard':
            ip = request.json['ip']
            ans = obj.unhideWifi5Wizard(ip, username, password)
        elif method == 'changeBandWidth24Wizard':
            ip = request.json['ip']
            bandwidth = request.json['bandwidth']
            ans = obj.changeBandWidth24Wizard(ip, username, password, bandwidth)
        elif method == 'changeBandWidth5Wizard':
            ip = request.json['ip']
            bandwidth = request.json['bandwidth']
            ans = obj.changeBandWidth5Wizard(ip, username, password, bandwidth)
        elif method == 'execPingWizard':
            ip = request.json['ip']
            destino = request.json['destino']
            tentativas = request.json['tentativas']
            ans = obj.execPingWizard(ip, username, password, destino,tentativas)
        elif method == 'changePPPoESettings':
            ip = request.json['ip']
            pppoe_user = request.json['pppoe_user']
            pppoe_paswd = request.json['pppoe_paswd']
            ans = obj.changePPPoESettings(ip, username, password, pppoe_user,pppoe_paswd)
        elif method == 'changePPPoESettingsWrong':
            ip = request.json['ip']
            pppoe_user = request.json['pppoe_user']
            pppoe_paswd = request.json['pppoe_paswd']
            ans = obj.changePPPoESettingsWrong(ip, username, password, pppoe_user,pppoe_paswd)
        elif method == 'execEnablePortMirror':
            ip = request.json['ip']
            ans = obj.execEnablePortMirror(ip, username, password)
        elif method == 'execEnableUPnPSettings':
            ip = request.json['ip']
            ans = obj.execEnableUPnPSettings(ip, username, password)
        elif method == 'execDisableUPnPSettings':
            ip = request.json['ip']
            ans = obj.execDisableUPnPSettings(ip, username, password)
        elif method == 'execFakeFirmwareUpdate':
            ip = request.json['ip']
            ans = obj.execFakeFirmwareUpdate(ip, username, password)
        elif method == 'execSkypeWeb':
            ans = obj.execSkypeWeb(username, password)
        elif method == 'teste':
            ans = obj.teste()
        elif method == 'execCreateFirewallRule':
            ip = request.json['ip']
            ruleName = request.json['ruleName']
            ruleProtocol = request.json['ruleProtocol']
            ruleLocalPort = request.json['ruleLocalPort']
            ruleRemotePort = request.json['ruleRemotePort']
            ruleLocalIP = request.json['ruleLocalIP']
            ruleRemoteIP = request.json['ruleRemoteIP']
            ruleAction = request.json['ruleAction']
            ans = obj.execCreateFirewallRule(ip, username, password, ruleName, ruleProtocol, ruleLocalPort, ruleRemotePort, ruleLocalIP, ruleRemoteIP, ruleAction)
        elif method == 'checkFacebookIPv6':
            ans = obj.checkFacebookIPv6()
        elif method == 'checkCofoneIPv6':
            ans = obj.checkCofoneIPv6()
        elif method == 'checkSessionExpirationWizard':
            ip = request.json['ip']
            ans = obj.checkSessionExpirationWizard(ip, username, password)
        elif method == 'execEnableSSHWizard':
            ip = request.json['ip']
            ans = obj.execEnableSSHWizard(ip, username, password)
        elif method == 'execEnableTelnetWizard':
            ip = request.json['ip']
            ans = obj.execEnableTelnetWizard(ip, username, password)
        elif method == 'changeAuthModeWifi24Wizard':
            ip = request.json['ip']
            authentication = request.json['authentication']
            ans = obj.changeAuthModeWifi24Wizard(ip, username, password, authentication)
        elif method == 'changeAuthModeWifi5Wizard':
            ip = request.json['ip']
            authentication = request.json['authentication']
            ans = obj.changeAuthModeWifi5Wizard(ip, username, password, authentication)
        elif method == 'changeStandard24Wizard':
            ip = request.json['ip']
            standard = request.json['standard']
            ans = obj.changeStandard24Wizard(ip, username, password, standard)
        elif method == 'changeStandard5Wizard':
            ip = request.json['ip']
            standard = request.json['standard']
            ans = obj.changeStandard5Wizard(ip, username, password, standard)
        elif method == 'execSoftResetPadrao':
            ip = request.json['ip']
            ans = obj.execSoftResetPadrao(ip, username, password)
        elif method == 'execCreateFirewallRuleACS':
            ip = request.json['ip']
            ruleName = request.json['ruleName']
            ruleProtocol = request.json['ruleProtocol']
            ruleLocalPort = request.json['ruleLocalPort']
            ruleRemotePort = request.json['ruleRemotePort']
            ruleLocalIP = request.json['ruleLocalIP']
            ruleRemoteIP = request.json['ruleRemoteIP']
            ruleAction = request.json['ruleAction']
            ans = obj.execCreateFirewallRuleACS(ip, username, password, ruleName, ruleProtocol, ruleLocalPort, ruleRemotePort, ruleLocalIP, ruleRemoteIP, ruleAction)
        elif method == 'accessWizardFirefox':
            ip = request.json['ip']
            ans = obj.accessWizardFirefox(ip, username, password)
        elif method == 'execFirmwareUpdate':
            ip = request.json['ip']
            ans = obj.execFirmwareUpdate(ip, username, password)
        elif method == 'execConfigDNS':
            ip = request.json['ip']
            primaryDNS = request.json['primaryDNS']
            secondaryDNS = request.json['secondaryDNS']
            ans = obj.execConfigDNS(ip, username, password, primaryDNS, secondaryDNS)
        elif method == 'execEnableDMZ':
            ip = request.json['ip']
            DMZHost = request.json['DMZHost']
            ans = obj.execEnableDMZ(ip, username, password, DMZHost)
        elif method == 'execDisableDMZ':
            ip = request.json['ip']
            ans = obj.execDisableDMZ(ip, username, password)
        elif method == 'execAddDDNS':
            ip = request.json['ip']
            provider = request.json['provider']
            hostname = request.json['hostname']
            interface = request.json['interface']
            ddnsUsername = request.json['ddnsUsername']
            ddnsPassword = request.json['ddnsPassword']
            ans = obj.execAddDDNS(ip, username, password, provider, hostname, interface, ddnsUsername, ddnsPassword)
        elif method == 'execChangeDHCPRange':
            ip = request.json['ip']
            dhcpRangeMin = request.json['dhcpRangeMin']
            dhcpRangeMax = request.json['dhcpRangeMax']
            ans = obj.execChangeDHCPRange(ip, username, password, dhcpRangeMin, dhcpRangeMax)
        elif method == 'execChangeVLAN':
            ip = request.json['ip']
            interface = request.json['interface']
            vlanValue = request.json['vlanValue']
            ans = obj.execChangeVLAN(ip, username, password, interface, vlanValue)
        elif method == 'execChangeACSURL':
            ip = request.json['ip']
            acsURL = request.json['acsURL']
            periodicInterval = request.json['periodicInterval']
            ans = obj.execChangeACSURL(ip, username, password, acsURL, periodicInterval)
        elif method == 'execDHCPReserv':
            ip = request.json['ip']
            staticIP = request.json['staticIP']
            ans = obj.execDHCPReserv(ip, username, password, staticIP)
        else:
            return {"name_teste": "Doesnt Exist", "response": "none"}
        return jsonify(ans)
        
