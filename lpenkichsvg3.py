################################################
# lpenkichsvg3.py by penkich
# for fablab kitakagaya rev 2014-04-02
# 2014-05-06
# class 2014-05-10
#################################################
import libxml2,math,re
import numpy as np

def getPointC(t,ar1,ar2,ar3,ar4):
        tp = 1.0 - t
        return  (t * t * t * np.array(ar4)
                 + 3.0 * t * t * tp * np.array(ar3)
                 + 3.0 * t * tp * tp * np.array(ar2)
                 + tp * tp * tp * np.array(ar1))

def rel2abs(x0,y0,data):
        npar = np.array([[x0,y0]] + data)
        for i, m in enumerate(npar):
                if i > 0:
                        npar[i] += npar[i-1]
        return npar.tolist()

def rel2abs4c(x0,y0,data):
        npar = np.array([[x0,y0]] + data)
	for i,m in enumerate(npar):
		if i ==0:
			npar[1] += npar[0]
			npar[2] += npar[0]
		if i >= 3:
			if i % 3 ==0:
				npar[i] += npar[i-3]
		       	if i % 3 ==1:	
				npar[i] += npar[i-1]
			if i % 3 ==2:
				npar[i] += npar[i-2]
        return npar[1:].tolist()


def m2point(t,x0,y0,data):
        ar = rel2abs(x0,y0,data)
        return M2point(t,x0,y0,ar[1:])

def M2point(t,x0,y0,data):
	ar2 = []
        ar = np.array(data)
        if len(ar) > 1:
                for i, m in enumerate(ar):
                        if i >0:
                                distance = np.linalg.norm(ar[i]-ar[i-1])
                                tt = int((t * distance)//300)
                                if tt < 2:
                                        tt = 2
                                for k in range(tt+1):
                                        ar2.append((ar[i-1]+((ar[i]-ar[i-1])/tt)*k).tolist())
        else:
                return ar.tolist()
        return ar2

def L2point(t,x0,y0,data):
	ar2 = []
        ar = np.array([[x0,y0]]+data)
        for i, m in enumerate(ar):
                if i >0:
                        distance = np.linalg.norm(ar[i]-ar[i-1])
                        tt = int((t * distance)//300)
                        if tt < 2:
                                tt = 2
                        for k in range(tt+1):
                                ar2.append((ar[i-1]+((ar[i]-ar[i-1])/tt)*k).tolist())
        return ar2

def l2point(t,x0,y0,data):
        ar = rel2abs(x0,y0,data)
        return L2point(t,x0,y0,ar)        

def z2point(t,x0,y0,xs,ys):
	ar2 = []
	ar0 = np.array([x0,y0])
        ars = np.array([xs,ys])
        distance = np.linalg.norm(ars-ar0)
        if distance ==0:
                return [ar0.tolist()]
        tt = int(t * distance /300)
        if tt < 2:
                tt = 2
	for k in range(tt+1):
		ar2.append((ar0+(ars-ar0)/tt *k).tolist())
        return ar2

def c2point(t,x0,y0,data):
        ar = rel2abs4c(x0,y0,data)
        return C2point(t,x0,y0,ar)

def C2point(t,x0,y0,data):
	ar2 = []
        ar = np.array([[x0,y0]] + data)
	j = 0
	for x in range(len(ar)//3):
		dist = np.linalg.norm(ar[j+3]-ar[j])
		tt = int((t * dist)//200)
		if tt < 2:
			tt = 2
		for d in range(tt+1):
			dif = 1.0/tt *d
                        ar2.append(getPointC(dif,ar[j],ar[j+1],ar[j+2],ar[j+3]))
                j +=3
	return ar2

def rotate(x,y,angle):
	angle = angle * math.pi/180.0
	x1 = x*math.cos(angle) - y*math.sin(angle)
	y1 = x*math.sin(angle) + y*math.cos(angle)
	return x1,y1

def exec_matrix(data,Matrix):
	ar = []
        if Matrix:
                a,b,c,d,e,f = Matrix
#                trcx,trcy = Trcxy
                trcx,trcy = 0,0
                for x in data:
                        ar.append([a * (x[0] -trcx) +c * (x[1] -trcy) +e +trcx,
                                   b * (x[0] -trcx) +d * (x[1] -trcy) +f +trcy])
                return ar
        else:
                return data

def exec_translate(data,translate):
        ar = []
        if translate:
                tx,ty = translate
                trcx=0
                trcy=0
                for x in data:
                        ar.append([x[0]-trcx + tx,
                                   x[1]-trcy + ty])
                return ar
        else:
                return data

class inksvg:
        def __init__(self,fname):
		self.fname = fname
        def getPath(self):
                tmp =[]
                doc = libxml2.parseFile(self.fname)
                for node in doc:
                        if node.name == "path":
                                tmp.append(str(node))
                doc.freeDoc()
                return tmp
        def getd(self):
                tmp =[]
		for s in self.getPath():
	       	        m = re.match('.*d\=\"([mMcClLaA].*?)\"',s)
                        tmp.append(m.group(1))
                return tmp
        def getstructPath(self):
                tmp2 =[]
		for s in self.getd():
                        tmp =[]
      			while True:
                                tmp3=[]
				m = re.match('([mMcClLaA]) ([\d\,\.\- e]*)',s)
				if m:
                                        tmp.append(m.group(1))
                                        if m.group(1) != 'a' and m.group(1) != 'A':
                                                for x in m.group(2).split(' '):
                                                        if x:
                                                                tmp3.append([float(x.split(',')[0]),float(x.split(',')[1])])
                                                tmp.append(tmp3)
                                                s = s[m.end(2):]
                                        if m.group(1) == 'a' or m.group(1) == 'A':
                                                for x in m.group(2).split(' '):
                                                        if x:
                                                                if ',' in x:
                                                                        tmp3.append([float(x.split(',')[0]),float(x.split(',')[1])])
                                                                else:
                                                                        tmp3.append([int(x)])
                                                tmp.append(tmp3)
                                                s = s[m.end(2):]
				else:
                                        if s:
                                                tmp.append(s)
					break
                        tmp2.append(tmp)
		return tmp2
        def gettrcxy(self):
                tmp =[]
		for s in self.getPath():
        		mx = re.match('.*inkscape\:transform\-center\-x=\"([\-\.\d]*).*\"',s)
        		my = re.match('.*inkscape\:transform\-center\-y=\"([\-\.\d]*).*\"',s)
			if mx:
				tmp.append([float(mx.group(1)),float(my.group(1))])
                        else:
                                tmp.append([0,0])
                return tmp
        def getmatrix(self):
                tmp2 =[]
		for s in self.getPath():
                        tmp =[]
        		m = re.match('.*transform\=\"matrix\(([\-\.\d\,]*)\).*\"',s)
        		if m:
        			for v in m.group(1).split(','):
                			tmp.append(float(v))
                                tmp2.append(tmp)
			else:
				tmp2.append("")
		return tmp2
        def gettranslate(self):
		tmp2 =[]
		for s in self.getPath():
                        tmp =[]
		        m = re.match('.*transform\=\"translate\(([\-\.\d\,]*)\).*\"',s)
			if m:
        			for v in m.group(1).split(','):
                			tmp.append(float(v))
                                tmp2.append(tmp)
			else:
				tmp2.append("")
		return tmp2

class inksvg2(inksvg):
        def convC2c(self):
                print getPath(self)




def getpoint(structPath,Matrix,Trcxy,Translate,t):
               ar =[]
               m =[]
               j =0
               for path in structPath:
                       x0,y0 =0,0
                       tmp =[]
                       for i,s3 in enumerate(path):
			       if s3 == 'm':
                     		       m = m2point(t,x0,y0,path[i+1])
                                       x0,y0 = m[-1][0],m[-1][1]
                                       if i ==0: xs,ys = m[0][0],m[0][1]
                                       tmp += m
			       if s3 == 'M':
				       m = M2point(t,x0,y0,path[i+1])
                                       x0,y0 = m[-1][0],m[-1][1]
                                       if i ==0: xs,ys = m[0][0],m[0][1]
                                       tmp += m
			       if s3 == 'l':
				       m = l2point(t,x0,y0,path[i+1])
                                       x0,y0 = m[-1][0],m[-1][1]
                                       if i ==0: xs,ys = m[0][0],m[0][1]
                                       tmp += m
			       if s3 == 'L':
				       m = L2point(t,x0,y0,path[i+1])
                                       x0,y0 = m[-1][0],m[-1][1]
                                       if i ==0: xs,ys = m[0][0],m[0][1]
                                       tmp += m
			       if s3 == 'c':
				       m = c2point(t,x0,y0,path[i+1])
                                       x0,y0 = m[-1][0],m[-1][1]
                                       if i ==0: xs,ys = m[0][0],m[0][1]
                                       tmp += m
			       if s3 == 'C':
				       m = C2point(t,x0,y0,path[i+1])
                                       x0,y0 = m[-1][0],m[-1][1]
                                       if i ==0: xs,ys = m[0][0],m[0][1]
                                       tmp += m
			       if s3 == 'z':
				       m = z2point(t,x0,y0,xs,ys)
                                       tmp += m
                       #if Matrix[j]:
                               #[a,b,c,d,e,f] = Matrix[j]
                               #[trcx,trcy] = Trcxy[j]
                       #        tmp = exec_matrix(tmp,Matrix[j],Trcxy[j])
                       #if Translate[j]:
                       #        a=1
                       j+=1
                       ar.append(tmp)
               return ar

def touitu_d(x0,y0,d1):
        tmp =[]
        for i,x in enumerate(d1):
                if x == 'm':
                        tmp.append('M')
                        tmp2 = rel2abs(x0,y0,d1[i+1])
                        tmp.append(tmp2[1:])
                        x0,y0 = tmp2[-1]
                if x == 'l':
                        tmp.append('L')
                        tmp2 = rel2abs(x0,y0,d1[i+1])
                        tmp.append(tmp2[1:])
                        x0,y0 = tmp2[-1]
                if x == 'c':
                        tmp.append('C')
                        tmp2 = rel2abs4c(x0,y0,d1[i+1])
                        tmp.append(tmp2)
                        x0,y0 = tmp2[-1]
                if x == 'M':
                        tmp.append('M')
                        tmp2 = d1[i+1]
                        tmp.append(tmp2)
                        x0,y0 = tmp2[-1]
                if x == 'L':
                        tmp.append('L')
                        tmp2 = d1[i+1]
                        tmp.append(tmp2)
                        x0,y0 = tmp2[-1]
                if x == 'z':
                        tmp.append(d1[i])
                        break
        return tmp


def devided(d1,d2,n,matrix1,matrix2,translate1,translate2):
        tmp =[]
        for i,s3 in enumerate(d1):
                if re.match('[mMcClLaA]',str(s3)):
                        tmp.append(d1[i])
                        npd1 = np.array(exec_translate(exec_matrix(d1[i+1],matrix1),translate1))
                        npd2 = np.array(exec_translate(exec_matrix(d2[i+1],matrix2),translate2))
                        tmp.append((npd1*(1-n) +npd2*(n)).tolist())
                elif s3 == 'z':
                        tmp.append(d1[i])
                        break
        return tmp

def devidestructPath(structPath1,structPath2,n,Matrix1,Matrix2,Translate1,Translate2):
        tmp = []
        for i,m in enumerate(structPath1):
                tmp.append(devided(structPath1[i],structPath2[i],n,Matrix1[i],Matrix2[i],Translate1[i],Translate2[i]))
        return tmp

def touitustructPath(structPath):
        tmp = []
        for m in structPath:
                tmp.append(touitu_d(0,0,m))
        return tmp

a=inksvg2("hosi1.svg")
b=inksvg2("hosi2.svg")
a_structPath = a.getstructPath()
a_Matrix = a.getmatrix()
a_Translate = a.gettranslate()
a_Trcxy = a.gettrcxy()
b_structPath = b.getstructPath()
b_Matrix = b.getmatrix()
b_Translate = b.gettranslate()
b_Trcxy = b.gettrcxy()

#print a_Translate
#print b_Translate


#print a_Matrix
#print a_Trcxy
#print b_Matrix
#print b_Trcxy
#print touitustructPath(a_structPath)
#print b_structPath
#print touitustructPath(b_structPath)


n = 20
for i in range(n):
        c=devidestructPath(touitustructPath(a_structPath),touitustructPath(b_structPath),1.0/(n-1) * i,a_Matrix,b_Matrix,a_Translate,b_Translate)
        d= getpoint(c,a_Matrix,a_Trcxy,a_Translate,12)
        print d
#        for x in(d):
#                for y in x:
#                        tmp1.append(y[0])
#                        tmp2.append(y[1])
#print "x=",tmp1
#print "y=",tmp2
