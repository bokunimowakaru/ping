# ping: ICMP Ping Code Examples for Raspberry Pi, Raspberry Pi Pico, and ESP32

This repository contains ICMP Ping examples for leaning Ping protocol.  

* icmp_ping.py
* icmp_logger.py
* icmp_sender.py

## Usage

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


## GitHub Pages (This Document)

* [https://git.bokunimo.com/ping/](https://git.bokunimo.com/ping/)

by <https://bokunimo.net>

