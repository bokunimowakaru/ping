# ping: ICMP Ping Code Examples for Raspberry Pi, Raspberry Pi Pico, and ESP32

ICMP Ping の送信や受信を行うサンプル・プログラムです。  
This repository contains ICMP Ping examples for leaning Ping protocol.  

* icmp_ping.py
* icmp_logger.py
* icmp_sender.py

## Language

Select a language to translate this page:

* [Japanese(日本語)](https://translate.google.com/website?sl=en&tl=ja&hl&u=https://git.bokunimo.com/ping/)
* [English(英語)](https://git.bokunimo.com/ping/)

## Usage for Raspberry Pi  

The ".py" example files on the root directory are for Raspberry Pi OS and the other Linux distributions. I tested them on Ubuntu 22 and Debian 11.  
These files are needed the super user privileges.  So, please add a "sudo" command to the beginning of these files to run.  

	pi@raspberry:~/ping $ sudo ./icmp_ping.py  
	ICMP Ping Sender Receiver  
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

In the "pico" and "esp32" directories, there are also some files coded in MicroPython for Raspberry Pi Pico W, ESP32.  
"icmp_ping.py" and "icmp_sender.py" send ICMP Pings to Google DNS (8.8.8.8).  If you don't like to send out from your LAN to Internet, please modify the IP address in the line of "adr = '8.8.8.8'" to your device on the LAN.  

	adr = '8.8.8.8'         # Google DNS
	adr = '192.168.1.1'     # e.g., Gateway on the LAN

* icmp_ping.py  
* icmp_sender.py  

"icmp_ping_cli.py" and "icmp_ping_srv.py" are for local uses. icmp_ping_srv.py is for the server side, and the other is for the client.  

* icmp_ping_cli.py  
* icmp_ping_srv.py  

## bokunimo.net Blog Site

- 解説ページ(bokunimo.netのブログ内)：  
	[https://bokunimo.net/blog/raspberry-pi/3512/](https://bokunimo.net/blog/raspberry-pi/3512/)  
- Google Translate to English：  
	[https://bokunimo.net/blog/raspberry-pi/3512/](https://bokunimo-net.translate.goog/blog/raspberry-pi/3512/?_x_tr_sl=ja&_x_tr_tl=en)  


## Security of Super User Privileges

The command added 'sudo' works the highest privileges on the system. It means the code behave without any limitations.  
If there are security weaknesses in a code, in software libraries, or in the operating system, and the device meets maliciously attacks, you may have a security accident.  
For improving way of the security for the kind of this code, is to reduce the external inputs and outputs. And checking all of the input data and discarding unwanted messages is one of the most important countermeasures for the security issue.  

## GitHub Pages (This Document)

* [https://git.bokunimo.com/ping/](https://git.bokunimo.com/ping/)

by <https://bokunimo.net>

