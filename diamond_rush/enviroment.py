#!/usr/bin/env python3
import cv2 
import numpy as np
import os

levels_dir = './levels/'
levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if x[len(x)-3:] == 'png']

def whichLevel(img1_p,img2_p):
  from matplotlib import pyplot as plt
  img1 = cv2.imread(img1_p, cv2.IMREAD_GRAYSCALE)
  img2 = cv2.imread(img2_p, cv2.IMREAD_GRAYSCALE)
#  img1 = cv2.imread(img1_p, cv2.IMREAD_UNCHANGED)
#  img2 = cv2.imread(img2_p, cv2.IMREAD_UNCHANGED)
# Initiate ORB detector
  orb = cv2.ORB_create()
  kp1, des1 = orb.detectAndCompute(img1,None)
  kp2, des2 = orb.detectAndCompute(img2,None)
  
  bf = cv2.BFMatcher.create()
### KNNMATCH VS BFMATCH -> bf doesnt repeat kp matching 
### TRY USING FEATURE MATCHING + HOMOGRAPHY FOR LOC
#  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = bf.knnMatch(des1,des2,k=2)
#  matches = bf.match(des1,des2)
#  matches=sorted(matches, key= lambda x:x.distance)
  good = []
  for i,j in matches:
#    if i.distance < 0.3*j.distance:
    if i.distance < 0.7*j.distance:
      good.append([i])
  # still getting error pos of kp
  lkp1 = [kp1[mat[0].queryIdx].pt for mat in good]  
  lkp2 = [kp1[mat[0].trainIdx].pt for mat in good]  
  lkp3 = [kp1[mat[0].imgIdx].pt for mat in good]  
#  print(lkp1)
#  print(lkp2)
#  print(lkp3)

#  for c in good:
#    print(c[0])
#    p1 = kp1[c[0].queryIdx].pt
#    p2 = kp1[c[0].trainIdx].pt
#    p3 = kp1[c[0].imgIdx].pt
#    print('p1: ',p1)
#    print('p2: ',p2)
#    print('p3: ',p3)
#
#  print('img1 shape: ', img1.shape)
#  print('img2 shape: ', img2.shape)
  img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
#  img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None)
  
#  img4 = cv2.circle(img1,(493, 171),3,(127,0,0),-1)
#  ma = max(lkp2)
#  print('max: ',ma[0])
#  img5 = img1[int(ma[0]):, 171:]
  
  return len(good)
#  cv2.imshow('a',img3)
#  cv2.imshow(img1_p,img3)
#  cv2.waitKey(0)
#  cv2.imshow('ass',img5)
#  cv2.waitKey(0)
# draw only keypoints location,not size and orientation
#  img1 = cv2.drawKeypoints(img1, kp1, None, color=(0,255,0), flags=0)
#  img2 = cv2.drawKeypoints(img2, kp2, None, color=(0,255,0), flags=0)
#  plt.imshow(img1), plt.show()
#  klt.imshow(img2), plt.show()

#whichLevel(levels[4], levels[1])
#print(levels[0])
#for i in levelsC:
best = -1
nM = -1
# Fails with idx: 11, 15
c = levels[8]
#d = levels[14]
#d = p[1][0] # spikes
#d = p[0][0]
#d = p[13][0]
#print(type(p[9]))
#print(d)
#whichLevel(c, d)
for idx,i in enumerate(levels):
  n = whichLevel(c, i)
  print(n)
  if n > nM:
    nM = n
    best = idx

img1 = cv2.imread(c, cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(levels[best], cv2.IMREAD_GRAYSCALE)

cv2.imshow(c,img1)
cv2.imshow(levels[best],img2)

cv2.waitKey(0)
cv2.destroyAllWindows()
print(c)
print(levels[best])
#print('nMatches: ', nM)
#print('best', best)
#whichLevel(objs[6][1], levels[1])
