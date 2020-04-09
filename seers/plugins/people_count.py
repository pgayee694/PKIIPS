import seer_plugin
import seer_config
import cv2
import imutils
import imutils.video
import numpy
import os.path
import matplotlib.pyplot as plt
import numpy as np
import utils
import sys

class PeopleCount(seer_plugin.DataCollectorPlugin):
    """
        Data collector plugin that gathers video feed
        and uses models to determine the count of people
        in the video stream.
        """

    BACKGROUND_CLASS 	= "background"
    AEROPLANE_CLASS		= "aeroplane"
    BICYCLE_CLASS		= "bicycle"
    BIRD_CLASS 			= "bird"
    BOAT_CLASS 			= "boat"
    BOTTLE_CLASS 		= "bottle"
    BUS_CLASS 			= "bus"
    CAR_CLASS 			= "car"
    CAT_CLASS 			= "cat"
    CHAIR_CLASS 		= "chair"
    COW_CLASS 			= "cow"
    DININGTABLE_CLASS 	= "diningtable"
    DOG_CLASS 			= "dog"
    HORSE_CLASS 		= "horse"
    MOTORBIKE_CLASS 	= "motorbike"
    PERSON_CLASS 		= "person"
    POTTEDPLANT_CLASS 	= "pottedplant"
    SHEEP_CLASS 		= "sheep"
    SOFA_CLASS 			= "sofa"
    TRAIN_CLASS 		= "train"
    TVMONITOR_CLASS 	= "tvmonitor"

    CLASSES = \
            [
                    BACKGROUND_CLASS 	,
                    AEROPLANE_CLASS		,
                    BICYCLE_CLASS		,
                    BIRD_CLASS 			,
                    BOAT_CLASS 			,
                    BOTTLE_CLASS 		,
                    BUS_CLASS 			,
                    CAR_CLASS 			,
                    CAT_CLASS 			,
                    CHAIR_CLASS 		,
                    COW_CLASS 			,
                    DININGTABLE_CLASS 	,
                    DOG_CLASS 			,
                    HORSE_CLASS 		,
                    MOTORBIKE_CLASS 	,
                    PERSON_CLASS 		,
                    POTTEDPLANT_CLASS 	,
                    SHEEP_CLASS 		,
                    SOFA_CLASS 			,
                    TRAIN_CLASS 		,
                    TVMONITOR_CLASS 	,
                    ]

    INI 		= 'people-count'
    CONFIDENCE_INI	= 'confidence'
    MODEL_INI		= 'model-path'
    PROTOTXT_INI	= 'prototxt-path'
    RPI_MODEL_INI       = 'rpi-model-path'
    LABELMAP_INI        = 'labelmap-path'

    DEFAULT_CONFIDENCE	= 0.2
    COUNT_KEY			= 'count'
    DISTANCES_KEY = 'distances'

    def init(self):
        """
        Gets configuration for confidence and model paths.
        Sets up the network and video stream.
        """
        self.confidence = seer_config.configuration[PeopleCount.INI].getfloat(PeopleCount.CONFIDENCE_INI, fallback=PeopleCount.DEFAULT_CONFIDENCE)
        self.model		= seer_config.configuration[PeopleCount.INI].get(PeopleCount.MODEL_INI)
        self.prototxt	= seer_config.configuration[PeopleCount.INI].get(PeopleCount.PROTOTXT_INI)
        self.rpi_model  = seer_config.configuration[PeopleCount.INI].get(PeopleCount.RPI_MODEL_INI)
        self.labelmap   = seer_config.configuration[PeopleCount.INI].get(PeopleCount.LABELMAP_INI)

        if not os.path.isfile(self.model):
            raise IOError(self.model)
        if not os.path.isfile(self.prototxt):
            raise IOError(self.prototxt)

        self.net		= cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        self.videoL             = cv2.VideoCapture(0)
        self.videoR             = cv2.VideoCapture(1)

        calibration = np.load('./calibration/generated/calibration.npz', allow_pickle=False)
        self.calib_size = tuple(calibration['imageSize'])
        self.leftMapX = calibration['leftMapX']
        self.leftMapY = calibration['leftMapY']
        self.leftROI = tuple(calibration['leftROI'])
        self.rightMapX = calibration['rightMapX']
        self.rightMapY = calibration['rightMapY']
        self.rightROI = tuple(calibration['rightROI'])
        self.focal_length = 3.04
        self.baseline = 254

        self.stereoMatcher = cv2.StereoBM_create()
        #self.stereoMatcher.setMinDisparity(4)
        self.stereoMatcher.setNumDisparities(32)
        self.stereoMatcher.setBlockSize(15)

    def shutdown(self):
        """
        Stops the video stream.
        """
        self.video.stop()

    def collect(self):
        """
        Collects a frame from the video stream, runs it through
        the network, and count the number of model detections
        in the frame.

        Returns:
            (dictionary): A dictionary with one key: PeopleCount.COUNT_KEY,
                                          with its value being the count of people in the current
                                          frame of the video feed.
        """
        ret, frameL = self.videoL.read()
        #frameL = imutils.resize(frameL, width=400)

        ret, frameR = self.videoR.read()
        #frameR = imutils.resize(frameR, width=400)

        height, width	= frameL.shape[:2]
        blob			= cv2.dnn.blobFromImage(cv2.resize(frameL, (300, 300)),
                        0.007843, (300, 300), 127.5)

        self.net.setInput(blob)
        detections 		= self.net.forward()
        detection_count = 0
        distances = []

        frameL = cv2.remap(frameL, self.leftMapX, self.leftMapY, cv2.INTER_LINEAR)
        frameR = cv2.remap(frameR, self.rightMapX, self.rightMapY, cv2.INTER_LINEAR)
        grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
        grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

        depth = self.stereoMatcher.compute(grayL, grayR)
        #plt.imshow(depth, 'gray')
        #plt.show()

        distance_mtx = (self.baseline * self.focal_length)/depth
        #print(distance_mtx)

        for i in numpy.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > self.confidence:
                idx = int(detections[0, 0, i, 1])
                if PeopleCount.CLASSES[idx] != PeopleCount.PERSON_CLASS:
                    continue

                detection_count += 1
                box = detections[0,0,i, 3:7] * np.array([width, height, width, height])
                startX, startY, endX, endY = box.astype('int')
                x = int((startX + endX)/2)
                y = int((startY + endY)/2)
                print(distance_mtx[y][x])
                plt.imshow(depth, 'gray')
                plt.show()


        return {PeopleCount.COUNT_KEY: detection_count}

    def find_marker(query, image):
        """
        Searches for the marker object in the image

        Parameters:
                query: picture of the object to search for, also called the query image
                image: image to search within, also called the train image

        return: list containing top left and top right coordinate of rectangle around object
        rtype: list
        """

        orb = cv2.ORB_create()

        kp_q, des_q = orb.detectAndCompute(query, None)
        kp_i, des_i = orb.detectAndCompute(image, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = bf.match(des_q, des_i)
        matches = sorted(matches, key=lambda x: x.distance)
        top_half = matches[:(int(len(matches)/2))]

        points = {}

        for match in top_half:
            idx = match.trainIdx
            points[idx] = kp_i[idx].pt

        x = 0
        y = 0
        cnt = 0

        # accumulation for center
        for pair in points.values():
            x += pair[0]
            y += pair[1]
            cnt += 1

        center = (x/cnt, y/cnt)
        top_half = sorted(top_half,
                        key=lambda x: utils.euclidean_distance(center[0], center[1], points[x.trainIdx][0], points[x.trainIdx][1]))
        good_matches = top_half[:(int(len(top_half)/2))]

        # find bounding rectangle coords
        left = bottom = sys.maxsize
        right = top = -sys.maxsize - 1
        for match in good_matches:
            idx = match.trainIdx
            pt = kp_i[idx].pt
            top = int(max(top, pt[1]))
            left = int(min(left, pt[0]))
            bottom = int(min(bottom, pt[1]))
            right = int(max(right, pt[0]))

        return [(top, left), (bottom, right)]

        # these lines left in for debugging, will be removed once distance stuff is done
        #res = cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 3)
        #res = cv2.drawMatches(query, kp_q, image, kp_i, top_half, None, flags=None)
        #plt.imshow(res), plt.show()
