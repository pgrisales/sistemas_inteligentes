#!/usr/bin/env python3
import cv2 
import numpy as np
import os
from capture import crop

#levels_dir = './levels/cropHalf2/'
#levels_dir = './levels/crop/'
levels_dir = './levels/'
levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if x[len(x)-3:] == 'png']
### TODO SORT LEVELS
### TODO SET LEVELS AS GLOBAL VARIABLES

#def reject_outliers(data, m=2):
#  return data[for i in data if abs(len(data) - np.mean(data)) < m * np.std(data)]

### TODO -> improve this function... also test removing outlier instead of asigning previous value
def reject_outliers(data, m=0.6):
  mean = np.mean(data)
  std = np.std(data)
  for i in range(len(data)) :
    if np.abs(data[i] -mean) > m*std :
      data[i] = data[i-1]
  return data

### TEMPLATE MATCHING... PROBLEMS WITH IMAGE OF DIFERENT SIZE
def matchI(img, templates):
  bestMatch = -1
  matchValue = -9999
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

# INIT -> TODO TAKE BROWSER SCREEENSHOT THEN CALL capture: crop game zone
def capture(img_p,templates):
  from matplotlib import pyplot as plt
  img = cv2.imread(img_p)
#  template = cv2.imread(template_p)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  tly = []
  tlx = []
  bry = []
  brx = []
  for i in templates:
    template = cv2.imread(i)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc 
    bottom_right = (top_left[0] + w, top_left[1] + h)
#    print(top_left, bottom_right)
    tly.append(top_left[1])
    tlx.append(top_left[0])
    bry.append(bottom_right[1])
    brx.append(bottom_right[0])
#    print(img_p, i)
#    print()
  
#  print('tlx: ',tlx)
#  print(tly)
#  print()
#  print('noOutliers: ',reject_outliers(tlx))
#  print(reject_outliers(tly))
#  print()

####### TO IMPLEMENT #####################
  tl = [int(np.mean(reject_outliers(tlx))),int(np.mean(reject_outliers(tly)))]
  br = [int(np.mean(reject_outliers(brx))),int(np.mean(reject_outliers(bry)))]

  res = img[tl[1]:br[1], tl[0]:br[0]]
  plt.imshow(res,cmap = 'gray')
  plt.show()
  return matchI(res,templates)

#  crop(img,tl,br,img_p)
##########################################  
####### TO TEST #####################
#  tl = [int(np.mean(reject_outliers(tlx))),int(np.mean(reject_outliers(tly)))]
#  br = [int(np.mean(reject_outliers(brx))),int(np.mean(reject_outliers(bry)))]
#  print('tl, br', tl, br)
#  cv2.rectangle(img,tl, br, 255, 8)
#  plt.imshow(img,cmap = 'gray')
#  plt.show()


#  plt.imshow(img[tl[0]:br[0],img[tl[1]:br[1]]],cmap = 'gray')

#  crop(img,top_left,bottom_right,img_p)
#  print(np.mean(res))
#  return np.mean(res)
#  cv2.rectangle(img,top_left, bottom_right, 255, 8)

#  plt.imshow(img,cmap = 'gray')
#  plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#  plt.show()

### BEST OVERALL
def mSift(img1_p,img2_p):
  from matplotlib import pyplot as plt
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
    print(dst)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,9, cv2.LINE_AA)
    plt.imshow(img2, 'gray'),plt.show()

  else:
    print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    matchesMask = None

#  img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None)
#  plt.imshow(img3, 'gray'),plt.show()

### FEATURE MATCHING BFMATCHING AND HOMOGRAPHY-> getting some errors
def mL(img1_p,img2_p):
  from matplotlib import pyplot as plt
  MIN_MATCH_COUNT = 4  
#  img1 = cv2.imread(img1_p, cv2.IMREAD_GRAYSCALE)
#  img2 = cv2.imread(img2_p, cv2.IMREAD_GRAYSCALE)
  img1 = cv2.imread(img1_p)
  img2 = cv2.imread(img2_p)
# IMG2GRAY
  img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

  orb = cv2.ORB_create()
  kp1, des1 = orb.detectAndCompute(img1,None)
  kp2, des2 = orb.detectAndCompute(img2,None)
  
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = bf.match(des1,des2)
  dmatches = sorted(matches, key = lambda x:x.distance)  
## extract the matched keypoints
  src_pts  = np.float32([kp1[m.queryIdx].pt for m in dmatches]).reshape(-1,1,2)
  dst_pts  = np.float32([kp2[m.trainIdx].pt for m in dmatches]).reshape(-1,1,2)
## find homography matrix and do perspective transform
  M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
  h,w = img1.shape[:2]
  pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
  dst = cv2.perspectiveTransform(pts,M)
## draw found regions
  img2 = cv2.polylines(img2, [np.int32(dst)], True, (0,0,255), 8, cv2.LINE_AA)
#  cv2.imshow("found", img2)
  plt.imshow(img2,'gray'),plt.show()
# draw match lines
#  res = cv2.drawMatches(img1, kp1, img2, kp2, dmatches[:90],None,flags=2)
#  cv2.imshow("orb_match", res);
#  cv2.waitKey();cv2.destroyAllWindows()

#  img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches, None)
#  plt.imshow(img3, 'gray'), plt.show()

  return len(matches)


### FEATURE MATCHING KNN-> getting some errors
def matchLevels(img1_p,img2_p):
  from matplotlib import pyplot as plt
#  img1 = cv2.imread(img1_p, cv2.IMREAD_GRAYSCALE)
#  img2 = cv2.imread(img2_p, cv2.IMREAD_GRAYSCALE)
  img1 = cv2.imread(img1_p)
  img2 = cv2.imread(img2_p)
  img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
  img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

  orb = cv2.ORB_create()

  kp1, des1 = orb.detectAndCompute(img1,None)
  kp2, des2 = orb.detectAndCompute(img2,None)
  
  bf = cv2.BFMatcher.create()
### TRY USING FEATURE MATCHING + HOMOGRAPHY FOR LOC
  matches = bf.knnMatch(des1,des2,k=2)
  good = []
  for i,j in matches:
#    if i.distance < 0.3*j.distance:
    if i.distance < 0.8*j.distance:
      good.append([i])

#  img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None)
#  plt.imshow(img3, 'gray'), plt.show()
  return len(good)

def whichLevel(ss):
  best = -1
  nM = -1
  # Fails with idx: 11, 15
  c = ss
  for idx,i in enumerate(levels):
#    n = matchLevels(c, i)
#    n = mL(i, c)
    n = capture(c,i)
    print(n)
    if n > nM:
      nM = n
      best = idx

  print(c)
  print(levels[best])
  return levels[best]

### set up level... its variables,and state 
class Level:
  diamonds = 0
  state = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)
  def __init__(self,whichLevel):
    self.level = whichLevel

### manage interactions btw Level and Agent... and it captures image of enviroment, dk if rules goes here or in level
class Enviroment:
#  level = Level(whichLevel())
#  state = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)
  ### TODO: check if agent has change pos, add metadata of levels as txt... add rules
  ### TODO probably need to remember 2 states back for spikes and some rocks interactions...
  
  def __init__(self):
    pass

class Agent:
  def __init__(self,pos):
    self.agentPos = pos

  def compute():
    pass

