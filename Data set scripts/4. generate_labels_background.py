import json
import glob
import random
import math
import os
import shutil
from os import walk
from os.path import exists

PATH = 'data_process/'
image_path = PATH + 'images/'
label_path = PATH + 'labels/'
s3ImagePath = 's3photos/'
background_path = s3ImagePath + 'backgrounds/'

# os.mkdir(PATH)
# os.mkdir(image_path)
# os.mkdir(label_path)

image_train_folder = image_path+'train/' 
image_valid_folder = image_path+'valid/'
image_test_folder = image_path+'test/' 
label_train_folder = label_path+'train/' 
label_valid_folder = label_path+'valid/'
label_test_folder = label_path+'test/'

# os.mkdir(image_train_folder)
# os.mkdir(image_valid_folder)
# os.mkdir(image_test_folder)
# os.mkdir(label_train_folder)
# os.mkdir(label_valid_folder)
# os.mkdir(label_test_folder)


for (dirpath, dirnames, filenames) in walk(background_path):
    numPhotos = len(filenames)
    numTrain = int(numPhotos * 0.8)
    numValid = int(math.ceil(numPhotos * 0.1))
    currentNum = 1
    for filename in filenames:
        labelFilename = filename[:len(filename)-4] + '.txt'
        yoloString = ""
        if(currentNum <= numTrain):
            shutil.copyfile(background_path + filename, image_train_folder + filename)
            fp = open(label_train_folder + labelFilename, 'w')
            fp.write(yoloString)
            fp.close()
        elif(currentNum > numTrain and currentNum <= numTrain + numValid):
            shutil.copyfile(background_path + filename, image_valid_folder + filename)
            fp = open(label_valid_folder + labelFilename, 'w')
            fp.write(yoloString)
            fp.close()
        else:
            shutil.copyfile(background_path + filename, image_test_folder + filename)
            fp = open(label_test_folder + labelFilename, 'w')
            fp.write(yoloString)
            fp.close()
        currentNum = currentNum + 1
