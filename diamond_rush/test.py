#!/usr/bin/env python3

import cv2 
import numpy as np
import os
from enviroment import levels
from enviroment import whichLevel
from enviroment import mL
from enviroment import capture

#fs = [os.path.join(blk_dir,x) for x in os.listdir(p) if os.path.isdir(os.path.join(blk_dir,x))]
ss_tests = './levels/ss_test/'

test = [os.path.join(ss_tests,x) for x in os.listdir(ss_tests) if os.path.isdir(os.path.join(ss_tests,x))]
test.sort()
#print(test)
t = []
for i in test:
  t.append([os.path.join(i,str(x)) for x in os.listdir(i) if x[len(x)-3:] == 'png'])

#for i in t[6]:
#  level = whichLevel(i)
#  print()
#  capture(levels[0],i)

#for i, j in enumerate(levels):
#  print(i, j)

#for i in t:
#  for j in i:
#    capture(j,levels)

#print(capture(t[8][0],levels))

#for i in t[1]:
#  capture(i,levels)
#state = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)
