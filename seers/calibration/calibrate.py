import numpy as np
import cv2
import glob
import time
import argparse
import os
import sys

parser = argparse.ArgumentParser(description='Calibrates cameras using chessboard calibration')
parser.add_argument('--path', help='Path to preexisting training files', required=False)
parser.add_argument('--num', help='Number of images to calibrate using, default is 10', required=False)

images = None
args = parser.parse_args()

if args.path:
    if not os.path.isdir(args.path) or len(os.listdir(args.path)) == 0:
        print('Invalid or empty directory')
        sys.exit()
    else:
        images = glob.glob('{}/*.jpg'.format(args.path))


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.


# Gathering data
num = -1

if args.num:
    num = args.num
else:
    num = 10

num_pics = 0

video = None
if not images:
    video = cv2.VideoCapture(0)

if video is not None:
    while num_pics < num:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        found, corners = cv2.findChessboardCorners(gray, (9,6), None)
        if found == True:
            cv2.imwrite('./images/chessboard-{}.jpg'.format(num_pics), gray)
            num_pics += 1

            objpoints.append(objp)
            imgpoints.append(corners)

            print('Found a picture, waiting 5 seconds')
            time.sleep(5)

    video.release()
    cv2.destroyAllWindows()
else:
    # We already have an image directory
    for image in images:
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        found, corners = cv2.findChessboardCorners(gray, (9,6), None)

        if found == True:
            objpoints.append(objp)
            imgpoints.append(corners)

# Actual calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

img = cv2.imread('./images/chessboard-0.jpg')
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

undistorted = cv2.undistort(img, mtx, dist, None, newcameramtx)
x, y, w, h = roi
undistorted = undistorted[y:y+h, x:x+w]
cv2.imwrite('./generated/result.jpg', undistorted)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )