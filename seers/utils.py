import math

"""
Houses utility functions.
"""

IN_TO_CM = 2.54
PI_WIDTH = 2.22 * IN_TO_CM # 5.6388cm
PI_LENGTH = 3.37 * IN_TO_CM # 8.5598cm

def in_to_cm(inches):
    """
    Converts the input from inches to centimeters

    Parameters:
        inches(int): value to convert
    
    return: converted value, in cm
    rtype: int
    """

    return inches * IN_TO_CM

def calc_focal_length(distance, width, pixels):
    """
    Calculates the focal length based off the input
    
    Parameters:
        distance(int): distance from camera to the object
        width(int): actual width of the object
        pixels(int): width in pixels of the object

    return: focal length of the camera based off the target object
    rtype: int
    """
    return (distance * pixels) / width

def euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)