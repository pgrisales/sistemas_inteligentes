#!/usr/bin/env python3
import cv2 
import numpy as np
# import glob // glob vs manually
import os

levels_dir = './levels/'
levelsC_dir = './levels/cropHalf2/'
blks_dir = './blocks/'
#levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if os.path.isdir(os.path.join(levels_dir,x))]
levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if x[len(x)-3:] == 'png']
levelsC = [os.path.join(levelsC_dir,x) for x in os.listdir(levelsC_dir) if x[len(x)-3:] == 'png']
blks = [os.path.join(blks_dir,x) for x in os.listdir(blks_dir) if os.path.isdir(os.path.join(blks_dir,x))]
p = []
for i in blks:
  p.append([os.path.join(i,str(x)) for x in os.listdir(i) if x[len(x)-3:] == 'png'])

objs = []
for idx,i in enumerate(blks):
  objs.append([os.path.join(i,x) for x in os.listdir(i) if x[len(x)-3:] == 'png'])

def blockify(img_p):
  img = cv2.imread(img_p, cv2.IMREAD_GRAYSCALE)
  bs = 88
  blks = np.empty([15,10], dtype=object) 

  for i in range(15):
    for j in range(10):
      x = bs*(j+1)
      y = bs*(i+1)
      img_b = img[bs*i:y, bs*j:x]
      blks[i,j] = img_b
#  cv2.imshow('a',blks[0,5])
#  cv2.waitKey(0)
  return blks 

def crop(a):
  ai = cv2.imread(a, cv2.IMREAD_UNCHANGED)
# Define size of new Image
  ai = ai[88*5:len(ai)-88, 88:len(a[0])-88]
  cv2.imwrite(a,ai)
#  cv2.imshow('a',ai)
#  cv2.waitKey(0)

#for i in levelsC:
#  crop(i)

count = 0
### Creates Matrix -> for all levels... still not good accurate
def extract(objs, env):
  mapView= np.chararray((15,10),unicode=True)
  mapView.fill('x')
#  mapView[:] = 'x'
  env_blks = blockify(env)
  global count
  for i in range(15):
    for j in range(10):
#      envB = cv2.imread(env_blks[i,j], cv2.IMREAD_GRAYSCALE)
      diffM = -1
      for k in range(0,len(objs)):
# no funciona igualdad pq son bytes -> cast
#        if mapView[i,j].decode('utf-8') != 'x':
#          break
#        print(i,j, mapView[i,j])
        for z in objs[k]:
#          print(z)
          objB = cv2.imread(z, cv2.IMREAD_GRAYSCALE)
          if objB.shape == (88,88) and env_blks[i,j].shape == (88,88):
            diff = cv2.absdiff(objB,env_blks[i,j])
            diffM = np.mean(diff)
            if diffM < 5:
              # 4 -> 2283/140 = 16.30
#              cv2.imshow('a',objB)
#              cv2.imshow('b',env_blks[i,j])
#              cv2.waitKey(0)
              if k == 0:
                mapView[i,j] = 'a' # agent
                count += 1
                break
              elif k == 1:
                mapView[i,j] = 's' # spikes
                count += 1
                print('spike in: ', i,j)
                break
              elif k == 2:
                mapView[i,j] = 'K' # kdoors
                count += 1
                break
              elif k == 3:
                mapView[i,j] = 'g' # goal
                count += 1
                break
              elif k == 4:
                mapView[i,j] = 'k' # keys
                count += 1
                break
              elif k == 5:
                mapView[i,j] = 'l' # lava
                count += 1
                break
              elif k == 6:
                mapView[i,j] = 'w' # wall
                count += 1
                break
              elif k == 7:
                mapView[i,j] = 'd' # diamonds
                count += 1
                break
              elif k == 8:
                mapView[i,j] = 'b' # button
                count += 1
                break
              elif k == 9:
                mapView[i,j] = 'h' # holes
                count += 1
                break
              elif k == 10:
                mapView[i,j] = 'B' # bDoor
                count += 1
                break
              elif k == 11:
                mapView[i,j] = 'r' # rock
                count += 1
                break
              elif k == 12:
                mapView[i,j] = 'p' # path
                count += 1
                break
  print(mapView)
  print()
  print(env)
  print('count: ',count)
  print()
  return mapView

#for i in levels:
#  m = extract(objs,i)
#  np.savetxt('./levels/default_init_states/'+i[9:len(i)-4], m,fmt='%c')
load = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)

# SEARCH MULT. SOURCE IMG MATCHING

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

# THRESHOLD VALUES WORKING 
#diamonds = objPos(level1_path,diamond_path,0.01, 0.5)
#spikes = objPos(level1_path,spikes_path,0.0019, 0.5)
#goal = objPos(level1_path,goal_path,0.001,0.5)
# FOR WALL NEED TO ADD MORE WALL IMAGES FOR BETTER RESULTS

def mapObjLoc(state):
  test = np.zeros((15,10))
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
#for idx,i in enumerate(levels):
#  n = whichLevel(c, i)
#  print(n)
#  if n > nM:
#    nM = n
#    best = idx
#
#img1 = cv2.imread(c, cv2.IMREAD_GRAYSCALE)
#img2 = cv2.imread(levels[best], cv2.IMREAD_GRAYSCALE)
#
#cv2.imshow(c,img1)
#cv2.imshow(levels[best],img2)
#
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#print(c)
#print(levels[best])
#print('nMatches: ', nM)
#print('best', best)
#whichLevel(objs[6][1], levels[1])
