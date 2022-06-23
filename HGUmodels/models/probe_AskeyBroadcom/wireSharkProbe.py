import os
import subprocess
from ..AskeyBROADCOM import HGU_AskeyBROADCOM
import pyshark
import multiprocessing
import asyncio
import time


class  HGU_AskeyBROADCOM_wireSharkProbe(HGU_AskeyBROADCOM):


# 178
    def capture_adv_pkt(self, return_dict):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        capture = pyshark.LiveCapture(eventloop=loop, interface=interface_name, display_filter="icmpv6.type==134")
        asyncio.get_child_watcher().attach_loop(capture.eventloop)
        
        advt_packet = None
        for packet in capture.sniff_continuously(packet_count=5000):
            
            if 'Advertisement' in str(packet):
                print(packet)  
                advt_packet = packet
                break
        return_dict['value'] = advt_packet


    def icmpv6_router_advt_flag_m_o(self, flask_username):
        # self.eth_interfaces_down()
        global interface_name 
        interface_name = self.get_interface(self._address_ip)
        print(interface_name)
        # time.sleep(5)
        
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=self.capture_adv_pkt, args=(return_dict,))
        p.start()
        p.join()
        advt_packet = [v for v in return_dict.values()][0]
        print(str(advt_packet))

        try:
            pkt_fields = advt_packet.icmpv6._all_fields
            flag_ra = pkt_fields['icmpv6.nd.ra.flag']
            flag_managed_address_config = pkt_fields['icmpv6.nd.ra.flag.m']
            flag_other_config = pkt_fields['icmpv6.nd.ra.flag.o']
            if (flag_ra == '0x00000048' and flag_managed_address_config == '0' and flag_other_config == '1'):
                self._dict_result.update({"obs": f'Router Advertisement packet flags -> ra: {flag_ra}, managed:{flag_managed_address_config}, other:{flag_other_config}', 
                "result":'passed', 
                "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'Router Advertisement packet flags -> ra: {flag_ra}, managed:{flag_managed_address_config}, other:{flag_other_config}'})
        except Exception as e:
            self._dict_result.update({"obs": str(e)})
        finally:
            # self.eth_interfaces_up()
            return self._dict_result
    #{'icmpv6.type': '134', 'icmpv6.code': '0', 'icmpv6.checksum': '24792', 'icmpv6.checksum_bad': '0', 'icmpv6.nd.ra.cur_hop_limit': '64', 'icmpv6.nd.ra.flag': '72', 'icmpv6.nd.ra.flag.m': '0', 'icmpv6.nd.ra.flag.o': '1', 'icmpv6.nd.ra.flag.h': '0', 'icmpv6.nd.ra.flag.prf': '1', 'icmpv6.nd.ra.flag.p': '0', 'icmpv6.nd.ra.flag.rsv': '0', 'icmpv6.nd.ra.router_lifetime': '180', 'icmpv6.nd.ra.reachable_time': '0', 'icmpv6.nd.ra.retrans_timer': '0', 'icmpv6.opt': 'ICMPv6 Option (Prefix information : 2804:431:c7c7:5016::/64)', 'icmpv6.opt.type': '3', 'icmpv6.opt.length': '4', 'icmpv6.opt.prefix.length': '64', 'icmpv6.opt.prefix.flag': '192', 'icmpv6.opt.prefix.flag.l': '1', 'icmpv6.opt.prefix.flag.a': '1', 'icmpv6.opt.prefix.flag.r': '0', 'icmpv6.opt.prefix.flag.reserved': '0', 'icmpv6.opt.prefix.valid_lifetime': '259200', 'icmpv6.opt.prefix.preferred_lifetime': '172800', 'icmpv6.opt.reserved': 'Reserved', 'icmpv6.opt.prefix': '2804:431:c7c7:5016::', 'icmpv6.opt.route_info.flag': '8', 'icmpv6.opt.route_info.flag.route_preference': '1', 'icmpv6.opt.route_info.flag.reserved': '0', 'icmpv6.opt.route_lifetime': '172800', 'icmpv6.opt.rdnss.lifetime': '4294967295', 'icmpv6.opt.rdnss': 'fe80::cab4:22ff:fee6:8670', 'icmpv6.opt.mtu': '1492', 'icmpv6.opt.linkaddr': 'c8:b4:22:e6:86:70', 'icmpv6.opt.src_linkaddr': 'c8:b4:22:e6:86:70'}
    #{'icmpv6.type': '136', 'icmpv6.code': '0', 'icmpv6.checksum': '20864', 'icmpv6.checksum_bad': '0', 'icmpv6.nd.na.flag': '1073741824', 'icmpv6.nd.na.flag.r': '0', 'icmpv6.nd.na.flag.s': '1', 'icmpv6.nd.na.flag.o': '0', 'icmpv6.nd.na.flag.rsv': '0', 'icmpv6.nd.na.target_address': '2804:431:c7c7:5016:d9fc:f1b4:c56b:651f'}
#####


# 184
    def capture_dhcpv6(self, return_dict):
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        capture = pyshark.LiveCapture(eventloop=loop, interface=interface_name, display_filter="dhcpv6")
        asyncio.get_child_watcher().attach_loop(capture.eventloop)
        
        advt_packet = None
        
        for packet in capture.sniff_continuously(packet_count=5000):
            str_packet = str(packet)
            if 'DHCPV6' in str_packet and 'Status Code' in str_packet:
                print("\n"*10, packet)  
                advt_packet = packet
                break
            else:
                print("Erro no teste", packet)  
        return_dict['value'] = advt_packet


    def dhcpv6_dhclient_no_avail(self, flask_username):
        global interface_name 
        interface_name = self.get_interface(self._address_ip)
        subprocess.Popen(f'echo 4ut0m4c40 | sudo -S dhclient -v -N {interface_name}', shell=True)
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=self.capture_dhcpv6, args=(return_dict,))
        p.start()
        p.join()
                
        advt_packet = [v for v in return_dict.values()][0]
        # print(str(advt_packet))

        try:
            pkt_fields = advt_packet.dhcpv6._all_fields
            print(str(pkt_fields))
            status_code = pkt_fields['dhcpv6.status_code'] 
            
            if (status_code == '2'): # NoAddrAvail
                self._dict_result.update({"obs": f'DHCPv6 Advertise Status Code: NoAddrAvail {status_code}', 
                "result":'passed', 
                "Resultado_Probe":"OK"})
            else:
                self._dict_result.update({"obs": f'DHCPv6 Advertise Status Code: {status_code}'})
        except Exception as e:
            self._dict_result.update({"obs": str(e)})
        finally:
            pid_list = os.popen('ps -aux | grep dhclient').readlines()
            for pid in pid_list:
                pid = list(filter(None, pid.split(' ')))
                os.system(f'echo 4ut0m4c40 | sudo -S kill -9 {pid[1]}')
            return self._dict_result
#####