import numpy as np
import pickle
import sys
import re
import math
import lpenkichsvg3 as pensvg

argvs = sys.argv
argc = len(argvs)
tmp2 =[]

for i in range(argc-2):
	a=pensvg.inksvg(argvs[i+1])
	b=pensvg.inksvg(argvs[i+2])

#	print a.getd()

	a_structPath = a.getstructPath()

	a_gMatrix = a.getgmatrix()
	a_Matrix = a.getmatrix()
	a_Translate = a.gettranslate()
#	a_Trcxy = a.gettrcxy()
	a_Trcxy = ""



	b_structPath = b.getstructPath()
	b_gMatrix = b.getgmatrix()
	b_Matrix = b.getmatrix()
	b_Translate = b.gettranslate()
#	b_Trcxy = b.gettrcxy()
	b_Trcxy = ""

#	print a_structPath


	if len(a_gMatrix) >1:
		if a_gMatrix[1]:
			for i in range(len(a_Matrix)):
				a_Matrix[i] = a_gMatrix[1]
	if len(b_gMatrix) >1:
		if b_gMatrix[1]:
			for i in range(len(b_Matrix)):
				b_Matrix[i] = b_gMatrix[1]
#	print "a",a_gMatrix
#	print "b",b_gMatrix
#	print "a",a_Matrix
#	print "b",b_Matrix

#	print "GTransform",a.getGTransform()
#	exit()



#	print "0",a.getg()[0]
#	print "1",a.getg()[1]
#	print a_structPath
#	print argvs[i+1]
#	print a_Matrix
#	print a_Translate
#	print a_Trcxy

#	print argvs[i+2]
#	print b_Matrix
#	print b_Translate
#	print b_Trcxy

	tmp =[]
	n = 30 # n of flames
	for i in range(n):
		c= pensvg.devidestructPath(pensvg.touitustructPath(a_structPath),pensvg.touitustructPath(b_structPath),1.0/(n-1) * i,a_Matrix,b_Matrix,a_Translate,b_Translate)
		d= pensvg.getpoint(c,a_Matrix,a_Trcxy,a_Translate,20)
		tmp.append(d)
	tmp2 += tmp
print tmp2
#print pickle.dumps(tmp2)
