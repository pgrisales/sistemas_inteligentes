#!/usr/bin/env python3
import cv2 
import numpy as np
from capture import levels
from capture import matchLevel 
from capture import matchLevel2 
from capture import agentPos 
from capture import agent_dir
#from test import t

# PONER EL PATH DE LA IMG DE PRUEBA
test_img = './test_img.png'

print(matchLevel(levels, test_img))

