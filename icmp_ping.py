#!/usr/bin/env python3
# coding: utf-8
# ICMPを送信する
# Copyright (c) 2023 Wataru KUNINO

# ICMPを送信します。
# sudo ./icmp_ping.py

# 第1引数は宛先IPアドレスです。
# sudo ./icmp_ping.py 127.0.0.1

# 第2引数以降は送信データです。
# sudo ./icmp_ping.py 127.0.0.1 data1 data2...

import sys
import socket
import ipaddress
from time import time
from random import randint

adr = '127.0.0.1'
icm_type = b'\x08'      # header[0] Type = echo message
icm_code = b'\x00'      # header[1] Code = 0
icm_csum = b'\x00\x00'  # header[2:4] Checksum = 0x0000 計算前の初期値
icm_idnt = b'\x00\x04'  # header[4:6] Identifier
icm_snum = b'\x00\x01'  # header[6:8] Sequence Number

def checksum_calc(payload):
    if len(payload)%2 == 1:
        payload += b'\x00'  # total length is odd, padded with one octet of zeros
    sum = 0x0000
    for i in range(len(payload)//2):    #  1 の補数和
        sum += int(payload[i*2]) * 256
        sum += int(payload[i*2+1])
        if sum > 0xFFFF:
            sum += 1
            sum &= 0xFFFF
    sum = ~(sum) & 0xFFFF
    return sum.to_bytes(2, 'big')

argc = len(sys.argv)                                    # 引数の数をargcへ代入
print('ICMP Ping Sender Reciever')                      # タイトル表示
print('Usage: sudo',sys.argv[0],'[ip_address] [data...]') # 使用方法
if argc >= 2:                                           # 入力パラメータ数の確認
    try:
        ipaddress.ip_interface(sys.argv[1])
        adr = sys.argv[1]                                   # IPアドレスを設定
        del sys.argv[1]
    except ValueError:
        pass
body = ''
if argc >= 2:
    for word in sys.argv[1:]:
        if len(body) > 0:
            body += ' '
        body += word

if len(body) > 0:
    print('send Ping "'+body+'" to',adr)
else:
    print('send Ping to',adr)

# Header の生成
icm_idnt = randint(0,65535).to_bytes(2, 'big')          # Identifier = 乱数
icm_snum =  (int(time()) % 65536).to_bytes(2, 'big')    # Sequence Number = 秒数
header = icm_type + icm_code + icm_csum + icm_idnt + icm_snum

# Checksum の計算
payload = header + body.encode()
checksum = checksum_calc(payload)

# Header にChecksumを付与
header = icm_type + icm_code + checksum + icm_idnt + icm_snum
payload = header + body.encode()

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
except PermissionError:                                 # 例外処理発生時
    print('PermissionError, 先頭に sudo を付与して実行してください')
    exit()                                              # プログラムの終了
if sock:                                                # 作成に成功したとき
    print('ICMP TX('+('{:02x}'.format(len(payload)))+')',end=' : ')
    for c in payload:
        print('{:02x}'.format(c), end=' ')             # 受信データを表示
    print()
    sock.sendto(payload,(adr,0))       # Ping送信
    sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1) #
    sock.settimeout(1)
    while sock:
        try:
            icmp = sock.recv(256)                                        # 受信データの取得
        except socket.timeout:
            break
        length = int(256 * icmp[2] + icmp[3])
        header_length = int((icmp[0]%16)*4)
        protocol = icmp[9]
        source_adr = int.from_bytes(icmp[12:16], 'big')
        source_adr_s = str(ipaddress.IPv4Address(source_adr))
        dest_adr = int.from_bytes(icmp[16:20], 'big')
        dest_adr_s = str(ipaddress.IPv4Address(dest_adr))
        if icmp[0] == 0x45 and protocol == 0x01 and length == len(icmp) and icmp[20] == 0x00:
            icmp_len = length - header_length
            identifier = int.from_bytes(icmp[24:26], 'big')
            sequence = int.from_bytes(icmp[26:28], 'big')
            check = not int.from_bytes(checksum_calc(icmp[20:]),'big')
            if identifier == int.from_bytes(icm_idnt,'big') and sequence == int.from_bytes(icm_snum,'big') and check:
                # icmp[0] == 0x45: IPv4と、IPヘッダ長20バイトに限定
                print('ICMP RX('+'{:02x}'.format(icmp_len)+')',end=' : ')
                for i in range(len(icmp)-len(payload),len(icmp)):
                    print('{:02x}'.format(icmp[i]), end=' ')               # 受信データを表示
                print()
                print('IP Version  =','v'+str(int(icmp[0]>>4)))
                print('IP Header   =',header_length)
                print('IP Length   =',length)
                print('Protocol    =','0x'+('{:02x}'.format(protocol)))
                print('Source      =',source_adr_s)
                print('Destination =',dest_adr_s)
                print('ICMP Length =',icmp_len)
                print('ICMP Type   =','{:02x}'.format(icmp[20]))
                print('ICMP Code   =','{:02x}'.format(icmp[21]))
                print('Checksum    =', 'Passed' if check else 'Failed')
                print('Identifier  =','{:04x}'.format(identifier))
                print('Sequence N  =','{:04x}'.format(sequence))
                if icmp_len > 8:
                    print('ICMP Data   =',icmp[28:].decode())
    sock.close()                                                # ソケットの切断

###############################################################################
# 参考文献 RAWソケットを利用したpingコマンド (Geekなページ)
'''
    https://www.geekpage.jp/programming/linux-network/book/12/12-1.php
'''

###############################################################################
# 参考文献 TCP/IP - ICMPとは (ネットワークエンジニアとして)
'''
    https://www.infraexpert.com/study/tcpip4.html
'''

###############################################################################
# 参考文献 INTERNET CONTROL MESSAGE PROTOCOL (IETF RFC 792)
'''
    https://www.rfc-editor.org/rfc/rfc792


Echo or Echo Reply Message

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Type      |     Code      |          Checksum             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Identifier          |        Sequence Number        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Data ...
   +-+-+-+-+-

   IP Fields:

   Addresses

      The address of the source in an echo message will be the
      destination of the echo reply message.  To form an echo reply
      message, the source and destination addresses are simply reversed,
      the type code changed to 0, and the checksum recomputed.

   IP Fields:

   Type

      8 for echo message;

      0 for echo reply message.

   Code

      0

   Checksum

      The checksum is the 16-bit ones's complement of the one's
      complement sum of the ICMP message starting with the ICMP Type.
      For computing the checksum , the checksum field should be zero.
      If the total length is odd, the received data is padded with one
      octet of zeros for computing the checksum.  This checksum may be
      replaced in the future.

   Identifier

      If code = 0, an identifier to aid in matching echos and replies,
      may be zero.

   Sequence Number

      If code = 0, a sequence number to aid in matching echos and
      replies, may be zero.

   Description

      The data received in the echo message must be returned in the echo
      reply message.

      The identifier and sequence number may be used by the echo sender
      to aid in matching the replies with the echo requests.  For
      example, the identifier might be used like a port in TCP or UDP to
      identify a session, and the sequence number might be incremented
      on each echo request sent.  The echoer returns these same values
      in the echo reply.

      Code 0 may be received from a gateway or a host.
'''

###############################################################################
# 参考文献 INTERNET PROTOCOL (IETF RFC 791)
'''
    https://www.rfc-editor.org/rfc/rfc791
    
    3.1.  Internet Header Format

      A summary of the contents of the internet header follows:


        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |Version|  IHL  |Type of Service|          Total Length         |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |         Identification        |Flags|      Fragment Offset    |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |  Time to Live |    Protocol   |         Header Checksum       |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                       Source Address                          |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                    Destination Address                        |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                    Options                    |    Padding    |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

'''
###############################################################################
# 参考文献 python raw socket: Protocol not supported (stackoverflow)
'''
    https://stackoverflow.com/questions/19732145/python-raw-socket-protocol-not-supported
'''
