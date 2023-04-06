# coding: utf-8
# ICMPを送信する for ESP32 MicroPython
# Copyright (c) 2023 Wataru KUNINO

# ICMPを送信します。

SSID = "1234ABCD"                               # 無線LANアクセスポイント SSID
PASS = "password"                               # パスワード

import network                                  # ネットワーク通信
import socket
from machine import Pin                         # machineのPinを組み込む
from utime import sleep                         # μtimeからsleepを組み込む

adr = '8.8.8.8'         # Google DNS
icm_type = b'\x08'      # header[0] Type = echo message
icm_code = b'\x00'      # header[1] Code = 0
icm_csum = b'\x00\x00'  # header[2:4] Checksum = 0x0000 計算前の初期値
icm_idnt = b'\x12\x34'  # header[4:6] Identifier
icm_snum = b'\x00\x00'  # header[6:8] Sequence Number

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

print('ICMP Sender')                            # タイトル表示
body = '0123456789ABCDEF'
led = Pin(2, Pin.OUT)                           # ESP32 LED用ledを生成

wlan = network.WLAN(network.STA_IF)             # 無線LAN用のwlanを生成
wlan.active(True)                               # 無線LANを起動
wlan.scan()                                     # Scan for available access points
wlan.connect(SSID, PASS)                        # 無線LANに接続
while not wlan.isconnected():                   # 接続待ち
    print('.', end='')                          # 接続中表示
    led.toggle()                                # LEDの点灯／非点灯の反転
    sleep(1)                                    # 1秒間の待ち時間処理
print(wlan.ifconfig()[0])                       # IPアドレスを表示
print('send Ping "'+body+'" to',adr)

while True:
    # Header の生成
    sequence = int.from_bytes(icm_snum,'big')
    sequence += 1
    icm_snum =  sequence.to_bytes(2, 'big')         # Sequence Number
    header = icm_type + icm_code + icm_csum + icm_idnt + icm_snum

    # Checksum の計算
    payload = header + body.encode()
    checksum = checksum_calc(payload)

    # Header にChecksumを付与
    header = icm_type + icm_code + checksum + icm_idnt + icm_snum
    payload = header + body.encode()

    led.value(1)                                    # LEDをONにする
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
    except Exception as e:                          # 例外処理発生時
        while True:
            print(e)                                # エラー内容を表示
            sleep(3)                                # 3秒の待ち時間処理
    print('ICMP TX('+('{:02x}'.format(len(payload)))+')',end=' : ')
    for c in payload:
        print('{:02x}'.format(c), end=' ')          # 受信データを表示
    print()
    sock.sendto(payload,(adr,0))                    # Ping送信
    # sock.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
    sock.settimeout(1)
    while sock:
        try:
            icmp = sock.recv(256)                   # 受信データの取得
        except Exception as e:                      # 例外処理発生時
            print(e)                                # エラー内容を表示
            break
        if icmp[0] == 0x45 and icmp[9] == 0x01 and icmp[20] == 0x00\
          and int.from_bytes(icmp[24:26], 'big') == int.from_bytes(icm_idnt,'big')\
          and int.from_bytes(icmp[26:28], 'big') == int.from_bytes(icm_snum,'big')\
          and  not int.from_bytes(checksum_calc(icmp[20:]),'big'):
            print("Passed")
            break
    sock.close()                                    # ソケットの切断
    led.value(0)                                    # LEDをOFFにする
    sleep(30)                                       # 30秒間の待ち時間処理

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
