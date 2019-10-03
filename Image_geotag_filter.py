# Image Geotag filtered
# Shivam Chourey
# This file reads all the '.JPG' files in a folder and reads their geotags
# If the latitude and longitude of the image geotags are within a defined range
# then the file is copied to a subfolder "filtered" created in the current directory

import os
import glob
from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1]
    seconds = dms[2][0] / dms[2][1]

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return [degrees, minutes, seconds]

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return (lat,lon)


# Add the folder location where all the images are present (relative path) below
# If you want to avoid that, simply put this file in the same folder as images
filenames = [file for file in glob.glob("*.JPG")]
newfolder = "filtered"
os.makedirs(newfolder, exist_ok=True)

for image in filenames:
   #print(image)
   exif = get_exif(image)
   geotags = get_geotagging(exif)
   coordinates = get_coordinates(geotags)
   #print(coordinates)

   # Enter the limits of latitude
   # Degree
   minLatD = 37.0
   maxLatD = 37.0
   # Minutes
   minLatM = 11.0
   maxLatM = 11.0
   # Seconds
   minLatS = 46.0
   maxLatS = 47.0

   # Enter the limits of longitude
   # Degree
   minLonD = -80.0
   maxLonD = -80.0
   # Minutes
   minLonM = -34.0
   maxLonM = -34.0
   # Second
   minLonS = -37.0
   maxLonS = -36.0

   # Check whether the latitude and longitude are within bounds
   if coordinates[0][0] >= minLatD and coordinates[0][0] <= maxLatD and coordinates[1][0] >= minLonD and coordinates[1][0] <= maxLonD and \
      coordinates[0][1] >= minLatM and coordinates[0][1] <= maxLatM and coordinates[1][1] >= minLonM and coordinates[1][1] <= maxLonM and \
      coordinates[0][2] >= minLatS and coordinates[0][2] <= maxLatS and coordinates[1][2] >= minLonS and coordinates[1][2] <= maxLonS:
      # Get the name of destination file along with relative path
       # Uncomment following line on Linux Machine
       destination = newfolder+"/"+image
       # Uncomment following line on Windows Machine
       #destination = newfolder+"\"+image

       # print the filtered file
       print(destination)
       # copy the file to destination
       os.popen('cp '+image+" "+destination)
