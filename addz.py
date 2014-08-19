import numpy as np
import sys
import math
import re
import cPickle

fi = sys.stdin
frames = pickle.load(fi)

global HIGH
HIGH = 30000
global LOW
LOW = -30000

def hokan(ar1,ar2):
        ar = []
        x1 = int(ar1[-1][0]) # start point
        y1 = int(ar1[-1][1])
        x2 = int(ar2[1][0]) # end point
        y2 = int(ar2[1][1])
        d = math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
        if (d==0):
                return ar
        n = 1+int(d/100) # should be adjusted
        for i in range(n):
                ar.append([x1,y1,HIGH]) # enphasize start point
        for i in range(n):
                ar.append([x1,y1,LOW])
        for i in range(n-1):
                ar.append([x1+(x2-x1)*(i+1)/n,y1+(y2-y1)*(i+1)/n,LOW]) # hokan
        for i in range(n):
                ar.append([x2,y2,LOW])
        for i in range(n):
                ar.append([x2,y2,HIGH]) # enphasize start point
        return ar

tmp = []
tmp2 =[]
out = []
for paths in frames:
	tmp2 =[]
        n = len(paths)
        for i in range(n-1):
		tmp =[]
		if paths[i][0] == 'ff0000': # if it is red
			HIGH = -30000
		else:
			HIGH = 30000
                for x in paths[i]:
			tmp.append([x[0],x[1],HIGH])
                for x in hokan(paths[i],paths[i+1]): # do hokan the last path to the next path
                        tmp.append([x[0],x[1],x[2]])
		tmp2.append(tmp[1:])
	tmp =[]
        for x in (paths[-1]): # the last path
		if paths[-1][0] == 'ff0000':
			HIGH = -30000
		else:
			HIGH = 30000
                tmp.append([x[0],x[1],HIGH])
	tmp2.append(tmp[1:])
	tmp =[]
        for x in hokan(paths[-1],paths[0]): # do hokan the last path to the 1st path 
		if paths[-1][0] == 'ff0000':
			x[2] = -30000
                tmp.append([x[0],x[1],x[2]])
	tmp2.append(tmp[1:])
	out.append(tmp2)

#for x in out:
#	for xx in x:
#		for xxx in xx:
#			print xxx[0],",",xxx[1],",",xxx[2]
print pickle.dumps(out)
