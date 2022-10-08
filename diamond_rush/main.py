#!/usr/bin/env python3
import cv2 
import numpy as np
from capture import levels
from capture import matchLevel 

# PONER EL PATH DE LA IMG DE PRUEBA
test_img = './test_img.png'

print(matchLevel(levels, test_img))

