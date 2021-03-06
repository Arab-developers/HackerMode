import subprocess
from  optparse import *
import re,sys,os

class MacChanger():
	""" This class is provided to change the mac address for the devices """
	def __init__(self):
		self.mp = OptionParser('''\033[1;32m
 -m  --mac 	 :	the mac address you want to change to
 -i  --interface :	the interface for the mac address
 -d  --default	 :	reset the mac address to the origin
 -h  --help	 :	show this help menu

Examples:
	\033[1;35m[default interface : eth0]\033[1;32m
	chmac -m 64:A1:B7:44:22:63 -i wlan0
	chmac -m 64:A1:B7:44:22:63
\033[0m					 ''' )

		self.mp.add_option("-m","--mac",dest="maca",type="string",help="the mac address you want to change to")
		self.mp.add_option("-i","--interface",dest="inter",type="string",help="the interface for the mac address")
		self.mp.add_option("-d","--default",dest="de",action="store_true",help="reset mac address to the origin mac address")
		self.options,self.args = self.mp.parse_args()

	def check(self,mac):
		pattern  =  r"^\w\w:\w\w:\w\w:\w\w:\w\w:\w\w$"
		self.mac=re.match(pattern,mac)
		if self.mac:
			self.mac=self.mac.group()
			print(mac)
		else:print(f'\033[1;31mInvald Mac Address | {mac}\033[0m');exit()

	def change(self,interface="eth0"):
		print(interface)
		i1 = subprocess.check_output(["ifconfig" , interface])
		print(i1)
		subprocess.call(["ifconfig",interface,"down"])
		subprocess.call(["ifconfig",interface,"hw","ether",self.mac])
		subprocess.call(["ifconfig",interface,"up"])
		i2 = subprocess.check_output(["ifconfig" , interface])
		if i1==i2:print("\033[1;31m[!] Failed to change Mac address..!\033[0m")
		else:print("\033[1;34m[+] Mac address changed successfully\033[0m")

	def run(self):
		if self.options.maca == None and '-d' not in sys.argv[1:]:
			print(self.mp.usage)
		if '-d' in sys.argv[1:]:
			inter = self.options.inter if self.options.inter else "eth0"
			com = "ifconfig %s hw ether $(ethtool -P %s | awk '{print $3}')"%(inter,inter)
			os.system(com)
		if self.options.maca:
			self.mac = self.options.maca
			if self.options.inter:
				self.check(self.options.maca)
				self.change(self.options.inter)
			else:
				self.check(self.options.maca)
				self.change()


if __name__ == '__main__':
	if os.geteuid() == 0:
		MacChanger().run()
	else:print("\033[1;31m#[!] This Tool should be runing with root privilege\033[0m")
