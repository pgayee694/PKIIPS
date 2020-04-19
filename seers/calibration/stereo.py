import cv2
import numpy as np
from matplotlib import pyplot as plt

videoL = cv2.VideoCapture(0)
videoR = cv2.VideoCapture(1)

while(True):
    ret, frameL = videoL.read()
    ret, frameR = videoR.read()

    frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
    frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

    stereo = cv2.StereoSGBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(frameL, frameR)
    plt.imshow(disparity, 'gray')
    plt.show()
