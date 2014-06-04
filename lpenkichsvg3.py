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
                                tt = int((t * distance)//200)
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
                        tt = int((t * distance)//200)
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
        tt = int(t * distance /200)
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

def a_origin(x0,y0,a,b,x1,y1):
	P = (x0+x1)/2.0 + a*a*(y0+y1)*(y0-y1)/(2.0*b*b*(x0-x1))
	Q = -a*a*(y0-y1)/(b*b*(x0-x1))
	A = a*a +b*b*Q*Q
	B = 2.0*b*b*P*Q -2.0*b*b*Q*x0 -2.0*a*a*y0
	C = b*b*x0*x0 -2.0*b*b*P*x0 +b*b*P*P +a*a*y0*y0 -a*a*b*b
	dy = (-B +math.sqrt(B*B -4.0*A*C))/(2.0*A)
	dx = P + Q*dy
	return dx,dy


def rotate(x,y,angle):
	angle = angle * math.pi/180.0
	x1 = x*math.cos(angle) - y*math.sin(angle)
	y1 = x*math.sin(angle) + y*math.cos(angle)
	return x1,y1

def exec_matrix(data,a,b,c,d,e,f,trcx,trcy):
	ar = []
	for x in data:
		ar.append([a * (x[0] -trcx) +c * (x[1] -trcy) +e +trcx,
                           b * (x[0] -trcx) +d * (x[1] -trcy) +f +trcy])
	return ar

def exec_translate(data,tx,ty,trcx,trcy):
        ar = []
        for x in data:
                ar.append([x[0]-trcx + tx,
                           x[1]-trcy + ty])
        return ar

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
			       if s3 == 'a':
				       m = a2point(t,x0,y0,path[i+1])
                                       x0,y0 = m[-1][0],m[-1][1]
                                       if i ==0: xs,ys = m[0][0],m[0][1]
                                       tmp += m
			       if s3 == 'A':
				       m = A2point(t,x0,y0,path[i+1])
                                       x0,y0 = m[-1][0],m[-1][1]
                                       if i ==0: xs,ys = m[0][0],m[0][1]
                                       tmp += m
			       if s3 == 'z':
				       m = z2point(t,x0,y0,xs,ys)
                                       tmp += m
                       if Matrix[j]:
                               [a,b,c,d,e,f] = Matrix[j]
                               [trcx,trcy] = Trcxy[j]
                               tmp = exec_matrix(tmp,a,b,c,d,e,f,trcx,trcy)
                       if Translate[j]:
                               a=1
                       j+=1
                       ar.append(tmp)
               return ar

def touitu_d(x0,y0,d1):
        tmp =[]
        tmp2 =[]
        for i,s3 in enumerate(d1):
                if s3 == 'm':
                        tmp.append('M')
                        tmp2 = rel2abs(x0,y0,d1[i+1])
                        tmp.append(tmp2)
                        x0,y0 = tmp2[-1]
                if s3 == 'l':
                        tmp.append('L')
                        tmp2 = rel2abs(x0,y0,d1[i+1])
                        tmp.append(tmp2)
                        x0,y0 = tmp2[-1]
                if s3 == 'c':
                        tmp.append('C')
                        tmp2 = rel2abs4c(x0,y0,d1[i+1])
                        tmp.append(tmp2)
                        x0,y0 = tmp2[-1]
                elif s3 == 'z':
                        tmp.append(d1[i])
                        break
        return tmp


def devided(d1,d2,n):
        tmp =[]
        for i,s3 in enumerate(d1):
                if re.match('[mMcClLaA]',str(s3)):
                        tmp.append(d1[i])
                        npd1 = np.array(d1[i+1])
                        npd2 = np.array(d2[i+1])
                        tmp.append((npd1*(1-n) +npd2*(n)).tolist())
                elif s3 == 'z':
                        tmp.append(d1[i])
                        break
        return tmp

a=inksvg2("Fo2.svg")
structPath = a.getstructPath()
Matrix = a.getmatrix()
Translate = a.gettranslate()
Trcxy = a.gettrcxy()
b= getpoint(structPath,Matrix,Trcxy,Translate,12)

#print a.structPath
print b

for x in(b):
        for y in x:
                print y[0], ",", y[1]
