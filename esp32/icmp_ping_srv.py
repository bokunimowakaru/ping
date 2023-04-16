# coding: utf-8
# ICMPでPingを受信・応答する Ping Server for ESP32 MicroPython
# Copyright (c) 2023 Wataru KUNINO

# ICMPでPingの受信と応答を行います。

SSID = "1234ABCD"                               # 無線LANアクセスポイント SSID
PASS = "password"                               # パスワード

import network                                  # ネットワーク通信
import socket
from machine import Pin                         # machineのPinを組み込む
from utime import sleep                         # μtimeからsleepを組み込む

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

print('ICMP Ping Server')                       # タイトル表示
led = Pin(2, Pin.OUT)                           # ESP32 LED用ledを生成

wlan = network.WLAN(network.STA_IF)             # 無線LAN用のwlanを生成
wlan.active(True)                               # 無線LANを起動
if (wlan.isconnected()): #  maybe not necessary
    wlan.disconnect()
wlan.scan()                                     # Scan for available access points
wlan.connect(SSID, PASS)                        # 無線LANに接続
while not wlan.isconnected():                   # 接続待ち
    print('.', end='')                          # 接続中表示
    led.value(not led.value())                  # LEDの点灯／非点灯の反転
    sleep(1)                                    # 1秒間の待ち時間処理
print(wlan.ifconfig()[0])                       # IPアドレスを表示

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
    except Exception as e:                          # 例外処理発生時
        while True:
            print(e)                                # エラー内容を表示
            sleep(3)                                # 3秒の待ち時間処理
    while sock:
        try:
            icmp = sock.recv(256)                   # 受信データの取得
        except Exception as e:                      # 例外処理発生時
            print(e)                                # エラー内容を表示
            break
        length = int(256 * icmp[2] + icmp[3])
        header_length = int((icmp[0]%16)*4)
        protocol = icmp[9]
        source_adr_s = str(icmp[12])+'.'+str(icmp[13])+'.'+str(icmp[14])+'.'+str(icmp[15])
        dest_adr_s = str(icmp[16])+'.'+str(icmp[17])+'.'+str(icmp[18])+'.'+str(icmp[19])
        if icmp[0] == 0x45 and protocol == 0x01 and length >= header_length + 8 and icmp[20]:
            icm_type = icmp[header_length+0]                    # header[0] Type = echo message
            icm_code = icmp[header_length+1]                    # header[1] Code = 0
            icm_csum = icmp[header_length+2:header_length+4]    # header[2:4] Checksum = 0x0000 計算前の初期値
            icm_idnt = icmp[header_length+4:header_length+6]    # header[4:6] Identifier
            icm_snum = icmp[header_length+6:header_length+8]    # header[6:8] Sequence Number
            icmp_len = length - header_length
            identifier = int.from_bytes(icm_idnt, 'big')
            sequence = int.from_bytes(icm_snum, 'big')
            check = not int.from_bytes(checksum_calc(icmp[20:]),'big')
            if check:
                led.value(1)                                    # LEDをONにする
                print('ICMP RX('+'{:02x}'.format(icmp_len)+')',end=' : ')
                for i in range(header_length,len(icmp)):
                    print('{:02x}'.format(icmp[i]), end=' ')               # 受信データを表示
                print()
                print('IP Version  =','v'+str(int(icmp[0]>>4)))
                print('IP Header   =',header_length)
                print('IP Length   =',length)
                print('Protocol    =','0x'+('{:02x}'.format(protocol)))
                print('Source      =',source_adr_s)
                print('Destination =',dest_adr_s)
                print('ICMP Length =',icmp_len)
                print('ICMP Type   =','{:02x}'.format(icm_type))
                print('ICMP Code   =','{:02x}'.format(icm_code))
                print('Checksum    =', 'Passed' if check else 'Failed')
                print('Identifier  =','{:04x}'.format(identifier))
                print('Sequence N  =','{:04x}'.format(sequence))

                # Header の生成
                icm_type = b'\x00'  # Echo Reply
                icm_csum = b'\x00\x00'  # reset check sum. 
                header = icm_type + icm_code.to_bytes(1,'big') + icm_csum + icm_idnt + icm_snum

                # Checksum の計算
                payload = header + icmp[28:]
                checksum = checksum_calc(payload)

                # Header にChecksumを付与
                header = icm_type + icm_code.to_bytes(1,'big') + checksum + icm_idnt + icm_snum
                payload = header + icmp[28:]
                print('ICMP TX('+('{:02x}'.format(len(payload)))+')',end=' : ')
                for c in payload:
                    print('{:02x}'.format(c), end=' ')          # 送信データを表示
                print()
                try:
                    sock.sendto(payload,(source_adr_s,0))   # Ping応答
                except Exception as e:                      # 例外処理発生時
                    print(e)                                # エラー内容を表示
                break

    sock.close()                                    # ソケットの切断
    led.value(0)                                    # LEDをOFFにする

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
'''

###############################################################################
# 参考文献 INTERNET PROTOCOL (IETF RFC 791)
'''
    https://www.rfc-editor.org/rfc/rfc791
'''
###############################################################################
# 参考文献 python raw socket: Protocol not supported (stackoverflow)
'''
    https://stackoverflow.com/questions/19732145/python-raw-socket-protocol-not-supported
'''
###############################################################################
# 参考文献 MicroPython Forum / WiFi re-connect problem
'''
    https://forum.micropython.org/viewtopic.php?t=12294
'''
