#!/usr/bin/env python3
import cv2 
import numpy as np
import os

def crop(img, top_left,bottom_right,save_dir):
  img = img[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
  cv2.imwrite(save_dir, img)

#levels_dir = './levels/cropHalf2/'
#levels_dir = './levels/crop/'
levels_dir = './levels/'
levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if x[len(x)-3:] == 'png']
### TODO SORT LEVELS
### TODO SET LEVELS AS GLOBAL VARIABLES

### TEMPLATE MATCHING... PROBLEMS WITH IMAGE OF DIFERENT SIZE
def matchI(img, templates):
  img = cv2.imread(img)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  bestMatch = -1
  matchValue = -9999
  print(img.shape)
  for idx, i in enumerate(templates):
    template = cv2.imread(i)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc 
    bottom_right = (top_left[0] + w, top_left[1] + h)
    mv = np.mean(res)
    if mv > matchValue:
      bestMatch = idx
      matchValue = mv

  return templates[bestMatch]

### BEST OVERALL
def mSift(img1_p,img2_p):
  MIN_MATCH_COUNT = 4
#  MIN_MATCH_COUNT = 10
  img1 = cv2.imread(img1_p) # queryImage
  img2 = cv2.imread(img2_p) # trainImage
  img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# Initiate SIFT detector
  sift = cv2.SIFT_create()
## find the keypoints and descriptors with SIFT
  kp1, des1 = sift.detectAndCompute(img1,None)
  kp2, des2 = sift.detectAndCompute(img2,None)

  FLANN_INDEX_KDTREE = 0
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)

  flann = cv2.FlannBasedMatcher(index_params, search_params)
  matches = flann.knnMatch(des1,des2,k=2)
# store all the good matches as per Lowe's ratio test.
  good = []
  for m,n in matches:
    if m.distance < 0.7*n.distance:
      good.append(m)
  if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    dst = np.int32(dst)
    tl = (dst[0][0][0], dst[0][0][1])
    br = (dst[2][0][0], dst[2][0][1])
    res = img2[tl[1]:br[1], tl[0]:br[0]]

#    cv2.imshow('CROP', res)
#    cv2.waitKey(0);cv2.destroyAllWindows()
    return res
#    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,9, cv2.LINE_AA)
#    cv2.rectangle(img2,tl,br , 255, 8)
#    crop(img2,tl,br,img2_p)
#    cv2.circle(img2,br,radius=0, color=(0,0,255), thickness=8)
  else:
    print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

def matchLevel(levels,img2_p):
  MIN_MATCH_COUNT = 4
#  MIN_MATCH_COUNT = 10
#  img2 = cv2.imread(mSift(levels[1],img2_p)) # queryImage
  img2 = mSift(levels[1],img2_p) # queryImage
#  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
  bestMatch = 0
  nMatches = -9999
# Initiate SIFT detector
  sift = cv2.SIFT_create()
  for idx,i in enumerate(levels):
    img1 = cv2.imread(i) # trainImage
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
## find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)
# store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
#      if m.distance < 0.7*n.distance:
      if m.distance < 0.1*n.distance:
        good.append(m)
    if len(good) > nMatches:
      bestMatch = idx
      nMatches = len(good)

  bMI = cv2.imread(levels[bestMatch])
#  bMI = cv2.cvtColor(bMI, cv2.COLOR_BGR2GRAY)
#  img3 = cv2.hconcat([bMI,img2])
  cv2.imshow('Best Match '+levels[bestMatch], bMI)
  cv2.waitKey(0);cv2.destroyAllWindows()
  cv2.imshow('Test Image', img2)
  cv2.waitKey(0);cv2.destroyAllWindows()

  return levels[bestMatch]

