import json
import glob
import random
import os
import shutil
from os.path import exists

PATH = 'data_process/'
image_path = PATH + 'images/'
label_path = PATH + 'labels/'
s3ImagePath = 's3photos/'

os.mkdir(PATH)
os.mkdir(image_path)
os.mkdir(label_path)

image_train_folder = image_path+'train/' 
image_valid_folder = image_path+'valid/'
image_test_folder = image_path+'test/' 
label_train_folder = label_path+'train/' 
label_valid_folder = label_path+'valid/'
label_test_folder = label_path+'test/'

os.mkdir(image_train_folder)
os.mkdir(image_valid_folder)
os.mkdir(image_test_folder)
os.mkdir(label_train_folder)
os.mkdir(label_valid_folder)
os.mkdir(label_test_folder)


names = [
"acteren",
"alles-mag-alles-kan",
"brainstorm",
"begrijpen",
"checkpunt",
"data-analyse",
"delen",
"de-wereld-in",
"doelgroep-leren-kennen",
"doe-maar-duurzaam",
"door-de-ogen-van",
"duiveltje",
"echt-nep",
"eindpunt",
"engeltje",
"enquete",
"experts-betrekken",
"filmen",
"gebruikerstest",
"gedachten-parkeren",
"herhaal",
"hypothese",
"inspiratie-opdoen",
"je-gevoel-volgen",
"je-zintuigen-gebruiken",
"keuzes-maken",
"kwaliteitscontrole",
"literatuur-lezen",
"maken",
"mindmap",
"moodboard",
"nabespreken",
"nieuw-leven-inblazen",
"ondernemingsplan",
"onderzoeken",
"ontdekken",
"ontwerpen",
"organiseren",
"persona",
"planning",
"presenteren",
"programma-van-eisen",
"prototype",
"reflecteren",
"samen-sterk",
"samenvatten",
"scenario",
"schetsen",
"succes-bepalen",
"tentoonstellen",
"verslag",
"vertrekpunt",
"vrije-activiteit",
"waarom-vragen-stellen"]

fp = open(label_train_folder + 'classes.txt', 'w')
for name in names:
    fp.write(name + '\n')
fp.close()
shutil.copyfile(label_train_folder + 'classes.txt', label_test_folder + 'classes.txt')
shutil.copyfile(label_train_folder + 'classes.txt', label_valid_folder + 'classes.txt')


with open('data_process.json', 'r') as lbData:
    imageArray = json.load(lbData)
    imageCount = 0

    for image in imageArray:
        imageCount = imageCount + 1
        print(imageCount)
        mediaInfo = image['Media Attributes']
        labelArray = image['Label']['objects']
        if("process-fotos/2019" in image['External ID']):
            continue
        yoloString = ""
        group = image['External ID'].split('/')[0]
        if(exists(s3ImagePath + image['External ID'] + "_border.jpg")):
            borderImage = True
        else:
            borderImage = False

        for label in labelArray:
            labelInfo = label
            labelName = labelInfo['title']
            if labelName not in names:
                continue
            bbox = labelInfo['bbox']
            yoloString += str(names.index(labelName))
            if(borderImage):
                topCoordinate = (bbox['top'] + (bbox['height'] / 2) + (mediaInfo['height']/2))/(mediaInfo['height']*2)
                leftCoordinate = (bbox['left'] + (bbox['width'] / 2) + (mediaInfo['width']/2))/(mediaInfo['width']*2)
                widthCoordinate = bbox['width'] / (mediaInfo['width']*2)
                heightCoordinate = bbox['height'] / (mediaInfo['height']*2)
            else:
                topCoordinate = (bbox['top'] + (bbox['height'] / 2)) / mediaInfo['height']
                leftCoordinate = (bbox['left'] + (bbox['width'] / 2)) / mediaInfo['width']
                widthCoordinate = bbox['width'] / mediaInfo['width']
                heightCoordinate = bbox['height'] / mediaInfo['height']
            yoloString += " "
            yoloString += str(leftCoordinate)
            yoloString += " "
            yoloString += str(topCoordinate)
            yoloString += " "
            yoloString += str(widthCoordinate)
            yoloString += " "
            yoloString += str(heightCoordinate)
            yoloString += "\n"
        #Move file

        if yoloString == '':
            continue
        
        if(borderImage):
            newFilename = image['External ID'].replace('/', '_') + "_border.jpg"
        else:
            newFilename = image['External ID'].replace('/', '_')
        labelFilename = newFilename[:len(newFilename)-4] + '.txt'

        if image['Data Split'] == 'training':
            if(borderImage):
                shutil.copyfile(s3ImagePath + image['External ID'] + "_border.jpg", image_train_folder + newFilename)
            else:
                shutil.copyfile(s3ImagePath + image['External ID'], image_train_folder + newFilename)
            fp = open(label_train_folder + labelFilename, 'w')
            fp.write(yoloString)
            fp.close()
        elif image['Data Split'] == 'validation':
            if(borderImage):
                shutil.copyfile(s3ImagePath + image['External ID'] + "_border.jpg", image_valid_folder + newFilename)
            else:
                shutil.copyfile(s3ImagePath + image['External ID'], image_valid_folder + newFilename)
            fp = open(label_valid_folder + labelFilename, 'w')
            fp.write(yoloString)
            fp.close()
        elif image['Data Split'] == 'test':
            if(borderImage):
                shutil.copyfile(s3ImagePath + image['External ID'] + "_border.jpg", image_test_folder + newFilename)
            else:
                shutil.copyfile(s3ImagePath + image['External ID'], image_test_folder + newFilename)
            fp = open(label_test_folder + labelFilename, 'w')
            fp.write(yoloString)
            fp.close()
        else:
            print("Unkown data split format")