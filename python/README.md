# RPi-GP60用Pythonサンプルファイル

RPi-GP60用Pythonサンプルファイルの使用方法について説明します。  
Raspberry Piは'Raspberry Pi3 ModelB'、OSは'Raspbian Stretch with desktop(NOOBS:2018-03-14)'で説明します。  
サンプルファイルは`sampleGp60.py`です。  

  
***
## 準備  
### Raspberry PiにRPi-GP60を接続  
下記の準備をおこなってください。  
- [OS(`RASPBIAN`)のインストール](../install/README.md#raspbianのインストール)  
- [GPIO40pinのI2C設定](../install/README.md#i2cの有効設定)  
- ['Raspberry Pi'に'RPi-GP60'を接続](../setup/README.md#rpi-gp60の設定と装着)  
- [シリアルドライバの設定](/setup/README.md#4-シリアルドライバ設定)  

### Pythonサンプルファイルを実行するディレクトリを作成  
1. 'mkdir'コマンドを使って'RPi-GP60'という名前のディレクトリを作成します。(ディレクトリ名や作成場所は自由です)  
    ```
    $ mkdir RPi-GP60  
    ```

1. 'ls'コマンドを実行して'RPi-GP60'ディレクトリが作成されていること確認します。  
    ```
    $ ls  
    ```

1. 'cd'コマンドで'RPi-GP60'ディレクトリに移動します。  
    ```
    $ cd RPi-GP60  
    ```  
    
### PythonサンプルファイルをGitHubからダウンロード    
GitHubからPythonサンプルファイルをダウンロードします。  
1. sampleGp60.pyをダウンロード  
    ```
    $ wget https://github.com/ratocsystems/rpi-gp60/raw/master/python/sampleGp60.py  
    ```  

1. `ls`コマンドを実行してPythonサンプルファイル`sampleGp60.py`がダウンロードされていることを確認します。  
    ```
    $ ls  
    sampleGp60.py  
    ```
  
***
## Pythonサンプルファイルについて  
  
`sampleGp60.py`  

RPi-GP60を使用してシリアルの送受信を行うPythonサンプルプログラムです。  
サンプルプログラムでは下記の処理を行っています。  

1. **RPi-GP60の初期設定 init_GP60()**  
    GPIOの初期設定を行います。  
    ※<u>ハードウェアに依存する設定ですので変更しないでください。</u>  
    - GPIOをGPIO番号で指定するように設定  
    - 絶縁回路用電源をONに設定   
        電源ON後、安定するまで待ちます。  

1. **シリアル設定情報変更 input_param( serial )**  
    [pyserialモジュール](https://pythonhosted.org/pyserial/pyserial_api.html#serial.Serial)のシリアル設定パラメータを入力値へ設定変更します。  
    以下のパラメータを指定可能です。変更しない場合はenterのみを入力してください。
    - ボーレート[bps]  
    - バイト長[bit]  
    - パリティ[なし,奇数,偶数,スペース,マーク]  
    - ストップビット長[bit]  
    - 受信タイムアウト時間[sec]  
    - フロー制御 XON/XOFF設定[False/True]  
    - フロー制御 RTS/CTS設定[False/True]  
    - フロー制御 DSR/DTR設定[False/True]  

1. **メニュー表示**  
    次のメニューを表示します。  
    `1:送受信テスト(RS232/RS422全二重) 2:1:送受信テスト(RS485半二重) 3:設定 0:終了 > `  

1. **送受信テスト**  
    メニューで1または2が入力された場合は、シリアル送受信テストを行います。  
    送信ポート番号と受信ポート番号(0,1)を入力します。enterのみでメニューに戻ります。  
    `送信ポート番号(0, 1) enter:戻る > `  
    `受信ポート番号(0, 1) enter:戻る > `  
    メニューで2が入力されていればRS485の全二重モード動作(差動ドライバの自動イネーブル制御)を有効にします。  
    `送信データ入力 enter:戻る > `  
    で、送信する文字列を入力します。送信後に受信文字列を表示します。  
    受信は設定されたタイムアウトが発生するまで継続されます。  
    タイムアウト後に、送信データ入力に戻ります。  
    送信データ入力時にenterのみでメニューに戻ります。  

1. **設定**  
    メニューで3が入力された場合は、シリアル設定を変更します。  
    ポート0とポート1についてシリアル設定情報変更 input_param() を行います。  
  
1. **終了**  
    メニューで0が入力された場合は、プログラムを終了します。  

***
## Pythonサンプルファイルの使い方  
サンプルファイル名の前に、`python3`をつけて実行します。  
- **シリアル送受信テスト**    
    `例) ボーレート115200bpsでポート0からポート1へ折り返し送受信テストをする場合`  
    ~~~  
    $ python3 sampleGp60.py  
    RPi-GP60 検査プログラム  
    1:送受信テスト(RS232/RS422全二重) 2:1:送受信テスト(RS485半二重) 3:設定 0:終了 > 3  
    [Port0 現在の設定]  
    Serial<id=0x76a49b90, open=False>(port='/dev/ttySC0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.5, xonxoff=False, rtscts=False, dsrdtr=False)  
    設定値を入力 enter:変更なし >  
     baudrate(300,1200,2400,4800,9600,14400,19200,38400,57600,115200,230400,460800,921600) = 115200  
     bytesize(5, 6, 7, 8) =  
     parity('N','E','O','S','M') =  
     stopbits(1, 1.5, 2) =  
     timeout =  
     xonxoff(False, True) =  
     rtscts(False, True) =  
     dsrdtr(False, True) =  
    [Port1 現在の設定]  
    Serial<id=0x76a49bb0, open=False>(port='/dev/ttySC1', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.5, xonxoff=False, rtscts=False, dsrdtr=False)  
    設定値を入力 enter:変更なし >  
     baudrate(300,1200,2400,4800,9600,14400,19200,38400,57600,115200,230400,460800,921600) = 115200  
     bytesize(5, 6, 7, 8) =  
     parity('N','E','O','S','M') =  
     stopbits(1, 1.5, 2) =  
     timeout =  
     xonxoff(False, True) =  
     rtscts(False, True) =  
     dsrdtr(False, True) =  
    1:送受信テスト(RS232/RS422全二重) 2:1:送受信テスト(RS485半二重) 3:設定 0:終了 > 1  
    送信ポート番号(0, 1) enter:戻る > 0  
    受信ポート番号(0, 1) enter:戻る > 1  
    送信データ入力 enter:戻る > ABCD  
    受信データ：ABCD  
    
    送信データ入力 enter:戻る > EFGH  
    受信データ：EFGH  
    
    送信データ入力 enter:戻る > UUUU  
    受信データ：UUUU
    
    送信データ入力 enter:戻る >  
    1:送受信テスト(RS232/RS422全二重) 2:1:送受信テスト(RS485半二重) 3:設定 0:終了 > 0  
    ~~~   
