# ping: ICMP Ping Code Examples for Raspberry Pi, Raspberry Pi Pico, and ESP32

This repository contains ICMP Ping examples for leaning Ping protocol.  

* icmp_ping.py
* icmp_logger.py
* icmp_sender.py

## Usage for Raspberry Pi  

The ".py" example files on the root directory are for Raspberry Pi OS and the other Linux distributions. I tested them on Ubuntu 22 and Debian 11).  
These files are needed the super user privileges.  So, please add a "sudo" command to the beginning of these files to run.  

	pi@raspberry:~/ping $ sudo ./icmp_ping.py  
	ICMP Ping Sender Reciever  
	Usage: sudo ./icmp_ping.py [ip_address] [data...]  
	send Ping to 127.0.0.1  
	ICMP TX(08) : 08 00 93 c0 e5 b9 7e 85  
	ICMP RX(08) : 00 00 9b c0 e5 b9 7e 85  
	IP Version  = v4  
	IP Header   = 20  
	IP Length   = 28  
	Protocol    = 0x01  
	Source      = 127.0.0.1  
	Destination = 127.0.0.1  
	ICMP Length = 8  
	ICMP Type   = 00  
	ICMP Code   = 00  
	Checksum    = Passed  
	Identifier  = e5b9  
	Sequence N  = 7e85  

## Usage for Raspberry Pi Pico W, ESP32 (MicroPython)

In the "pico" directory, there are also some files coded in MicroPython for Raspberry Pi Pico W, ESP32.  
They send ICMP Pings to Google DNS (8.8.8.8).  If you don't like to send out from your LAN, please modify the IP address in the line of "adr = '8.8.8.8'" to your device on the LAN.  

	adr = '8.8.8.8'         # Google DNS
	adr = '192.168.1.1'     # e.g. Gateway on the LAN

## GitHub Pages (This Document)

* [https://git.bokunimo.com/ping/](https://git.bokunimo.com/ping/)

by <https://bokunimo.net>

