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
    CALIBRATION_DATA = 'calibration-data'
    BLOCKSIZE = 'blocksize'
    BASELINE = 'baseline'

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

        self.height = 720 # px
        self.width = 1280 # px

        self.videoL             = cv2.VideoCapture(0)
        self.videoL.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.videoL.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)

        self.videoR             = cv2.VideoCapture(1)
        self.videoR.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.videoR.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)

        calibration_path = seer_config.configuration[PeopleCount.INI].get(PeopleCount.CALIBRATION_DATA)

        if not os.path.isfile(calibration_path):
            raise IOError(calibration_path)

        calibration = np.load(calibration_path, allow_pickle=False)
        self.calib_size = tuple(calibration['imageSize'])
        self.leftMapX = calibration['leftMapX']
        self.leftMapY = calibration['leftMapY']
        self.leftROI = tuple(calibration['leftROI'])
        self.rightMapX = calibration['rightMapX']
        self.rightMapY = calibration['rightMapY']
        self.rightROI = tuple(calibration['rightROI'])
        leftCamMtx = calibration['leftCamMtx']
        rightCamMtx = calibration['rightCamMtx']

        self.focal_length = self.calculate_focal_length(leftCamMtx, rightCamMtx)
        self.baseline = seer_config.configuration[PeopleCount.INI].get(PeopleCount.BASELINE)

        self.stereoMatcher = cv2.StereoBM_create()
        self.stereoMatcher.setBlockSize(seer_config.configuration[PeopleCount.INI].get(PeopleCount.BLOCKSIZE))

        self.initial_disparity = self.get_initial_disparity()

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

        ret, frameR = self.videoR.read()

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


        for i in numpy.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > self.confidence:
                idx = int(detections[0, 0, i, 1])
                if PeopleCount.CLASSES[idx] != PeopleCount.PERSON_CLASS:
                    continue

                detection_count += 1

                box = detections[0,0,i, 3:7] * np.array([width, height, width, height])
                startX, startY, endX, endY = box.astype('int')

                disparity = self.stereoMatcher.compute(grayL, grayR)

                closest_disp = self.get_closest(disparity, startX, startY, endX, endY)

                if closest_disp <= 0:
                    # try to see if we can get some sort of distance from the original scene
                    closest_disp = self.get_closest(self.initial_disparity, startX, startY, endX, endY)

                depth = self.baseline * self.focal_length / (closest_disp / 16.0)
                distances.append(depth)

        return {PeopleCount.COUNT_KEY: detection_count,
                PeopleCount.DISTANCES_KEY: distances}

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

    def calculate_focal_length(self, leftCamMtx, rightCamMtx):
        """
        Calculates the focal length to use. Takes the average of the left and right
        focal lengths of each camera and then returns the average of those values
        across both cameras.

        Parameters:
            leftCamMtx: left camera matrix from calibration
            rightCamMtx: right camera matrix from calibration
        
        Returns:
            focal_length: focal length to use, in pixels
        """

        fxL = leftCamMtx[0][0]
        fyL = leftCamMtx[1][1]
        fxR = rightCamMtx[0][0]
        fyR = rightCamMtx[1][1]
        
        fL = (fxL + fyL) / 2.0
        fR = (fxR + fyR) / 2.0

        return (fL + fR) / 2.0
    
    def get_closest(self, disparities, startX, endX, startY, endY):
        """
        Finds the closest positive disparity in the range specified by start/end X/Y.

        Parameters:
            distances: distance matrix from disparity map
            startX: starting x coordinate
            endX: ending x coordinate
            startY: start y coordinate
            endY: ending y coordinate

        Returns:
            disparity: closest disparity
        """

        # modify bounds to make sure theyre in the image in case of remapping issues
        startX = min(max(startX, 0), self.width - 1)
        startY = min(max(startY, 0), self.height - 1)
        endX = max(min(endX, self.width - 1), 0)
        endY = max(min(endY, self.height - 1), 0)

        disparity = disparities[startY][startX]

        for y in range(startY, endY):
            for x in range(startX, endX):
                if disparities[y][x] > disparity:
                    disparity = disparities[y][x]
        
        return disparity

    def get_initial_disparity(self):
        """
        Finds the initial disparity map of the scene before it starts looking for people.
        This helps to at least approximate gaps that might be in the image when people
        start walking through the scene.

        TODO: Remove this and find a better solution.

        Returns:
            disparity: disparity map of the scene
        """

        ret, frameL = self.videoL.read()
        ret, frameR = self.videoR.read()

        frameL = cv2.remap(frameL, self.leftMapX, self.leftMapY, cv2.INTER_LINEAR)
        frameR = cv2.remap(frameR, self.rightMapX, self.rightMapY, cv2.INTER_LINEAR)
        grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)
        grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)

        return self.stereoMatcher.compute(grayL, grayR)
