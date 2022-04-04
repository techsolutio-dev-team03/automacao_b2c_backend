from HGUmodels.main_session import MainSession

session = MainSession()

class HGUModelInterface():
    def __init__(self, address_ip, model_name, username, password, driver, dict_result):
        self._address_ip = address_ip
        self._model_name = model_name
        self._username = username
        self._password = password
        self._driver = driver
        self._dict_result = dict_result 
    

    def update_global_result_memory(self, flask_username, test_name, dict_out):
        if not session.check_username(flask_username):
            session.insert_username(flask_username)
            
        session.update_state(flask_username, test_name, dict_out)

    
    def accessWizard_401(self): pass

    def accessPadrao_403(self): pass

    def accessRemoteHttp_405(self): pass

    def accessRemoteTelnet_406(self): pass

    def accessRemoteSSH_407(self): pass

    def accessRemoteTrustedIP_408(self): pass

    def NTPServer_409(self): pass

    def timeZone_410(self): pass
    
    def checkACSSettings_411(self): pass

    def GPV_OneObjct_414(self): pass

    def periodicInformEnable_415(self, flasky_username): pass

    def periodicInformInterval_416(self, flasky_username): pass

    def connectionRequestPort_417(self, serialnumber, GPV_Param, IPACS, acsUsername, acsPassword): pass

    def enableCwmp_418(self, flasky_username): pass

    def userConnectionRequest_419(self, flasky_username): pass

    def checkWanInterface_420(self): pass

    def prioridadePPPoE_421(self, flasky_username): pass

    def tipoRedeInet_422(self, flasky_username):pass

    def checkNatSettings_423(self, flasky_username): pass



