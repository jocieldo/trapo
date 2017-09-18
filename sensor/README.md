# TRAPO(Traffic Counter Portable)
センサー・ロガー・モバイルバッテリー
![TRAPO Sensor and Logger](https://raw.githubusercontent.com/kfb01250/trapo/images/TRAPO-sensor-logger.JPG)

ロガー
![TRAPO Logger](https://raw.githubusercontent.com/kfb01250/trapo/images/TRAPO-logger.JPG)

## TRAPOセンサー

### 部品
- [シャープ測距モジュール　GP2Y0A710K][3]
- アルミ角パイプ 20mm x 20mm x 1200mm
- [ゴムブッシュ9φ][8]
- LANケーブル(5mを半分にカット)
- センサーケース(3Dプリント)2個
- キャップ(3Dプリント)2個

### 配線(シャープ測距モジュール = LANケーブル)

センサー1(右)

- 1(黄)GND = 青(4)
- 2(青)Vcc = 白茶(7)
- 3(黒)Vcc = 白茶(7)
- 4(白)Vo  = 白青(5)
- 5(赤)GND = 青(4)

センサー2(左)

- 1(黄)GND = 緑(6)
- 2(青)Vcc = 茶(8)
- 3(黒)Vcc = 茶(8)
- 4(白)Vo  = 白緑(3)
- 5(赤)GND = 緑(6)


### LANケーブルの配線
1. 角パイプを1200mmに切断し穴を開ける。
![pipe](https://raw.githubusercontent.com/kfb01250/trapo/images/pipe.JPG)
2. 真ん中の穴にブッシュゴムを取り付ける。
![rubberbush](https://raw.githubusercontent.com/kfb01250/trapo/images/rubberbush.JPG)
3. 真ん中の穴からLANケーブルを通し、右側の穴まで通す。
![pipe and LAN cable](https://raw.githubusercontent.com/kfb01250/trapo/images/pipe-lancable.JPG)
4. 角パイプ半分より少し長めのところでLANケーブルの被覆を剥き、ケーブルに結び目を作る。オレンジ・白オレンジのケーブルは切断する。
![strip LAN cable](https://raw.githubusercontent.com/kfb01250/trapo/images/strip-cable.JPG)
![knot](https://raw.githubusercontent.com/kfb01250/trapo/images/knot.JPG)
5. 両端からケーブルを引き出す。
右側からは青・白青・白茶のケーブルを引き出す。
![right side](https://raw.githubusercontent.com/kfb01250/trapo/images/rightside.JPG)
左側からは緑・白緑・茶のケーブルを引き出す。
![left side](https://raw.githubusercontent.com/kfb01250/trapo/images/leftside.JPG)
6. センサーとケースを取り付ける。
![right sensor and case](https://raw.githubusercontent.com/kfb01250/trapo/images/rightsensor-case.JPG)
![left sensor and case](https://raw.githubusercontent.com/kfb01250/trapo/images/leftsensor-case.JPG)
7. 側面の穴からケーブルを引き出し、センサーをケースに押し込む。
8. 側面の穴から引き出したケーブルを、穴に戻してキャップで蓋をする。 

## TRAPOロガー
![Logger Inside](https://raw.githubusercontent.com/kfb01250/trapo/images/logger-inside.JPG)
![Arduino and Shield](https://raw.githubusercontent.com/kfb01250/trapo/images/arduino-shield.JPG)
![TRAPO Logger](https://raw.githubusercontent.com/kfb01250/trapo/images/logger-lcd-button.JPG)

### 部品
- [Arduino Uno][7]
- [Adafruit Data Logging Shield][1]
- [LANコネクタDIP化基板][2]
- [LCDキャラクタディスプレイモジュール（16x2行バックライト無）][4]
- [可変抵抗][5]（LCDのコントラスト調整用）
- [タクトスイッチ][6](赤・白)
- ケース(3Dプリント)
- フタ(3Dプリント)
- ボタン(3Dプリント)(赤・黄)
- プリント基板(自作) 


### 配線
#### LANコネクタDIP化基板 = Data Logging Shield

- 1(白橙) = nc
- 2(橙)   = nc
- 3(白緑) = AnalogIn 1
- 4(青)   = GND
- 5(白青) = AnalogIn 0
- 6(緑)   = GND
- 7(白茶) = 5V
- 8(茶)   = 5V


#### LCDキャラクタディスプレイモジュール = Data Logging Shield
-  1 VDD = 5V
-  2 VSS = GND
-  3 VO  = 可変抵抗(2)
-  4 RS  = D7
-  5 R/W = GND
-  6 E   = D6
-  7 DB0 = nc
-  8 DB1 = nc
-  9 DB2 = nc
- 10 DB3 = nc
- 11 DB4 = D5
- 12 DB5 = D4
- 13 DB6 = D3
- 14 DB7 = D2


#### 可変抵抗
- 1 = GND
- 2 = LCD(3)
- 3 = 5V


#### タクトスイッチ = Data Logging Shield
決定ボタン(赤)

- T1-T2 = D8
- T3-T4 = GND

選択ボタン(赤以外)

- T1-T2 = D9
- T3-T4 = GND

#### Data Logging Shieldへの部品配置と配線

部品面
![Shield Top](https://raw.githubusercontent.com/kfb01250/trapo/images/shield-top.JPG)

半田面（Data Logging Shieldの「SCK」「MISO」「MOSI」3つのジャンパを
ハンダ付けしてショートしてください。）
![Shield Top](https://raw.githubusercontent.com/kfb01250/trapo/images/shield-bottom.JPG)


### プリント基板
![pcb](https://raw.githubusercontent.com/kfb01250/trapo/images/pcb.JPG)
![pcb and wiring](https://raw.githubusercontent.com/kfb01250/trapo/images/pcb-non-pcb.JPG)

制作時間を短縮するためにプリント基板を作りました。

![Logger PCB](https://raw.githubusercontent.com/kfb01250/trapo/images/logger-pcb.png)

PCBEで設計し[ユニクラフト](https://unicraft-jp.com)に発注しました。
logger.zipは発注時に送ったデータです。

※Data Logging Shieldの「SCK」「MISO」「MOSI」3つのジャンパを
ハンダ付けしてショートしてください。

参考にしたサイト：[PCBEによる基板設計の手引き][10]


### ファームウェア(Arduino)

ファームウェアにはRTCのライブラリが必要です。
「RTClib by Adafruit」のバージョン1.2.0をインストールしてください。

Arduino IDEの「スケッチ」「ライブラリを管理...」から検索してください。


[1]: https://www.adafruit.com/product/1141
[2]: http://akizukidenshi.com/catalog/g/gP-05409/
[3]: http://akizukidenshi.com/catalog/g/gI-03157/
[4]: http://akizukidenshi.com/catalog/g/gP-00040/
[5]: http://akizukidenshi.com/catalog/g/gP-06063/
[6]: http://akizukidenshi.com/catalog/g/gP-03646/
[7]: https://store.arduino.cc/usa/arduino-uno-rev3
[8]: https://www.marutsu.co.jp/pc/i/14644/
[10]: http://ifdl.jp/akita/plan/pcbeguide/
