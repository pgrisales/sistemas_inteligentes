#!/usr/bin/env python3
import cv2 
import numpy as np
from enviroment import capture
from enviroment import mL
from enviroment import levels
#from enviroment import mSift 
from enviroment import matchLevel 
from test import t

# PONER EL PATH DE LA IMG DE PRUEBA
test_img = './test_img.png'
print(matchLevel(levels,test_img))
