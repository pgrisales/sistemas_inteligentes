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
idx = 0

def blockify(img_p):
#  img = cv2.imread(img_p, cv2.IMREAD_UNCHANGED)
  img = cv2.imread(img_p, cv2.IMREAD_GRAYSCALE)
  global idx
  for i in range(15):
    for j in range(10):
      bx = cx*(j+1)
      by = cy*(i+1)
#      if by > 1313: by = 1313
#      b = cv2.rectangle(img, (cx*j,cy*i), (cx*(j+1),cy*(i+1)), (0,255,0), thickness=2)
      img_b = img[cy*i:by, cx*j:bx]
#      b_name = './blocks/b_' + str(idx) + '.png'
      b_name = './gBlocks/gB_' + str(idx) + '.png'
      idx += 1
      print(idx)
      cv2.imwrite(b_name, img_b)

blk_dir = './blocks/'
gBlk_dir = './gBlocks/'
gBlks = [gBlk_dir+str(x) for x in os.listdir(gBlk_dir)]
blks = [blk_dir+str(x) for x in os.listdir(blk_dir)]

def classifier(blks):
  img1 = cv2.imread(blks[74], cv2.IMREAD_UNCHANGED)
#  img22 = cv2.imread(blks[35], cv2.IMREAD_UNCHANGED)
#  print(blks[35])
#  a = cv2.subtract(img1,img22)
  for idx,i in enumerate(blks):
    img2 = cv2.imread(i, cv2.IMREAD_UNCHANGED)
    print(img2.shape)
    if img2.shape == (88,88):
      a = cv2.absdiff(img1,img2)
#    print(np.mean(img1))
#    print(np.mean(img2))
      am = np.mean(a)
      print(str(idx)+' Mean of '+blks[1]+', '+i+': ',am)
      if am < 6:
        cv2.imshow(i,img2)
        cv2.imshow(blks[1],img1)
#      cv2.imshow('a',a)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

#  for idxi,i in enumerate(blks):
#    for idxj,j in enumerate(blks):
#      img1 = cv2.imread(blks[idxi], cv2.IMREAD_UNCHANGED)
#      img2 = cv2.imread(blks[idxj], cv2.IMREAD_UNCHANGED)
#      print(type(img1))
#      res = cv2.matchTemplate(img1, img2, cv2.TM_SQDIFF_NORMED)
#      min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#      print(max_val)
#      if max_val > 0.7: os.remove(blks[idxj])

#print(len(blks))
#classifier(blks)
classifier(gBlks)
#blockify(imgs[0])
#for i in imgs:
#  blockify(i)

