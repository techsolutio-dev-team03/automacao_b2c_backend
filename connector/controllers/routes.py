from connector import app, api
from flask_restful import Api, Resource
from connector.controllers import networkController
from connector.controllers import cliController
from connector.controllers import guiController
from connector.controllers import iptvController
from connector.controllers import atuadoresController
from connector.controllers import tsharkController
from connector.controllers import appiumController
from connector.controllers import acsController
from connector.controllers import opencvController
from connector.controllers import utilsController
from connector.controllers import ipv6Controller
from connector.controllers import firmwareController

class home(Resource):
    def get(self):
        return {"api" : {
            "connectividade" : "http://localhost:8000/api/v1/network/getUrlGuiDefault",
            "ssh": "http://localhost:8000/api/v1/ssh",
            "routes": app.url_map
        }}

api.add_resource(home, "/")

api.add_resource(networkController.network, "/api/v1/network/<string:method>")

api.add_resource(cliController.cli, "/api/v1/cli/<string:method>")

api.add_resource(guiController.gui, "/api/v1/gui/<string:method>")

api.add_resource(iptvController.iptv, "/api/v1/iptv/<string:method>")

api.add_resource(tsharkController.captura, "/api/v1/tshark/<string:method>")

api.add_resource(atuadoresController.atuadores, "/api/v1/atuadores/<string:method>")

api.add_resource(appiumController.appium, "/api/v1/appium/<string:method>")

api.add_resource(acsController.acs, "/api/v1/acs/<string:method>")

api.add_resource(opencvController.opencv, "/api/v1/opencv/<string:method>")

api.add_resource(utilsController.utils, "/api/v1/utils/<string:method>")

api.add_resource(ipv6Controller.ipv6, "/api/v1/ipv6/<string:method>")

api.add_resource(firmwareController.firmware, "/api/v1/firmware/<string:method>")