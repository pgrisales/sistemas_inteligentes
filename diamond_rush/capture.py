#!/usr/bin/env python3
import cv2 
import numpy as np
import glob
import os

levels_dir = './levels/'
levelsC_dir = './levels/crop/'
blks_dir = './blocks/'
#levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if os.path.isdir(os.path.join(levels_dir,x))]
levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if x[len(x)-3:] == 'png']
levelsC = [os.path.join(levelsC_dir,x) for x in os.listdir(levelsC_dir) if x[len(x)-3:] == 'png']
blks = [os.path.join(blks_dir,x) for x in os.listdir(blks_dir) if os.path.isdir(os.path.join(blks_dir,x))]
#mapView= np.chararray((15,10))
#mapView[:] = 'p'
objs = []
for idx,i in enumerate(blks):
  objs.append([os.path.join(i,x) for x in os.listdir(i) if x[len(x)-3:] == 'png'])

def blockify(img_p):
  img = cv2.imread(img_p, cv2.IMREAD_GRAYSCALE)
  bs = 88
  blks = np.empty([15,10], dtype=object) 
#  print(img.shape)
#  print(blks)
#  print(blks[0,1])
  for i in range(15):
    for j in range(10):
      x = bs*(j+1)
      y = bs*(i+1)
#      print(x)
      #img_b = img[bs*i:y][bs*j:x]
      img_b = img[bs*i:y, bs*j:x]
      blks[i,j] = img_b
#      cv2.imshow('a',blks[i,j])
#      cv2.waitKey(0)
#      print(img_b)
#  print(blks[0,0])
#  cv2.imshow('a',blks[0,5])
#  cv2.waitKey(0)
  return blks 

#for i in range(0,len(objs)):
#  print(objs[i][0])
#print(objs[2][0])
#print(objs[3][0])
#aa = blockify(levels[0])

def extractI(img1_p,img2_p):
  from matplotlib import pyplot as plt
  img1 = cv2.imread(img1_p, cv2.IMREAD_GRAYSCALE)
  img2 = cv2.imread(img2_p, cv2.IMREAD_GRAYSCALE)
# Initiate ORB detector
  orb = cv2.ORB_create()
# find the keypoints with ORB
#  kp1 = orb.detect(img1,None)
#  kp2 = orb.detect(img2,None)
# compute the descriptors with ORB
#  kp1, des1 = orb.compute(img1,None)# kp1)
#  kp2, des2 = orb.compute(img2,None)# kp2)
  kp1, des1 = orb.detectAndCompute(img1,None)# kp1)
  kp2, des2 = orb.detectAndCompute(img2,None)# kp2)
  
  bf = cv2.BFMatcher()
  matches = bf.knnMatch(des1,des2,k=2)

  good = []
  for i,j in matches:
    if i.distance < 0.3*j.distance:
      good.append([i])
  img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
  
  return len(good)
#  cv2.imshow('a',img3)
#  cv2.waitKey(0)
# draw only keypoints location,not size and orientation
#  img1 = cv2.drawKeypoints(img1, kp1, None, color=(0,255,0), flags=0)
#  img2 = cv2.drawKeypoints(img2, kp2, None, color=(0,255,0), flags=0)
#  plt.imshow(img1), plt.show()
#  plt.imshow(img2), plt.show()

"""
# Initiate FAST object with default values
  fast = cv2.FastFeatureDetector_create()
# find and draw the keypoints
  kp = fast.detect(a,None)
  c = cv2.drawKeypoints(a, kp, None, color=(255,0,0))
# Print all default params
  print( "Threshold: {}".format(fast.getThreshold()) )
  print( "nonmaxSuppression:{}".format(fast.getNonmaxSuppression()) )
  print( "neighborhood: {}".format(fast.getType()) )
  print( "Total Keypoints with nonmaxSuppression: {}".format(len(kp)) )
  cv2.imwrite('fast_true.png', c)
# Disable nonmaxSuppression
  fast.setNonmaxSuppression(0)
  kp = fast.detect(a, None)
  print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )
  d = cv2.drawKeypoints(a, kp, None, color=(255,0,0))
  cv2.imwrite('fast_false.png', d)
"""
#extractI(levels[4], levels[1])
#print(levels[0])
#for i in levelsC:
best = -1
nM = -1
# Fails with idx: 11, 15
c = levels[11]
#d = levels[14]
#n = extractI(c, d)
for idx,i in enumerate(levels):
  n = extractI(c, i)
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
print('nMatches: ', nM)
print('best', best)
#extractI(objs[6][1], levels[1])
"""
"""
def crop(a):
  ai = cv2.imread(a, cv2.IMREAD_GRAYSCALE)
# Define size of new Image
  ai = ai[88*3:len(ai)-88, 88:len(a[0])-88]
#  cv2.imwrite(a,ai)
#  cv2.imshow('a',ai)
#  cv2.waitKey(0)

#crop(levels[0])
#for i in levelsC:
#  crop(i)
#  extractI(ai,a)

def extract(objs, env):
  mapView= np.chararray((15,10))
  mapView[:] = 'x'
  env_blks = blockify(env)
  for i in range(15):
    for j in range(10):
#      envB = cv2.imread(env_blks[i,j], cv2.IMREAD_GRAYSCALE)
      for k in range(0,len(objs)):
        print(i,j, mapView[i,j])
        for z in objs[k]:
#          print(z)
          objB = cv2.imread(z, cv2.IMREAD_GRAYSCALE)
          if objB.shape == (88,88) and env_blks[i,j].shape == (88,88):
            diff = cv2.absdiff(objB,env_blks[i,j])
            diffM = np.mean(diff)
            if diffM < 12:
#              cv2.imshow('a',objB)
#              cv2.imshow('b',env_blks[i,j])
#              cv2.waitKey(0)
              if k == 0:
                mapView[i,j] = 'a' # agent
              elif k == 1:
                mapView[i,j] = '@' # spikes
                print('spike in: ', i,j)
              elif k == 2:
                mapView[i,j] = 'q' # kdoors
              elif k == 3:
                mapView[i,j] = 'g' # goal
              elif k == 4:
                mapView[i,j] = 'k' # keys
              elif k == 5:
                mapView[i,j] = 'l' # lava
              elif k == 6:
                mapView[i,j] = 'w' # wall
              elif k == 7:
                mapView[i,j] = 'd' # diamonds
              elif k == 8:
                mapView[i,j] = 'b' # button
              elif k == 9:
                mapView[i,j] = 'h' # holes
              elif k == 10:
                mapView[i,j] = 'v' # bDoor
              elif k == 11:
                mapView[i,j] = 'r' # stones
              elif k == 12:
                mapView[i,j] = 'p' # path
              break
      if mapView != 'x':
        continue
  print(mapView)

#extract(objs,levels[1])
# PRUEBA MULT SOURCE IMG MATCHING
#level1_img = cv2.imread(level1_path)
#tmp_dat = []
#f1 = glob.glob('./img/path*.png')
#
#for f in f1:
#  im = cv2.imread(f,0)
#  tmp_dat.append(im)
#
#for tmp in tmp_dat:
#  (tH, tW) = tmp.shape[:2]
#  cv2.imshow("Template", tmp)
#  cv2.waitKey(1000)
#  cv2.destroyAllWindows()
#  result = cv2.matchTemplate(tmp,level1_img, cv2.TM_CCOEFF)
#  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#  top_left = max_loc
#  bottom_right = (top_left[0] + tW, top_left[1] + tH)
#  cv2.rectangle(level1_img,top_left, bottom_right,255, 2)
#
#cv2.imshow('Result',level1_img)
#cv2.waitKey(0)
# end prueba

def objPos(env,obj,t,eps):
  env_img = cv2.imread(env, cv2.IMREAD_UNCHANGED)
  obj_img = cv2.imread(obj, cv2.IMREAD_UNCHANGED)

  obj_shape = obj_img.shape
  obj_match = cv2.matchTemplate(env_img, obj_img, cv2.TM_SQDIFF_NORMED)

  locations = np.where(obj_match <= t)
  locations = list(zip(*locations[::-1]))
  
  rectangles = []
  for loc in locations:
    rect = [int(loc[0]), int(loc[1]), obj_shape[1], obj_shape[0]]
    # Add every box to the list twice in order to retain single (non-overlapping) boxes
    rectangles.append(rect)
    rectangles.append(rect)

#  rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
  rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=eps)
  points = []

  if len(rectangles):
    line_color = (0, 255, 0)
    line_type = cv2.LINE_4
    marker_color = (255, 0, 255)
    marker_type = cv2.MARKER_CROSS

    # Loop over all the rectangles
    for (x, y, w, h) in rectangles:
      # Determine the center position
      center_x = x + int(w/2)
      center_y = y + int(h/2)
      # Save the points
      points.append((center_x, center_y))
      # Determine the box position
      top_left = (x, y)
      bottom_right = (x + w, y + h)
      # Draw the box
      a = cv2.rectangle(env_img, top_left, bottom_right, color=line_color, lineType=line_type, thickness=2)
    cv2.imshow('Matches', a)
    cv2.waitKey()
  return points


#path = objPos(level1_path,path_path,0.0007, 0.2)
# THRESHOLD VALUES WORKING 
#diamonds = objPos(level1_path,diamond_path,0.01, 0.5)
#spikes = objPos(level1_path,spikes_path,0.0019, 0.5)
#goal = objPos(level1_path,goal_path,0.001,0.5)
# FOR WALL NEED TO ADD MORE WALL IMAGES FOR BETTER RESULTS
#wall,a = objPos(level1_path,wall_path,0.01,0.5)

def mapObjLoc(state):
  test = np.zeros((12,10))
  for idx, i in enumerate(state):
    for j in i:
      if idx == 0:
#      print('Sin nada: ',i[1],i[0])
#      print('Con Div: ', i[1]//86, i[0]//87)
        test[j[1]//86][j[0]//87] = 999
      elif idx == 1:
        test[j[1]//86][j[0]//87] = 888 
      elif idx == 2:
        test[j[1]//86][j[0]//87] = 777
  print()
  print(test) 


