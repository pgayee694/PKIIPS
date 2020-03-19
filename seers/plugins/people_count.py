import seer_plugin
import seer_config
import cv2
import imutils
import imutils.video
import numpy
import os.path


class PeopleCount(seer_plugin.DataCollectorPlugin):
    """
    Data collector plugin that gathers video feed
    and uses models to determine the count of people
    in the video stream.
    """

    BACKGROUND_CLASS = "background"
    AEROPLANE_CLASS = "aeroplane"
    BICYCLE_CLASS = "bicycle"
    BIRD_CLASS = "bird"
    BOAT_CLASS = "boat"
    BOTTLE_CLASS = "bottle"
    BUS_CLASS = "bus"
    CAR_CLASS = "car"
    CAT_CLASS = "cat"
    CHAIR_CLASS = "chair"
    COW_CLASS = "cow"
    DININGTABLE_CLASS = "diningtable"
    DOG_CLASS = "dog"
    HORSE_CLASS = "horse"
    MOTORBIKE_CLASS = "motorbike"
    PERSON_CLASS = "person"
    POTTEDPLANT_CLASS = "pottedplant"
    SHEEP_CLASS = "sheep"
    SOFA_CLASS = "sofa"
    TRAIN_CLASS = "train"
    TVMONITOR_CLASS = "tvmonitor"

    CLASSES = \
        [
            BACKGROUND_CLASS,
            AEROPLANE_CLASS,
            BICYCLE_CLASS,
            BIRD_CLASS,
            BOAT_CLASS,
            BOTTLE_CLASS,
            BUS_CLASS,
            CAR_CLASS,
            CAT_CLASS,
            CHAIR_CLASS,
            COW_CLASS,
            DININGTABLE_CLASS,
            DOG_CLASS,
            HORSE_CLASS,
            MOTORBIKE_CLASS,
            PERSON_CLASS,
            POTTEDPLANT_CLASS,
            SHEEP_CLASS,
            SOFA_CLASS,
            TRAIN_CLASS,
            TVMONITOR_CLASS,
        ]

    INI = 'people-count'
    CONFIDENCE_INI = 'confidence'
    MODEL_INI = 'model-path'
    PROTOTXT_INI = 'prototxt-path'

    DEFAULT_CONFIDENCE = 0.2
    COUNT_KEY = 'count'

    STREAM_TYPE_INI = 'stream-type'
    DEFAULT_STREAM_TYPE = 'camera'
    FILE_STREAM_PATH_INI = 'file-stream-path'

    def init(self):
        """
        Gets configuration for confidence and model paths.
        Sets up the network and video stream.
        """
        self.confidence = seer_config.configuration[PeopleCount.INI].getfloat(
            PeopleCount.CONFIDENCE_INI, fallback=PeopleCount.DEFAULT_CONFIDENCE)
        self.model = seer_config.configuration[PeopleCount.INI].get(
            PeopleCount.MODEL_INI)
        self.prototxt = seer_config.configuration[PeopleCount.INI].get(
            PeopleCount.PROTOTXT_INI)
        self.streamType = seer_config.configuration[PeopleCount.INI].get(
            PeopleCount.STREAM_TYPE_INI, fallback=PeopleCount.DEFAULT_STREAM_TYPE)

        if not os.path.isfile(self.model):
            raise IOError(self.model)
        if not os.path.isfile(self.prototxt):
            raise IOError(self.prototxt)

        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

        if self.streamType == PeopleCount.DEFAULT_STREAM_TYPE:
            self.video = imutils.video.VideoStream().start()
        else:
            self.video = imutils.video.FileVideoStream(
                seer_config.configuration[PeopleCount.INI].get(
                    PeopleCount.FILE_STREAM_PATH_INI)
            ).start()

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
        frame = self.video.read()
        frame = imutils.resize(frame, width=400)

        height, width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        self.net.setInput(blob)
        detections = self.net.forward()
        detection_count = 0

        for i in numpy.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > self.confidence:
                idx = int(detections[0, 0, i, 1])
                if PeopleCount.CLASSES[idx] != PeopleCount.PERSON_CLASS:
                    continue
                detection_count += 1

        return {PeopleCount.COUNT_KEY: detection_count}
