#!/usr/bin/env python3
import cv2 
import numpy as np
from capture import levels
from capture import matchLevel 
from capture import matchLevel2 
from capture import agentPos 
from capture import agent_dir
from test import t
from random import randint

# PONER EL PATH DE LA IMG DE PRUEBA
test_img = './test_img.png'
for i in range(10):
  i = randint(0,len(t)-1)
  j = randint(0,len(t[i])-1)
  print(agentPos(agent_dir, t[i][j]))
print(agentPos(agent_dir, test_img))
print(matchLevel(levels, test_img))

