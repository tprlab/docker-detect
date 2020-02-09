import logging
import cv2 as cv
import numpy as np
import dnn_ctrl as ctrl


def decode_image_data(data):
    return cv.imdecode(data, cv.IMREAD_UNCHANGED)

def detect(data):
    img = decode_image_data(data)
    if img is None:
        return False, "Empty image"
    return ctrl.detect(img)

def detect_draw(data):
    img = decode_image_data(data)
    if img is None:
        return False, "Empty image"
    rc, img = ctrl.detect_draw(img)
    if not rc:
        return rc, img
    return cv.imencode(".jpg", img)




ctrl.init()

