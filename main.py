import logging
import logzero
from logzero import logger
import ephem
from picamera import PiCamera
import datetime
from time import sleep
import numpy
import random
from io import BytesIO
from PIL import Image
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
#from pathlib import Path
#dir_path = Path(__file__).parent.resolve()


# Set a logfile name
logzero.logfile(dir_path+"/data01.csv")
#data_file = dir_path/'data01.csv'

# Set a custom formatter
formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
logzero.formatter(formatter)

# Latest TLE data for ISS location
name = "ISS (ZARYA)"
l1 = "1 25544U 98067A   21014.31054398  .00001697  00000-0  38545-4 0  9993"
l2 = "2 25544  51.6457  23.8259 0000410 224.6534 316.4858 15.49291243264748"
iss = ephem.readtle(name, l1, l2)

# Set up camera resolution
cam = PiCamera()
cam.resolution = (2592,1944)

# function to write lat/long to EXIF data for photographs
def get_latlon():    
    iss.compute() # Get the lat/long values from ephem
    long_value = [float(i) for i in str(iss.sublong).split(":")]
    if long_value[0] < 0:
        long_value[0] = abs(long_value[0])
        cam.exif_tags['GPS.GPSLongitudeRef'] = "W"
    else:
        cam.exif_tags['GPS.GPSLongitudeRef'] = "E"
    cam.exif_tags['GPS.GPSLongitude'] = '%d/1,%d/1,%d/10' % (long_value[0], long_value[1], long_value[2]*10)
    lat_value = [float(i) for i in str(iss.sublat).split(":")]
    if lat_value[0] < 0:
        lat_value[0] = abs(lat_value[0])
        cam.exif_tags['GPS.GPSLatitudeRef'] = "S"
    else:
        cam.exif_tags['GPS.GPSLatitudeRef'] = "N"
    cam.exif_tags['GPS.GPSLatitude'] = '%d/1,%d/1,%d/10' % (lat_value[0], lat_value[1], lat_value[2]*10)
    return(str(lat_value), str(long_value))

# datetime variable to store the start time
start_time = datetime.datetime.now()

# create a datetime variable to store the current time
now_time = datetime.datetime.now()

# setting photo counter for start
photo_counter = 1

# initialise binary stream which will receive image data
imageBytes = BytesIO()

# collecting data (gps data and photographs for 3 hours=179 minutes)
while (now_time < start_time + datetime.timedelta(minutes=179)):
    try:
                
        # get latitude and longitude
        lat, lon = get_latlon()
        
       
        # Capturing daytime photographs
        cam.capture(imageBytes, format='jpeg')
        im = Image.open(imageBytes)
        im.info.get('exif', b'')[:20]'Exif\x00\x00II*\x00\x08\x00\x00\x00\x0c\x00\x0f\x01\x02\x00'
        imageBrightness = numpy.mean(im)

        if imageBrightness > 20:
            logger.info("Img%s, Lat%s, Lon%s", photo_counter, lat, lon )
            im.save(dir_path+"/photo_"+ str(photo_counter).zfill(4)+".jpg", "JPEG")
            photo_counter+=1
            sleep(1.000)
        else:
            logger.info("Photo Rejected-Low Brightness, Lat%s, Lon%s", lat, lon )
            sleep(1.000)
            
        imageBytes.truncate(0)
        imageBytes.seek(0)

        
                
        # update the current time
        now_time = datetime.datetime.now()
    except Exception as e:
        logger.error("An error occurred: " + str(e))
