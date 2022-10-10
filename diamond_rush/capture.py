#!/usr/bin/env python3
import cv2 
import numpy as np
import os

def crop(img, top_left,bottom_right,save_dir):
  img = img[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
  cv2.imwrite(save_dir, img)

levels_dir = './levels/'
agent_dir = './blocks/agent/2.png'
levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if x[len(x)-3:] == 'png']
### TODO SORT LEVELS
### TODO SET LEVELS AS GLOBAL VARIABLES

def agentPos(agentTemplate, levelTemplate):
  MIN_MATCH_COUNT = 4
#  MIN_MATCH_COUNT = 10
  level = getFrame(levels[1],levelTemplate) # queryImage
  agent = cv2.imread(agentTemplate) # trainImage
  agent = cv2.cvtColor(agent, cv2.COLOR_BGR2GRAY)

  sift = cv2.SIFT_create()
  kp1, des1 = sift.detectAndCompute(agent,None)
  kp2, des2 = sift.detectAndCompute(level,None)

  FLANN_INDEX_KDTREE = 0
  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
  search_params = dict(checks = 50)

  flann = cv2.FlannBasedMatcher(index_params, search_params)
  matches = flann.knnMatch(des1,des2,k=2)
  good = []
  for m,n in matches:
      if m.distance < 0.9*n.distance:
        good.append(m)
  print(len(good))
  if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    ah,aw = agent.shape
    pts = np.float32([ [0,0],[0,ah-1],[aw-1,ah-1],[aw-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)
    
    lh,lw= level.shape
    lh = lh//15
    lw = lw//10
    
    dst = np.int32(dst)
    tl = (dst[0][0][0], dst[0][0][1])
    br = (dst[2][0][0], dst[2][0][1])

    print('tl:', tl)
    print('br:', br)
    aPos = (tl[1]//lw,tl[0]//lh)
    print('agent position:', aPos)

    cv2.rectangle(level,tl,br , 255, 3)
#    cv2.circle(level,tl,radius=0, color=(0,0,255), thickness=8)
    cv2.imshow('CROP', level)
    cv2.waitKey(0);cv2.destroyAllWindows()
#    print('tl:',tl)
#    print('lh:',lh)
#    print('lw:',lw)
    return aPos  

### BEST OVERALL
def getFrame(img1_p,img2_p):
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
#  img2 = cv2.imread(getFrame(levels[1],img2_p)) # queryImage
  img2 = getFrame(levels[1],img2_p) # queryImage
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

def matchLevel2(levels,img2_p):
  MIN_MATCH_COUNT = 4
#  MIN_MATCH_COUNT = 10
  img2 = cv2.imread(img2_p) # queryImage
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
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

  #bMI = cv2.imread(levels[bestMatch])
  #cv2.imshow('Best Match '+levels[bestMatch], bMI)
  #cv2.waitKey(0);cv2.destroyAllWindows()
  #cv2.imshow('Test Image', img2)
  #cv2.waitKey(0);cv2.destroyAllWindows()

  return levels[bestMatch]
