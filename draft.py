from io import BytesIO
from PIL import Image
import logging
import logzero
from logzero import logger
from picamera import PiCamera
import numpy
import datetime
from time import sleep
import random
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


# Set a logfile name
logzero.logfile(dir_path+"/data01.csv")

# Set a custom formatter
formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
logzero.formatter(formatter)

# Set up camera for 4:3 aspect ratio
cam = PiCamera()
cam.resolution = (2592,1944)

# datetime variable to store the start time
start_time = datetime.datetime.now()

# create a datetime variable to store the current time
now_time = datetime.datetime.now()

# setting photo counter for start
photo_counter = 1

# initialise binary stream which will receive image data
imageBytes = BytesIO()

# collecting data (gps data and photographs for 2 minutes)
while (now_time < start_time + datetime.timedelta(minutes=2)):
    try:
        # Capture photograph
        # cam.capture(dir_path+"/photo_"+ str(photo_counter).zfill(4)+".jpg")

        cam.capture(imageBytes, format='jpeg')
        im = Image.open(imageBytes)
        imageBrightness = numpy.mean(im)

        if imageBrightness > 20:
            logger.info("Saving photo %s", photo_counter)
            im.save(dir_path+"/photo_"+ str(photo_counter).zfill(4)+".jpg", "JPEG")
            photo_counter+=1
            sleep(5)
        else:
            logger.info("Photo rejected, waiting...")
            sleep(60)
            
        imageBytes.truncate(0)
        imageBytes.seek(0)

        # update the current time
        now_time = datetime.datetime.now()
    except Exception as e:
        logger.error("An error occurred: " + str(e))
