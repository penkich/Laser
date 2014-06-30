################################
# mk6wav.py
# to make wavfile
# by penkich
# for fablab kitakagaya 2014-04-02
# 6ch 2014-04-25
################################
import sys
import struct
import string
import math
import numpy as np
import pickle

argvs = sys.argv
argc = len(argvs)

fi = sys.stdin
flames = np.array(pickle.load(fi))

#fi = open(argvs[1],"r") # input file of x,y
fo = open(argvs[1],"wb") # output file of wav
repeat = int(argvs[2]) # redundancy

#################################
# to make wav header (Extensible Format)
#################################
dsize = 20000000 # data size (set enough size for easy)
fsize = dsize + 44 # wav file size
cksize = 40 # Chunk size: 40=fix
fbit = 16 # bits 
ch = 6 # n of channel
sb = 48000 # sampling frequency must be 48000 
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
fo.write(struct.pack("H",0x003F)) # Speaker position mask (111111b = 3F)
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
# x,y,z data followed by the above headder
#################################

xsize = 750.0
ysize = 750.0

for flame in flames:
        for path in flame:
		for x in path:
			for i in range(repeat):
				fo.write(struct.pack("h",(x[0]-xsize/2.0)/xsize * 32000)) # ch1 (x)
				fo.write(struct.pack("h",(x[1]-ysize/2.0)/ysize * 32000)) # ch2 (y)
				fo.write(struct.pack("h",x[2])) # ch3 (z ... on/off)
				fo.write(struct.pack("h",0)) # ch4 not use
				fo.write(struct.pack("h",0)) # ch5 not use
				fo.write(struct.pack("h",0)) # ch6 not use

fi.close()
fo.close()
