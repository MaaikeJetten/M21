import tornado.web
import tornado.ioloop
import tornado.httpclient

import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import json as json
from json import loads

import uuid
import os
import time

from variables import *
from detecting import *
from ARDetection import *

# from urllib.parse import urlencode
# from urllib.request import Request, urlopen

import requests
import urllib.parse

class uploadHandler(tornado.web.RequestHandler):
    
    def post(self):
        # print(self.request);
        files = self.request.files["image"]
        # self.write(f"<html><body><p>{csrf}</p></body></html>")
        for f in files:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        print(f.filename)
        image = f.body
        np_img = np.array(image)
        results = model(f"img/{f.filename}", size = 1280)
        array = results.pred[0].cpu().numpy()
        if array.size == 0:
            os.remove(f"img/{f.filename}")
            self.write("no detection")
        else:
            detections = detect(array)
            json_det = JSONDetections(detections)
            os.remove(f"img/{f.filename}")
            self.write(json_det)     

class arHandler(tornado.web.RequestHandler):
    
    def post(self):
        files = self.request.files["image"]
        # self.write(f"<html><body><p>{csrf}</p></body></html>")
        for f in files:
            fh = open(f"img/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        print(f.filename)
        image = cv2.imread(f"img/{f.filename}")
        results = model(f"img/{f.filename}", size = 1280)
        array = results.pred[0].cpu().numpy()
        if array.size == 0:
            os.remove(f"img/{f.filename}")
            self.write("no detection")
        else:
            detections = detect(array)
            slug_det = SLUGDetections(detections, image)
            os.remove(f"img/{f.filename}")
            self.write(slug_det)


if(__name__ == "__main__"):

    app = tornado.web.Application([
        ("/", uploadHandler),
        ("/AR", arHandler),
        ("/img/(.*)", tornado.web.StaticFileHandler, {"path" : "img"})
    ])
    app.listen(8080)
    print("Listening on port 8080")
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='Model/L1280.pt')
    print("Model loaded")
    tornado.ioloop.IOLoop.instance().start()


