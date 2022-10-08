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

def crop(img, top_left,bottom_right,save_dir):
  img = img[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
  cv2.imwrite(save_dir, img)

### Creates Matrix -> for all levels... still not good accurate
load = np.loadtxt('./levels/default_init_states/0',dtype=str)#.reshape(15,10)

