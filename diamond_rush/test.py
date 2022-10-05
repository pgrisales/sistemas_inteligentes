#!/usr/bin/env python3

import cv2 
import numpy as np
import os
from enviroment import levels
from enviroment import whichLevel

#fs = [os.path.join(blk_dir,x) for x in os.listdir(p) if os.path.isdir(os.path.join(blk_dir,x))]
ss_tests = './levels/ss_test/'

test = [os.path.join(ss_tests,x) for x in os.listdir(ss_tests) if os.path.isdir(os.path.join(ss_tests,x))]
test.sort()
#print(test)
t = []
for i in test:
  t.append([os.path.join(i,str(x)) for x in os.listdir(i) if x[len(x)-3:] == 'png'])

for i in t[0]:
  level = whichLevel(i)
  print()
#state = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)

