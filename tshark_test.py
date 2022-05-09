import pyshark

def capture_adv_pkt():
    capture = pyshark.LiveCapture()
        
    advt_packet = None
    for packet in capture.sniff_continuously(packet_count=1000):
        print(packet)
        if 'Advertisement' in str(packet):  
            advt_packet = packet
            break
    return advt_packet


if __name__ == '__main__':
    capture_adv_pkt()
