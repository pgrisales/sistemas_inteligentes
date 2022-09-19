#!/usr/bin/env python3
import cv2
import numpy as np
import os

# (1313, 882, 4)
# cx = 88; cy = 87
cx = 882//10
# best value for cy => 1321
cy = 1321//15

img_dir = './levels/'
imgs = [img_dir+str(x) for x in os.listdir(img_dir)]
#print(imgs)
#print(len(imgs))
idx = 0

def blockify(img_p):
  img = cv2.imread(img_p, cv2.IMREAD_UNCHANGED)
  global idx
  for i in range(15):
    for j in range(10):
      bx = cx*(j+1)
      by = cy*(i+1)
#      if by > 1313: by = 1313
#      b = cv2.rectangle(img, (cx*j,cy*i), (cx*(j+1),cy*(i+1)), (0,255,0), thickness=2)
      img_b = img[cy*i:by, cx*j:bx]
      b_name = './blocks/b_' + str(idx) + '.png'
      idx += 1
      print(idx)
      cv2.imwrite(b_name, img_b)


#for i in imgs:
#  blockify(i)

