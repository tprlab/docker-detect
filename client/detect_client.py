import requests
import time
import json
import sys
import os
import numpy as np
import cv2 as cv
import io

URL = "http://192.168.1.243:8001"

colors = [
    (250,0,0),
    (0,0,120),
    (0,0,0),
    (0,250,0),
    (220,220,0),
    (107,142,35),
    (152,251,152),
    (70,130,180),
    (220,20,60),
    (255,0,0),
    (0,0,142),
    (0,0,70),
    (0,60,100),
    (0,80,100),
    (0,0,230),
    (119,11,32),
    (70,70,70),
    (102,102,156),
    (190,153,153),
]

def get_color(idx):
    return colors[idx % len(colors)]
 


def request_detect(f):
    try:
        params = dict (file = f)
        resp = requests.post(URL + "/detect", files=params, verify=False)
        if resp.status_code == requests.codes.ok:
            return 0, resp.json()
        return resp.status_code, resp.content
    except:
        return 503, None

def request_detect_draw(f):
    try:
        params = dict (file = f)
        resp = requests.post(URL + "/ddetect", files=params, verify=False)
        if resp.status_code == requests.codes.ok:
            return 0, resp.content
    except:
        return 503, None



def read_file(path):
    with open(path, "rb") as f:
        return f.read()

def to_memfile(content):
    memfile = io.BytesIO()
    memfile.write(content)
    memfile.seek(0)
    return memfile

def detect_file(path):
    with open(path, "rb") as f:
        return request_detect(f)

def detect_draw(path):
    with open(path, "rb") as f:
        return request_detect_draw(f)



def detect_img(img):
    _, img_encoded = cv.imencode('.jpg', img)
    return request_detect(to_memfile(img_encoded))

def detect_draw_img(img):
    _, img_encoded = cv.imencode('.jpg', img)
    return request_detect_draw(to_memfile(img_encoded))


def draw_detection(img, d, draw_text=True):
    if d is None:
        return
    n = 0
    for a in d:
        clr = get_color(n)
        cv.rectangle(img, (a["x"], a["y"]), (a["x"] + a["w"], a["y"] + a["h"]), clr, thickness=2)
        word = a["name"] + "(" + str(int(100. * a["score"])) + "%)" 
        if draw_text:
            cv.putText(img, word, (a["x"] + 5, a["y"] + 25), cv.FONT_HERSHEY_SIMPLEX, 0.5, clr, 1, cv.LINE_AA)
        n += 1



if __name__ == "__main__":
    t = time.time()    
    #err, R = detect_file(sys.argv[1])
    #img = cv.imread(sys.argv[1])
    #err, R = detect_img(img)
    err, R = detect_draw(sys.argv[1])
    t = time.time() - t

    with open("out.jpg", 'wb') as f:
        f.write(R)
    """

    if err == 0:    
        for r in R:
            print(r) 
        print("Detection done in {:.4f} seconds".format(t))
        draw_detection(img, R, True)
        cv.imwrite("out.jpg", img)
    else:
        print (err, R)
    """



 