import cv2
import numpy as np
from matplotlib import pyplot as plt

calibration = np.load('./generated/calibration.npz', allow_pickle=False)
imageSize = tuple(calibration['imageSize'])
leftMapX = calibration['leftMapX']
leftMapY = calibration['leftMapY']
leftROI = tuple(calibration['leftROI'])
rightMapX = calibration['rightMapX']
rightMapY = calibration['rightMapY']
rightROI = tuple(calibration['rightROI'])

videoL = cv2.VideoCapture(0)
videoL.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
videoL.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

videoR = cv2.VideoCapture(1)
videoR.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
videoR.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

ret, frameL = videoL.read()
ret, frameR = videoR.read()

stereo = cv2.StereoBM_create()

fixedL = cv2.remap(frameL, leftMapX, leftMapY, cv2.INTER_LINEAR)
fixedR = cv2.remap(frameR, rightMapX, rightMapY, cv2.INTER_LINEAR)

fixedL = cv2.cvtColor(fixedL, cv2.COLOR_BGR2GRAY)
fixedR = cv2.cvtColor(fixedR, cv2.COLOR_BGR2GRAY)

#cv2.imwrite('./StereoTuner/left.png', fixedL)
#cv2.imwrite('./StereoTuner/right.png', fixedR)

cn = fixedL.shape[2] if len(fixedL.shape) > 2 else 3

#BM params
stereo.setBlockSize(9)
#stereo.setNumDisparities(48)
stereo.setTextureThreshold(507)

#SGBM params
#stereo.setBlockSize(9)
#stereo.setNumDisparities(32)
#stereo.setP1(500)
#stereo.setP2(900)

disparity = stereo.compute(fixedL, fixedR)
plt.imshow(disparity, 'gray')
plt.show()

