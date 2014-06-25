import numpy as np
import cv2
import sys
import math
import re
import pickle

#argvs = sys.argv
#argc = len(argvs)

fi = sys.stdin
flames = pickle.load(fi)

global HIGH
HIGH = 30000
global LOW
LOW = -30000

def hokan(ar1,ar2):
        ar = []
        x1 = int(ar1[-1][0]) # start point
        y1 = int(ar1[-1][1])
        x2 = int(ar2[0][0]) # end point
        y2 = int(ar2[0][1])
        d = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
        if (d==0):
                return ar
        n = 1+int(d/40) # should be adjusted
        for i in range(n):
                ar.append([x1,y1,HIGH]) # enphasize start point
        for i in range(n):
                ar.append([x1,y1,LOW])
        for i in range(n-1):
                ar.append([x1+(x2-x1)*(i+1)/n,y1+(y2-y1)*(i+1)/n,LOW]) # hokan
        for i in range(n):
                ar.append([x2,y2,LOW])
        for i in range(n):
                ar.append([x2,y2,HIGH]) # enphasize end point
        return ar


tmp = []
tmp2 =[]
out = []
for paths in flames:
	tmp2 =[]
        n = len(paths)
        for i in range(n-1):
		tmp =[]
                for x in (paths[i]):
                        tmp.append([x[0],x[1],HIGH])
                for x in hokan(paths[i],paths[i+1]): # do hokan the last path to the next path
                        tmp.append([x[0],x[1],x[2]])
		tmp2.append(tmp)
	tmp =[]
        for x in (paths[-1]): # the last path
                tmp.append([x[0],x[1],HIGH])
        for x in hokan(paths[-1],paths[0]): # do hokan the last path to the 1st path 
                tmp.append([x[0],x[1],x[2]])
	tmp2.append(tmp)
	out.append(tmp2)
#print len(out),len(out[0]),len(out[0][0])
#print out[0][0]
print pickle.dumps(out)
