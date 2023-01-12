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
white = [255,255,255]
for (dirpath, dirnames, filenames) in walk('./'):
    f.extend(filenames)
    for filename in filenames:
        if (filename == '.DS_Store' or filename == 'train.cache' or filename == 'test.cache' or filename == 'valid.cache' or dirpath == './process-fotos' or dirpath == './backgrounds' or 'border' in filename):
            continue
        if(exists(dirpath + "/" + filename + '_border.jpg')): #check if border image has already been created for this file
            number = number + 1
            print(str(number))
            continue
        img = cv2.imread(dirpath + "/" + filename)
        h, w = img.shape[:2]
        border_h = (int) (h/2)
        border_w = (int) (w/2)
        constant = cv2.copyMakeBorder(img, border_h, border_h, border_w, border_w, cv2.BORDER_CONSTANT, value=white)
        cv2.imwrite(dirpath + "/" + filename + '_border.jpg', constant)
        number = number + 1
        print(str(number) + ', ' + dirpath + "/" + filename)
        