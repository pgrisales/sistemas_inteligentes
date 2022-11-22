import cv2 
import numpy as np
import os

levels_dir = './levels/'
agent_dir = './blocks/agent/2.png'
levels = [os.path.join(levels_dir,x) for x in os.listdir(levels_dir) if x[len(x)-3:] == 'png']

def agent_pos(levelTemplate):
  MIN_MATCH_COUNT = 4
#  MIN_MATCH_COUNT = 10
  level = levelTemplate # queryImage
  level = cv2.cvtColor(level, cv2.COLOR_BGR2GRAY)
  agent = cv2.imread(agent_dir) # trainImage
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
#  print(len(good))
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

#    print('tl:', tl)
#    print('br:', br)
    aPos = ((tl[1]+10)//lh, (tl[0]+10)//lw)
    print('agent position:', aPos)

#    cv2.rectangle(level,tl,br , 255, 3)
##    cv2.circle(level,tl,radius=0, color=(0,0,255), thickness=8)
#    cv2.imshow('CROP', level)
#    cv2.waitKey(0);cv2.destroyAllWindows()
#    print('tl:',tl)
#    print('lh:',lh)
#    print('lw:',lw)
    return aPos  

