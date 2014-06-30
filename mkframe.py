import numpy as np
import pickle
import sys
import re
import math
import lpenkichsvg3 as pensvg

argvs = sys.argv
argc = len(argvs)
tmp2 =[]

argvs = argvs[1:]
argc = len(argvs)
files = []
i = 0
while i < argc-1:
	if argvs[i+1][-3:] != "svg":
		i = i+1
	else:
		files.append([argvs[i],argvs[i+1]])
	i = i+1

for x in files:
	a=pensvg.inksvg(x[0])
	b=pensvg.inksvg(x[1])

	a_structPath = a.getstructPath()

	a_gMatrix = a.getgmatrix()
	a_Matrix = a.getmatrix()
	a_Translate = a.gettranslate()

	b_structPath = b.getstructPath()
	b_gMatrix = b.getgmatrix()
	b_Matrix = b.getmatrix()
	b_Translate = b.gettranslate()


#	GTrans = a.getGTransform()[0]
#	if GTrans[0:9] == 'translate':
#		tmp = GTrans[10:-1]
#		print "translate",GTrans,tmp
#	if GTrans[0:6] == 'matrix':
#		print "matrix",GTrans
#	if GTrans[0:5] == 'scale':
#		tmp = GTrans[6:-1]
#		print "scale",GTrans,tmp

	a_color = a.getcolor()

	if len(a_gMatrix) >1:
		if a_gMatrix[1]:
			for i in range(len(a_Matrix)):
				a_Matrix[i] = a_gMatrix[1]
	if len(b_gMatrix) >1:
		if b_gMatrix[1]:
			for i in range(len(b_Matrix)):
				b_Matrix[i] = b_gMatrix[1]
	
	tmp =[]
	n = 30 # n of frames
	for i in range(n):
		c= pensvg.devidestructPath(pensvg.touitustructPath(a_structPath),pensvg.touitustructPath(b_structPath),1.0/(n-1) * i,a_Matrix,b_Matrix,a_Translate,b_Translate)
		d= pensvg.getpoint(c,a_Matrix,a_Translate,a_color,20)
		tmp.append(d)
	tmp2 += tmp
#print tmp2
print pickle.dumps(tmp2)
