from PIL import Image
from io import BytesIO
import numpy


filelist = ["C:/STUFF/Python_Stuff/AstroPi/0528.jpg",
"C:/STUFF/Python_Stuff/AstroPi/0811.jpg",
"C:/STUFF/Python_Stuff/AstroPi/1054.jpg",
"C:/STUFF/Python_Stuff/AstroPi/1164.jpg",
"C:/STUFF/Python_Stuff/AstroPi/1349.jpg",
"C:/STUFF/Python_Stuff/AstroPi/0044.jpg",
"C:/STUFF/Python_Stuff/AstroPi/0106.jpg"]

imageBytes = open(filelist[5], "rb")

im = Image.open(imageBytes)
imageBrightness = numpy.mean(im)

print(imageBrightness)

im.save("C:/STUFF/Python_Stuff/AstroPi/XTEST.jpg", "JPEG", exif=im.info["exif"])

#newFile = open("C:/STUFF/Python_Stuff/AstroPi/CTEST.jpg", "wb")
#newFile.write(imageBytes.read())
#newFile.close()

