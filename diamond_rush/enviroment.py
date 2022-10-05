#!/usr/bin/env python3
import cv2 
import numpy as np
import os

levels_dir = './levels/cropHalf2/'
#levels_dir = './levels/'
levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if x[len(x)-3:] == 'png']
### TODO SORT LEVELS
#print(levels)

# TODO SET LEVELS AS GLOBAL VARIABLES

def matchLevels(img1_p,img2_p):
  from matplotlib import pyplot as plt
#  img1 = cv2.imread(img1_p, cv2.IMREAD_GRAYSCALE)
#  img2 = cv2.imread(img2_p, cv2.IMREAD_GRAYSCALE)
  img1 = cv2.imread(img1_p, cv2.IMREAD_UNCHANGED)
  img2 = cv2.imread(img2_p, cv2.IMREAD_UNCHANGED)

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
    if i.distance < 0.9*j.distance:
#    if i.distance < 0.7*j.distance:
      good.append([i])

  return len(good)

def whichLevel(ss):
  best = -1
  nM = -1
  # Fails with idx: 11, 15
  c = ss
  for idx,i in enumerate(levels):
    n = matchLevels(c, i)
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

