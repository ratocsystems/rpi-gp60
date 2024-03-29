#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#   RPi-GP60 サンプルプログラム
#   "sampleGp60.py"
#   2018/12/07 R1.0
#   2020/03/24 R1.1 初期値としてRTS=Falseを明示
#   2024/03/15 RPI.GPIO の代わりに gpoid を使用
#
#   RATOC Systems, Inc. Osaka, Japan
#
#   このサンプルを実行する前にシリアルドライバ設定が必要です。
#
#   a) config.txt を編集する。
#      $ sudo nano /boot/firmware/config.txt
#
#    * Raspberry Pi 5 から /boot/config.txt は /boot/firmware/config.txt へ移動されました。
#
#   b) 次の２行を config.txt の最終行へ追加する。
#      gpio=27=op,dh
#      dtoverlay=sc16is752-i2c,int_pin=17,addr=0x4d,xtal=14745600
#
#   修正後は、システムを再起動してください。
#


import sys
import os
import time
import argparse
import math
# import RPi.GPIO as GPIO #GPIO制御用
import gpiod            #GPIO制御用
import serial
import serial.rs485

# グローバル変数
gpioChip = 'gpiochip4'           # gpiomem device for Raspberry Pi 5
GP60_POWER = 27

port0 = "/dev/ttySC0"   # Port0 のデバイス名
baud0 = 9600            # 初期値 9600 
port1 = "/dev/ttySC1"   # Port1 のデバイス名
baud1 = 9600

    # GPIO終了処理
def close_GP60():
    print("RPi-GP60の使用を終了します")
    # 再度、gp10_power_line を取得、出力設定しないと set_value(0)が実行できない
    chip = gpiod.Chip(gpioChip)  # GP6O デバイスを開く
    gp60_power_line = chip.get_line(GP60_POWER)
    gp60_power_line.request(consumer="GP60_POWER", type=gpiod.LINE_REQ_DIR_OUT)
    gp60_power_line.set_value(0)  # RPi-GP60 絶縁電源 OFF <<< GPIO.output(27,False)
    chip.close()                  # <<< GPIO.cleanup()
    sys.exit()

    # RPi-GP60初期化
def init_GP60():
    try:
        chip = gpiod.Chip(gpioChip)  # GPIO デバイスを開く
                        # <<< GPIO.setmode(GPIO.BCM)    # GPIO番号で指定/Use Broadcom pin numbering
    except gpiod.Error as e:
        print(gpioChip + "open error:", e)
        sys.exit()

    # RPi-GP60 絶縁回路用電源 ON  <<< GPIO.setup(27,   GPIO.OUT, initial=GPIO.HIGH )
    gp60_power_line = chip.get_line(GP60_POWER)
    gp60_power_line.request(consumer="GP60_POWER", type=gpiod.LINE_REQ_DIR_OUT)
    gp60_power_line.set_value(1)
    time.sleep(0.5)                                       # 電源安定待ち

# シリアル設定情報変更
# 各パラメータの詳細についてはpyserialを参照
# https://pythonhosted.org/pyserial/pyserial_api.html#serial.Serial
def input_param( ser ):
    print( "設定値を入力 enter:変更なし >" )
    i=input(" baudrate(300,1200,2400,4800,9600,14400,19200,38400,57600,115200,230400,460800,921600) = ")
    if( len(i) ):
        ser.baudrate = int(i)         # ボーレート[bps]設定変更
    i=input(" bytesize(5, 6, 7, 8) = ")
    if( len(i) ):
        ser.bytesize = int(i)         # バイト長[bit]設定変更
    i=input(" parity('N','E','O','S','M') = ")
    if( len(i) ):
        ser.parity = i                # パリティ[なし,奇数,偶数,スペース,マーク]設定変更
    i=input(" stopbits(1, 1.5, 2) = ")
    if( len(i) ):
        ser.stopbits = float(i)       # ストップビット長[bit]設定変更
    i=input(" timeout = ")
    if( len(i) ):
        ser.timeout = float(i)        # タイムアウト[sec]設定変更
    i=input(" xonxoff(False, True) = ")
    if( len(i) ):
        ser.xonoff = i                # Xon/Xoff制御 設定変更
    i=input(" rtscts(False, True) = ")
    if( len(i) ):
        ser.rtscts = i                # RTS/CTS制御 設定変更
    i=input(" dsrdtr(False, True) = ")
    if( len(i) ):
        ser.dsrdtr = i                # DSR/DTR制御 設定変更


# メイン
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog='sampleGp60.py',          #プログラムファイル名
                usage='RPi-GP60のサンプルプログラム', #使用方法
                description='引数なし',
                epilog=     '--------------------------------------------------------------------------',
                add_help=True,
                )

    try:
        # RPi-GP60初期化
        init_GP60()

        print( "RPi-GP60 サンプルプログラム" )
        key = 1

        s0 = serial.Serial() # Port0
        s0.port = port0
        s0.timeout = 0.5
        s1 = serial.Serial() # Port1
        s1.port = port1
        s1.timeout = 0.5

        s0.rtscts=False
        s0.dsrdtr=False
        s0.rts=False
        s0.dtr=False
        s1.rtscts=False
        s1.dsrdtr=False
        s1.rts=False
        s1.dtr=False

        while( key != 0 ):
            i = input( "1:送受信テスト(RS232/RS422全二重) 2:1:送受信テスト(RS485半二重) 3:設定 0:終了 > " )
            if( len(i) == 0 ):      # Enterのみなら、
                continue            # メニュー再表示
            key = int(i,10)
            if( key == 0 ):         # '0'なら、
                break               # プログラム終了

            # 送受信のテスト
            if( (key == 1)or(key == 2) ):         # '1'または'2'なら、送受信テスト
                # [RS232またはRS422全二重モードの設定]
                # 基板上のジャンパを、[RS232]または[RS-422の全二重で受信両端の終端抵抗をON]に設定する。

                # [RS485モードの設定]
                # 基板上のジャンパを、[RS-485の半二重で両端の終端抵抗をON]に設定する。

                stx = input( "送信ポート番号(0, 1) enter:戻る > " ) # 送信ポート番号
                if( len(stx)==0 ):                                  # Enterのみの場合はメニューに戻る。
                    continue
                srx = input( "受信ポート番号(0, 1) enter:戻る > " ) # 受信ポート番号
                if( len(srx)==0 ):                                  # Enterのみの場合はメニューに戻る。
                    continue
                try:
                    s0.open() # Port0 オープン
                    s1.open() # Port1 オープン
                except Exception as e:
                    print( "シリアルポートのオープンに失敗しました", e)
                    break

                if( key == 1 ):   # '1'なら、全二重の設定
                    # RPi-GP60のRS422では、TXDENにRTS信号を使用。全二重で通信するにはRTSを常にFalse状態とする。
                    if(s0.rtscts==False):
                        s0.rts=False
                    if(s1.rtscts==False):
                        s1.rts=False

                if( key == 2 ):   # '2'なら、RS485モードの設定
                    # RPi-GP60ではRTSの設定を、(rts_level_for_tx=False, rts_level_for_rx=True)とする。
                    # ループバックは(loopback=False)でも、半二重設定だと送信データはエコーバックされる。
                    # RPi-GP60のRS485ドライバはハードウェアでネイティブに制御されるので、(delay_before_tx=None, delay_before_rx=None)とする。
                    s0.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=False, rts_level_for_rx=True, loopback=False, 
                                                               delay_before_tx=None, delay_before_rx=None)
                    s1.rs485_mode = serial.rs485.RS485Settings(rts_level_for_tx=False, rts_level_for_rx=True, loopback=False, 
                                                               delay_before_tx=None, delay_before_rx=None)

                while( 1 ):     # キー入力した文字列送信と、受信バッファの文字列表示を繰り返す
                    txd = input( "送信データ入力 enter:戻る > " )   # 送信文字列を入力する
                    if( len(txd)==0 ):                              # Enterのみの場合はメニューに戻る。
                        if( key == 2 ):   # '2'ならRS485モードの設定解除
                            s0.rs485_mode = None    # RS485モード解除
                            s1.rs485_mode = None    # RS485モード解除
                        s0.close()        # Port0 クローズ
                        s1.close()        # Port1 クローズ
                        break
                    if( stx=='0' ):       # 送信
                        s0.write( txd.encode('utf-8')+b'\n' )       # Port0 1行文字列をバイト列へ変換しシリアル送信
                    else:
                        s1.write( txd.encode('utf-8')+b'\n' )       # Port1 1行文字列をバイト列へ変換しシリアル送信
                    while( 1 ):           # 受信
                        if( srx=='0' ):
                            line = s0.readline()    # Port0 1行シリアル受信バイト列
                        else:
                            line = s1.readline()    # Port1 1行シリアル受信バイト列
                        if( len(line)==0 ):         # 受信データがなくなるまで受信繰り返す
                            break
                        print( "受信データ："+line.decode('utf-8') )    # 受信バイト列を文字列へ変換し表示

            # 設定
            if( key == 3 ):         # '3'なら、シリアル設定変更
                print( "[Port0 現在の設定]" )
                print( s0 )         # Port0 の現在の設定情報表示
                input_param( s0 )   # Port0 の設定情報入力し変更

                print( "[Port1 現在の設定]" )
                print( s1 )         # Port1 の現在の設定情報表示
                input_param( s1 )   # Port1 の設定情報入力し変更

        print( "終了します" )

    except KeyboardInterrupt:       # CTRL-C キーが押されたら、
         print( "中断しました" )    # 中断
#    except Exception:               # その他の例外発生時
         print( "エラー" )          # エラー

    close_GP60()
#    GPIO.output(27, False)          # RPi-GP60の絶縁電源OFF
#    GPIO.cleanup()
    sys.exit()
