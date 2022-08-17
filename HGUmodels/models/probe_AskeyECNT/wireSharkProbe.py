import os
import signal
import subprocess
from ..AskeyECNT import HGU_AskeyECNT
import pyshark
import multiprocessing
import asyncio
import time


class HGU_AskeyECNT_wireSharkProbe(HGU_AskeyECNT):


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
        p.join(timeout=60)

        try:
            advt_packet = [v for v in return_dict.values()][0]
            print(str(advt_packet))
            pkt_fields = advt_packet.icmpv6._all_fields
            flag_ra = pkt_fields['icmpv6.nd.ra.flag']
            print(flag_ra)
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
                # print("\n"*10, packet)  
                advt_packet = packet
                break
            else:
                print("Erro no teste", packet)  
        return_dict['value'] = advt_packet


    def dhcpv6_dhclient_no_avail(self, flask_username):
        global interface_name 
        interface_name = self.get_interface(self._address_ip)
        print(interface_name)
        os.popen(f'echo 4ut0m4c40 | sudo -S dhclient -v -N {interface_name}')#, shell=True, preexec_fn=os.setsid)
        time.sleep(3)   
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=self.capture_dhcpv6, args=(return_dict,))
        p.start()
        p.join(timeout=30)
                            
        try:
            advt_packet = [v for v in return_dict.values()][0]
            # print(str(advt_packet))
            pkt_fields = advt_packet.dhcpv6._all_fields
            print(pkt_fields)
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
####


# 185
    def capture_icmpv6(self, return_dict):
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        capture = pyshark.LiveCapture(eventloop=loop, interface=interface_name, display_filter="icmpv6")
        asyncio.get_child_watcher().attach_loop(capture.eventloop)
        
        advt_packet = None
        
        for packet in capture.sniff_continuously(packet_count=5000):
            str_packet = str(packet)
            # print(str_packet)
            if 'Type: Router Advertisement (134)' in str_packet:
                advt_packet = packet
                break
            else:
                print("Erro no teste", packet)  
        return_dict['value'] = advt_packet


    def router_solicitation(self, flask_username):
        global interface_name 
        interface_name = self.get_interface(self._address_ip)
        print(interface_name)

        endereco_ipv6 = []
        for n in range(0,3):
            router_adv = 0
            print('reiniciando interface')
            os.system(f'echo 4ut0m4c40 | sudo -S ifconfig {interface_name} down')
            time.sleep(2)
            os.system(f'echo 4ut0m4c40 | sudo -S ifconfig {interface_name} up')
            time.sleep(10)
            print('interface reiniciada')

            inet6_raw = os.popen(f'ip addr show {interface_name}').read()
            time.sleep(2)
            for inet6 in inet6_raw.split('\n'):
                if inet6.strip(' ').startswith('inet6'):
                    ipv6 = inet6.strip(' ').split(' ')[1].split('/')[0]
                    print('Endereço IPv6 = ', ipv6)
                    endereco_ipv6.append(ipv6)
                    break

            ping = os.popen(f'ping6 2001:4860:4860::8888 -c 10 -I {interface_name}')
        
            try:
                # print(ping.read().strip(' \n'))
                for pacotes in ping.read().strip(' \n').split('\n'):
                    if pacotes.startswith('10 p'):
                        pacotes_recebidos = pacotes.split(',')[1].strip(' ').split(' ')[0]
                        print(pacotes, pacotes_recebidos)
                        break
                if int(pacotes_recebidos) < 8: 
                    self._dict_result.update({"obs": f'Router Advertisement CheckSum Status NOK: ping < 80%'})
                    break
            except:
                self._dict_result.update({"obs": f'Router Advertisement CheckSum Status NOK: erro no ping 2001:4860:4860::8888 de {ipv6}'})
                break

            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            p = multiprocessing.Process(target=self.capture_icmpv6, args=(return_dict,))
            p.start()
            p.join(timeout=60)
            
            try:
                advt_packet = [v for v in return_dict.values()][0]
                # print(str(advt_packet))
                pkt_fields = advt_packet.icmpv6._all_fields
                # print(pkt_fields)
                router_adv = pkt_fields['icmpv6.checksum.status'] 
                
                if (router_adv == '1'): 
                    self._dict_result.update({"obs": f'Router Advertisement CheckSum Status OK: {pkt_fields}; Endereços recebidos: {endereco_ipv6}', 
                    "result":'passed', 
                    "Resultado_Probe":"OK"})
                else:
                    self._dict_result.update({"obs": f'Router Advertisement CheckSum Status NOK: {pkt_fields}; Endereços recebidos: {endereco_ipv6}'})
                    break
            except Exception as e:
                self._dict_result.update({"obs": str(e), "result":'failed', "Resultado_Probe":"NOK"})
                break
        
        return self._dict_result
#####