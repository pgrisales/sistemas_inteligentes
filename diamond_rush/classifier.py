#!/usr/bin/env python3
import cv2
import numpy as np
import os, shutil

# (1313, 882, 4)
# cx = 88; cy = 87
cx = 882//10
# best value for cy => 1321
cy = 1321//15

img_dir = './levels/'
imgs = [img_dir+str(x) for x in os.listdir(img_dir)]
idx = 0

def blockify(img_p):
  img = cv2.imread(img_p, cv2.IMREAD_UNCHANGED)
#  img = cv2.imread(img_p, cv2.IMREAD_GRAYSCALE)
  global idx
  for i in range(15):
    for j in range(10):
      bx = cx*(j+1)
      by = cy*(i+1)
#      if by > 1313: by = 1313
#      b = cv2.rectangle(img, (cx*j,cy*i), (cx*(j+1),cy*(i+1)), (0,255,0), thickness=2)
      img_b = img[cy*i:by, cx*j:bx]
      b_name = './blocks/b_' + str(idx) + '.png'
#      b_name = './gBlocks/gB_' + str(idx) + '.png'
      idx += 1
      print(idx)
      cv2.imwrite(b_name, img_b)

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
  import imagehash
  from PIL import Image
  searched = set()
  duplicates = set()
  i = 0
#  img1 = cv2.imread(p[0], cv2.IMREAD_GRAYSCALE)
#  h1 = imagehash.average_hash(Image.open(p[0]))
#  h2 = imagehash.average_hash(img1)
#  print(h1)
#  print(h2)
#  print(h2-h1)
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
#        print(diffM)
        if diffM < 5:
          duplicates.add(p[j])
          continue
#          if a != i:
#            cv2.imshow(p[i],img1)
#            cv2.imshow(p[j],img2)
#            cv2.waitKey(0)
#            cv2.destroyAllWindows()
#            a = i
    searched.add(p[i])
    i += 1
  for d in duplicates:
    os.remove(d)
  print(p[0])
  print('searched: ',len(searched))
  print('duplicates: ',len(duplicates))

blk_dir = './blocks/'
walls_dir = './blocks/walls/'
walls_dir = './blocks/walls/'
gBlk_dir = './gBlocks/'
lava_dir = './blocks/lava/'
keys_dir = './blocks/keys/'
holes_dir = './blocks/holes/'
agent_dir = './blocks/agent/'
button_dir = './blocks/button/'
diamonds_dir = './blocks/diamonds/'
goal_dir = './blocks/diamonds/'

#wB = [walls_dir+str(x) for x in os.listdir(walls_dir) if x[len(x)-3:] == 'png']
#lB = [lava_dir+str(x) for x in os.listdir(lava_dir) if x[len(x)-3:] == 'png']
#kB = [keys_dir+str(x) for x in os.listdir(keys_dir) if x[len(x)-3:] == 'png']
#hB = [holes_dir+str(x) for x in os.listdir(holes_dir) if x[len(x)-3:] == 'png']
#aB = [agent_dir+str(x) for x in os.listdir(agent_dir) if x[len(x)-3:] == 'png']
#bB = [button_dir+str(x) for x in os.listdir(button_dir) if x[len(x)-3:] == 'png']
#dB = [diamonds_dir+str(x) for x in os.listdir(diamonds_dir) if x[len(x)-3:] == 'png']

#ds = [os.path.join(blk_dir,x) for x in os.listdir(blk_dir) if os.path.isdir(os.path.join(blk_dir,x))]
#for i in ds:
#  p = [os.path.join(i,str(x)) for x in os.listdir(i) if x[len(x)-3:] == 'png']
#  cleanData(p)

#gBlks = [gBlk_dir+str(x) for x in os.listdir(gBlk_dir) if x[len(x)-3:] == 'png']
#blks = [blk_dir+str(x) for x in os.listdir(blk_dir) if x[len(x)-3:] == 'png']

#for i in imgs:
#  blockify(i)
#classifier(blks)
#rmEmptyF(blk_dir)
