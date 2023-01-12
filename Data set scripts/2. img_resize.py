import PIL.Image
import PIL.ImageOps
import numpy as np
import glob
import cv2
from os import walk
from os.path import exists


f = []
sizes = []
number = 0
for (dirpath, dirnames, filenames) in walk('./'):
    f.extend(filenames)
    for filename in filenames:
        if ('border' not in filename):
            continue
        img = cv2.imread(dirpath + "/" + filename)
        height, width = img.shape[:2]
        size = ''
        if(width > height):
            if (width > 4032):
                scale = 4032/width
                scaledWidth = 4032
                scaledHeight = height * scale
                resizeImg = cv2.resize(img, (int(scaledWidth), int(scaledHeight)))
                cv2.imwrite(dirpath + "/" + filename, resizeImg)
        else:
            if(height > 4032):
                scale = 4032/height
                scaledWidth = width * scale
                scaledHeight = 4032
                resizeImg = cv2.resize(img, (int(scaledWidth), int(scaledHeight)))
                cv2.imwrite(dirpath + "/" + filename, resizeImg)
        number = number + 1
        print(str(number) + ', ' + dirpath + "/" + filename)

        