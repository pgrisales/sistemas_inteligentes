#!/usr/bin/env python3

import cv2 
import numpy as np
import os
from capture import levels
from capture import matchLevel 
from capture import matchLevel2 
from capture import agentPos

#fs = [os.path.join(blk_dir,x) for x in os.listdir(p) if os.path.isdir(os.path.join(blk_dir,x))]
ss_tests = './levels/ss_test/'

test = [os.path.join(ss_tests,x) for x in os.listdir(ss_tests) if os.path.isdir(os.path.join(ss_tests,x))]
test.sort()
#print(test)
t = []
for i in test:
  t.append([os.path.join(i,str(x)) for x in os.listdir(i) if x[len(x)-3:] == 'png'])

#print(agentPos(agent_dir, t[1][0]))
#for i in t:
#  for j in i:
#    print(j)
#    print(matchLevel2(levels,j))
#    print()

#for i in t[6]:
#  level = whichLevel(i)
#  print()

#for i, j in enumerate(levels):
#  print(i, j)

#for i in t:
#  for j in i:


#for i in t[1]:
#state = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)

### test of main file
#test_img = './test_img.png'
#ts = t[5][0]
#print(ts)
#print(matchI(ts,levels))

###
### test 2 main
#print(matchLevel(levels,t[3][2]))
#for i in t:
#  for j in range(1):
#    print(i[j])
#    print(matchLevel(levels,i[j]))
#    print()
#
##    print(j)
##    print(matchLevel(levels,j))
##    print()
