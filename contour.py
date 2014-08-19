import numpy as np
import cv2
import cPickle
 
im = cv2.imread('4.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(imgray,(5,5),0)
ret,thresh = cv2.threshold(blur,128,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
start = 0  
max = 0
n= len(contours)

for i in range(n):
    if (max < np.max(contours[i])):
        max = np.max(contours[i])
if len(contours[0] ==4 & (np.max(contours[0]) ==max)):
    start = 1
tmp =[]
for i in range(start,n):
    tmp2 =[]
    for x in contours[i]:
        tmp2.append([x[0][0],x[0][1]])
    tmp.append(tmp2)
#print tmp
print pickle.dumps([tmp])
