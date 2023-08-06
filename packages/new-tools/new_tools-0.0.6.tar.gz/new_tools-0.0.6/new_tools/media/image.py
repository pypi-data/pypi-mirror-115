import os
import logging
import cv2
from numpy import ndarray

IMAGE_FORMAT = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".pgm")

def check_image(image):
    """
    check_image method uses to status of check reading image .
    
    Args
    ----
    image: Image is able to string、numpy.ndarray instance.
    
    Return
    ------
    status: 
        0: image is numpy.ndarray instance.
        1: image is numpy.ndarray instance, but size is 0.
        2: image data type is None type.
    image: Numpy.ndarray instance.
    """
    
    status = None
    
    if type(image) == type(None):
        logging.warning("Image type is None !")
        status = 2
        
    elif type(image) == ndarray and image.size == 0:
        logging.warning("Image size is 0 !")
        status = 1
        
    elif type(image) == ndarray and image.size > 0:
        logging.debug("Image status is currect !")
        status = 0
        
    elif type(image) == str:
        # Check image fromat.
        if os.path.splitext(image)[-1].lower() not in IMAGE_FORMAT:
            logging.error("Image format error ! {} isn't image.".format(image))
            raise ValueError
        
        # Check image path.
        if os.path.exists(image): 
            image = cv2.imread(image)
            if type(image) == ndarray and image.size > 0:
                status = 0
            elif type(image) == ndarray and image.size == 0:
                status = 1
            else:
                status = 2
        else:
            logging.error("{} doesn't exist !".format(image))
            raise FileNotFoundError
    else:
        logging.warning("Check your image !")
        logging.debug("tools.exception.check_image.image type: {}".format(type(image)))
        raise TypeError
        
    return status, image