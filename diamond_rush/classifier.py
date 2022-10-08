#!/usr/bin/env python3
import cv2
import numpy as np
import os, shutil

img_dir = './levels/'
imgs = [img_dir+str(x) for x in os.listdir(img_dir)]
idx = 0

def classifier(blks):
  duplicates = set() 
  groups = []
  g = []
  idx = 0
  gIdx = 0
  while idx < len(blks):
    if idx in duplicates:
      idx += 1
      continue
    img1 = cv2.imread(blks[idx], cv2.IMREAD_GRAYSCALE)
    for i in range(idx+1,len(blks)-1):
      if i in duplicates:
        continue
      img2 = cv2.imread(blks[i], cv2.IMREAD_GRAYSCALE)
      if img2.shape == (88,88) and img1.shape == (88,88):
        diff = cv2.absdiff(img1,img2)
        diffM = np.mean(diff)
        if diffM < 5:
          duplicates.add(i)
          g.append(i)
          continue
    groups.append(g)
    print('len of groups: ',len(groups[gIdx]))
    if len(groups[gIdx]) > 1:
      if not os.path.exists('./blocks/'+str(gIdx)):
        os.mkdir('./blocks/'+str(gIdx))
      for i in groups[gIdx]:
#        if os.path.exists(blks[i]):
        nP = './blocks/'+str(gIdx)+'/'+blks[i][10:]
        shutil.move(blks[i], nP)
    g = []
    gIdx += 1
    idx += 1
  print(len(duplicates))

def rmEmptyF(p):
  fs = [os.path.join(blk_dir,x) for x in os.listdir(p) if os.path.isdir(os.path.join(blk_dir,x))]
  for i in fs:
    if len(os.listdir(i)) == 0:
      print(i)
      shutil.rmtree(i)

def cleanData(p):
  searched = set()
  duplicates = set()
  i = 0
  a = -1 
  while i < len(p):
    if p[i] in duplicates:
      i += 1
      continue
    img1 = cv2.imread(p[i], cv2.IMREAD_GRAYSCALE)
##    print(i)
    for j in range(i+1,len(p)):
      if p[j] in duplicates:
        continue
      img2 = cv2.imread(p[j], cv2.IMREAD_GRAYSCALE)
      if img2.shape == (88,88) and img1.shape == (88,88):
        diff = cv2.absdiff(img1,img2)
        diffM = np.mean(diff)
        if diffM < 5:
          duplicates.add(p[j])
          continue
    searched.add(p[i])
    i += 1
  for d in duplicates:
    os.remove(d)
  print(p[0])
  print('searched: ',len(searched))
  print('duplicates: ',len(duplicates))

blk_dir = './blocks/'

#ds = [os.path.join(blk_dir,x) for x in os.listdir(blk_dir) if os.path.isdir(os.path.join(blk_dir,x))]
#for i in ds:
#  p = [os.path.join(i,str(x)) for x in os.listdir(i) if x[len(x)-3:] == 'png']
#  cleanData(p)

#classifier(blks)
#rmEmptyF(blk_dir)
