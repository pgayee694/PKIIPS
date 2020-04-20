import cv2
import numpy as np
from matplotlib import pyplot as plt

videoL = cv2.VideoCapture(0)
videoL.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
videoL.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

videoR = cv2.VideoCapture(1)
videoR.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
videoR.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

orb = cv2.ORB_create()

ret, frameL = videoL.read()
ret, frameR = videoR.read()

frameL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
frameR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

kpL, desL = orb.detectAndCompute(frameL, None)
kpR, desR = orb.detectAndCompute(frameR, None)

# FLANN opts
FLANN_INDEX_LSH = 6
index_params = dict(algorithm=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(desL, desR, k=2)

good = []
ptsL = []
ptsR = []

# Lowe's ratio test
for i, (m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        good.append(m)
        ptsL.append(kpL[m.trainIdx].pt)
        ptsR.append(kpR[m.queryIdx].pt)

ptsL = np.array(ptsL)
ptsR = np.array(ptsR)

F, mask = cv2.findFundamentalMat(ptsL, ptsR, cv2.FM_RANSAC, 3, 0.99)

ptsL = ptsL[:,:][mask.ravel()==1]
ptsR = ptsR[:,:][mask.ravel()==1]

ptsL = np.int32(ptsL)
ptsR = np.int32(ptsR)

ptsLNew = ptsL.reshape((ptsL.shape[0]*2, 1))
ptsRNew = ptsR.reshape((ptsR.shape[0]*2, 1))

ret, rectL, rectR = cv2.stereoRectifyUncalibrated(ptsLNew, ptsRNew, F, frameL.shape[:2])

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
frameLNew = cv2.warpPerspective(frameL, rectL, frameL.shape[:2])
frameRNew = cv2.warpPerspective(frameR, rectR, frameR.shape[:2])
disparity = stereo.compute(frameLNew, frameRNew)

plt.imshow(disparity)
plt.show()