#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import glob

level1_path = './img/level1.png'
mapView= np.zeros((12,10))

# Identifiable objects 
diamond_path = './img/diamond.png'
heroe_path = ''
rock_path = ''
spikes_path = './img/spikes.png'
hole_path = ''
goal_path = './img/goal.png'
path_path = './img/path.png'
wall_path = './img/wall.png'
button_path = ''
doors_path = ''

# PRUEBA MULT SOURCE IMG MATCHING
#level1_img = cv.imread(level1_path)
#tmp_dat = []
#f1 = glob.glob('./img/path*.png')
#
#for f in f1:
#  im = cv.imread(f,0)
#  tmp_dat.append(im)
#
#for tmp in tmp_dat:
#  (tH, tW) = tmp.shape[:2]
#  cv.imshow("Template", tmp)
#  cv.waitKey(1000)
#  cv.destroyAllWindows()
#  result = cv.matchTemplate(tmp,level1_img, cv.TM_CCOEFF)
#  min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
#  top_left = max_loc
#  bottom_right = (top_left[0] + tW, top_left[1] + tH)
#  cv.rectangle(level1_img,top_left, bottom_right,255, 2)
#
#cv2.imshow('Result',level1_img)
#cv2.waitKey(0)
# end prueba

def objPos(env,obj,t,eps):
  env_img = cv.imread(env, cv.IMREAD_UNCHANGED)
  obj_img = cv.imread(obj, cv.IMREAD_UNCHANGED)

  obj_shape = obj_img.shape
  obj_match = cv.matchTemplate(env_img, obj_img, cv.TM_SQDIFF_NORMED)

  locations = np.where(obj_match <= t)
  locations = list(zip(*locations[::-1]))
  
  rectangles = []
  for loc in locations:
    rect = [int(loc[0]), int(loc[1]), obj_shape[1], obj_shape[0]]
    # Add every box to the list twice in order to retain single (non-overlapping) boxes
    rectangles.append(rect)
    rectangles.append(rect)

#  rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
  rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=eps)
  points = []

  if len(rectangles):
    line_color = (0, 255, 0)
    line_type = cv.LINE_4
    marker_color = (255, 0, 255)
    marker_type = cv.MARKER_CROSS

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
      a = cv.rectangle(env_img, top_left, bottom_right, color=line_color, lineType=line_type, thickness=2)
    cv.imshow('Matches', a)
    cv.waitKey()
  return points


#path = objPos(level1_path,path_path,0.0007, 0.2)
# THRESHOLD VALUES WORKING 
diamonds = objPos(level1_path,diamond_path,0.01, 0.5)
spikes = objPos(level1_path,spikes_path,0.0019, 0.5)
goal = objPos(level1_path,goal_path,0.001,0.5)
# FOR WALL NEED TO ADD MORE WALL IMAGES FOR BETTER RESULTS
#wall,a = objPos(level1_path,wall_path,0.01,0.5)

# DIMENSIONS
#(1034, 871, 4)
#86.16666666666667 87.1
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

init_state = []
init_state.append(diamonds)
init_state.append(spikes)
init_state.append(goal)

#mapObjLoc(init_state)
mapObjLoc(init_state)

#print(len(init_state))
#print(init_state)

#print(len(diamonds))
#print(diamonds)
#print(len(path))
#print(path)

#cv.imshow('Matches', a)
#cv.waitKey()

#if __name__ '__main__':
#  return
