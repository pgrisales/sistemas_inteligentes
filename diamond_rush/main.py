#!/usr/bin/env python3
import cv2 
import numpy as np
from enviroment import capture
from enviroment import mL
from enviroment import levels
from enviroment import mSift 

test_img = './test_img.png'

for i in levels:
  mSift(i,test_img)
#mSift(levels[1],test_img)
#mSift(test_img,levels[1])
#mSift(levels[0],levels[1])
#print(capture(test_img,levels))
#print(mL(test_img,levels[1]))
