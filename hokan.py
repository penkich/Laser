# -*- coding:utf8 -*-
import numpy as np
import cv2
import sys
import math

argvs = sys.argv
argc = len(argvs)

fi = open(argvs[1],"r") # 第１引数で、入力ファイル(x,y座標）を指定
global HIGH
HIGH = 30000
global LOW
LOW = -30000

def hokan(ar1,ar2):
	ar = []
	x1 = int(ar1[-1][0])
	y1 = int(ar1[-1][1])
	x2 = int(ar2[0][0])
	y2 = int(ar2[0][1])
	d = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
	if (d==0):
		return ar
	n = 1+int(d/10)
	for i in range(n):
		ar.append([x1,y1,HIGH])
	for i in range(n):
                ar.append([x1,y1,LOW])
	for i in range(n-1):
		ar.append([x1+(x2-x1)*(i+1)/n,y1+(y2-y1)*(i+1)/n,LOW])
	for i in range(n):
		ar.append([x2,y2,LOW])
	for i in range(n):
                ar.append([x2,y2,HIGH])
	return ar

ar =[]
tp =[]
buf = fi.readline()
while buf:
	if(len(buf.strip()) !=0):
		tp.append([int(buf.strip().split(',')[0]),int(buf.strip().split(',')[1])])
	buf = fi.readline()
	if(len(buf.strip()) ==0):
		ar.append(tp)
		tp=[]
n = len(ar)
for i in range(n-1):
	for x in (ar[i]):
		print x[0],",",x[1],",",HIGH
        for x in hokan(ar[i],ar[i+1]):
		print x[0],",",x[1],",",x[2]
for x in (ar[n-1]):
	print x[0],",",x[1],",",HIGH

for x in hokan(ar[n-1],ar[0]):
	print x[0],",",x[1],",",x[2]

