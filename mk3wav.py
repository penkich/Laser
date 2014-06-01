# -*- coding:utf8 -*-
################################
# mk3wav.py
# wavファイルを生成させる(6ch)
# by penkich
# for fablab kitakagaya 2014-04-02
# 6ch 2014-04-25
################################
import sys
import struct
import string
import math

argvs = sys.argv
argc = len(argvs)

fi = open(argvs[1],"r") # 第１引数で、入力ファイル(x,y座標,z）を指定
fo = open(argvs[2],"wb") # 第２引数で、出力ファイル（wavファイル）を指定
t = int(argvs[3]) # 第３引数で、再生時間を指定 2000で約5s
repeat = int(argvs[4]) # 第４引数で、繰返回数を指定

#################################
# to make wav header (Extensible Format)
#################################
dsize = 2399324-44 #データサイズ(手抜いて計算せず十分な値に設定）
fsize = dsize + 44 #ファイルサイズ
cksize = 40 # Chunk size: 40=fix
fbit = 16 # 量子化ビット数(固定)
ch = 6 #チャンネル数
sb = 48000 #サンプリング周波数 must be 48000=fix 
sp = sb * ch * fbit / 8
bz = fbit / 8 * ch

fo.write('RIFF') # Chunk ID: "RIFF"
fo.write(struct.pack("i",fsize-8))
fo.write('WAVE')
fo.write('fmt ')
fo.write(struct.pack("i",cksize))
fo.write(struct.pack("H",0xFFFE))
fo.write(struct.pack("h",ch))
fo.write(struct.pack("i",sb))
fo.write(struct.pack("i",sp))
fo.write(struct.pack("H",bz))
fo.write(struct.pack("H",16))
fo.write(struct.pack("H",0x0016)) # 22=fix
fo.write(struct.pack("H",0x0000))
fo.write(struct.pack("H",0x003F)) # Speaker position mask
fo.write(struct.pack("H",0x0000)) # 
fo.write(struct.pack("H",0x0001)) # GUID (first two bytes are the data format code)
fo.write(struct.pack("H",0x0000)) #
fo.write(struct.pack("H",0x0000)) #
fo.write(struct.pack("H",0x0010)) #
fo.write(struct.pack("H",0x0080)) #
fo.write(struct.pack("H",0xAA00)) #
fo.write(struct.pack("H",0x3800)) #
fo.write(struct.pack("H",0x719B)) #
fo.write('data')
fo.write(struct.pack("i",dsize))
#################################
# ヘッダーの次にデータ(xy座標値,z)がつづく
#################################

x=[]
y=[]
z=[] ## on/off data
buf = fi.readline().strip().split(',')
i = 0
while buf[0]:
	x.append(int(buf[0]))
	y.append(int(buf[1]))
	z.append(int(buf[2]))
	buf = fi.readline().strip().split(',')
	i = i+1
### 丁度真ん中に適当な大きさで表示するように調整（なくてもいいけど）
xorigin = int((max(x) + min(x)) /2)
yorigin = int((max(y) + min(y)) /2)
max = max(max(x),max(y))
scale = int(32000 / max) ### 32000=16bit の（約）最大値
for j in range(int(t*100/i/repeat)): ### 100は適当な値。データ量に応じて繰り返しを調整する。
	for k in range(i):
		for n in range(repeat):
			fo.write(struct.pack("h",(x[k]-xorigin)*scale))
			fo.write(struct.pack("h",(y[k]-yorigin)*scale))
			fo.write(struct.pack("h",z[k]))
			fo.write(struct.pack("h",0))
			fo.write(struct.pack("h",0))
			fo.write(struct.pack("h",0))
fi.close()
fo.close()
