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

	a_structPath = a.getstructPath()
	a_Matrix = a.getmatrix()
	a_Translate = a.gettranslate()
	a_Trcxy = a.gettrcxy()
	b_structPath = b.getstructPath()
	b_Matrix = b.getmatrix()
	b_Translate = b.gettranslate()
	b_Trcxy = b.gettrcxy()

	tmp =[]
	n = 30 # n of flames
	for i in range(n):
		c=pensvg.devidestructPath(pensvg.touitustructPath(a_structPath),pensvg.touitustructPath(b_structPath),1.0/(n-1) * i,a_Matrix,b_Matrix,a_Translate,b_Translate)
		d= pensvg.getpoint(c,20)
		tmp.append(d)
	tmp2 += tmp
print pickle.dumps(tmp2)
