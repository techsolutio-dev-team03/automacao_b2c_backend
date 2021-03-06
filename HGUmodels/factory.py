from .models.AskeyBROADCOM import HGU_AskeyBROADCOM

from .models.probe_MItraStarECNT.settingsProbe import HGU_MItraStarECNT_settingsProbe
from .models.probe_MItraStarECNT.wizardProbe import HGU_MItraStarECNT_wizardProbe
from .models.probe_MItraStarECNT.functionalProbe import HGU_MItraStarECNT_functionalProbe
from .models.probe_MItraStarECNT.ipv6Probe import HGU_MItraStarECNT_ipv6Probe
from .models.probe_MItraStarECNT.wireSharkProbe import HGU_MItraStarECNT_wireSharkProbe

from .models.probe_MItraStarBROADCOM.settingsProbe import HGU_MItraStarBROADCOM_settingsProbe
from .models.probe_MItraStarBROADCOM.wizardProbe import HGU_MItraStarBROADCOM_wizardProbe
from .models.probe_MItraStarBROADCOM.functionalProbe import HGU_MItraStarBROADCOM_functionalProbe
from .models.probe_MItraStarBROADCOM.ipv6Probe import HGU_MItraStarBROADCOM_ipv6Probe
from .models.probe_MItraStarBROADCOM.wireSharkProbe import HGU_MItraStarBROADCOM_wireSharkProbe

from .models.probe_AskeyECNT.settingsProbe import HGU_AskeyECNT_settingsProbe
from .models.probe_AskeyECNT.wizardProbe import HGU_AskeyECNT_wizardProbe
from .models.probe_AskeyECNT.functionalProbe import HGU_AskeyECNT_functionalProbe
from .models.probe_AskeyECNT.ipv6Probe import HGU_AskeyECNT_ipv6Probe
from .models.probe_AskeyECNT.wireSharkProbe import HGU_AskeyECNT_wireSharkProbe

from .models.probe_AskeyBroadcom.settingsProbe import HGU_AskeyBROADCOM_settingsProbe
from .models.probe_AskeyBroadcom.wizardProbe import HGU_AskeyBROADCOM_wizardProbe
from .models.probe_AskeyBroadcom.functionalProbe import HGU_AskeyBROADCOM_functionalProbe
from .models.probe_AskeyBroadcom.ipv6Probe import HGU_AskeyBROADCOM_ipv6Probe
from .models.probe_AskeyBroadcom.wireSharkProbe import HGU_AskeyBROADCOM_wireSharkProbe


class HGUModelFactory:
    @staticmethod
    def getHGU(probe, dict_result, model_name, username=None, password=None, address_ip=None, driver=None ):

        if model_name == 'HGU1_MitraStar_ECNT':
            if probe == 'settingsProbe':
                return HGU_MItraStarECNT_settingsProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'wizardProbe':
                return HGU_MItraStarECNT_wizardProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'functionalProbe':
                return HGU_MItraStarECNT_functionalProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'ipv6Probe':
                return HGU_MItraStarECNT_ipv6Probe(address_ip, model_name, username, password, driver, dict_result)
            elif probe == 'wireSharkProbe':
                return HGU_MItraStarECNT_wireSharkProbe(address_ip, model_name, username, password, driver, dict_result)

        elif model_name == 'HGU4_MitraStar_BROADCOM':
            if probe == 'settingsProbe':
                return HGU_MItraStarBROADCOM_settingsProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'wizardProbe':
                return HGU_MItraStarBROADCOM_wizardProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'functionalProbe':
                return HGU_MItraStarBROADCOM_functionalProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'ipv6Probe':
                return HGU_MItraStarBROADCOM_ipv6Probe(address_ip, model_name, username, password, driver, dict_result)
            elif probe == 'wireSharkProbe':
                return HGU_MItraStarBROADCOM_wireSharkProbe(address_ip, model_name, username, password, driver, dict_result)

        elif model_name == 'HGU2_Askey_ECNT':
            if probe == 'settingsProbe':
                return HGU_AskeyECNT_settingsProbe(address_ip, model_name, username, password, driver, dict_result)
            elif probe == 'wizardProbe':
                return HGU_AskeyECNT_wizardProbe(address_ip, model_name, username, password, driver, dict_result)
            elif probe == 'functionalProbe':
                return HGU_AskeyECNT_functionalProbe(address_ip, model_name, username, password, driver, dict_result)
            elif probe == 'ipv6Probe':
                return HGU_AskeyECNT_ipv6Probe(address_ip, model_name, username, password, driver, dict_result)
            elif probe == 'wireSharkProbe':
                return HGU_AskeyECNT_wireSharkProbe(address_ip, model_name, username, password, driver, dict_result)

        elif model_name == 'HGU3_Askey_BROADCOM':
            if probe == 'settingsProbe':
                return HGU_AskeyBROADCOM_settingsProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'wizardProbe':
                return HGU_AskeyBROADCOM_wizardProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'functionalProbe':
                return HGU_AskeyBROADCOM_functionalProbe(address_ip, model_name, username, password, driver, dict_result)
            if probe == 'ipv6Probe':
                return HGU_AskeyBROADCOM_ipv6Probe(address_ip, model_name, username, password, driver, dict_result)
            elif probe == 'wireSharkProbe':
                return HGU_AskeyBROADCOM_wireSharkProbe(address_ip, model_name, username, password, driver, dict_result)

        else:
            return None
