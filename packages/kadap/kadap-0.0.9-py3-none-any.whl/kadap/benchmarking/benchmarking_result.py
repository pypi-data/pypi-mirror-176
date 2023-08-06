import cv2
import base64
import requests
import numpy as np

class Benchmarking :
    def __init__(self) :
        self.url = "http://bigdata-car.kr:5000/APIs/detecting-model-benchmarking"

    def getResult(self, source, height=640, width=640) :
        res = requests.get(self.url + "?source" + source + "&height=" + height + "&width=" + width)

        return res.text

    def getImg_origin(self, source) :
        category = "origin"
        url = self.url + "/images/" + category
        res = requests.get(url+"?source="+source)
        
        data = base64.b64decode(res.text)
        jpg_arr = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)

        b, g, r = cv2.split(img)
        img_ = cv2.merge([r, g, b])

        return img_

    def getImg_bbox(self, source) :
        category = "bbox"
        url = self.url + "/images/" + category
        res = requests.get(url+"?source="+source)
        
        data = base64.b64decode(res.text)
        jpg_arr = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(jpg_arr, cv2.IMREAD_COLOR)

        b, g, r = cv2.split(img)
        img_ = cv2.merge([r, g, b])

        return img_    

# benchmarking = Benchmarking()
# print(benchmarking.getImg_bbox("7K1A5572-scaled.jpg"))