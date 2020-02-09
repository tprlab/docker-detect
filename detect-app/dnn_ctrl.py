import dnn_conf
import cv2 as cv
import tf_labels
import time
import sys
import logging
import detect_draw as dd


net = None

def init():
    global net
    tf_labels.initLabels(dnn_conf.DNN_LABELS_PATH)
    t = time.time()
    net = cv.dnn.readNetFromTensorflow(dnn_conf.DNN_PATH, dnn_conf.DNN_TXT_PATH)
    dt = time.time() - t
    logging.debug("Net loaded in {:.4f} secs".format(dt))
    return net


def inference(img):
    if img is None:
        logging.error("No image")
        return False, "No image"
    if net is None:
        logging.error("No net")
        return False, "No net"
    net.setInput(cv.dnn.blobFromImage(img, 1.0/127.5, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    return True, net.forward()

def build_detection(data, thr, rows, cols):
    if data is None:
        return None
    ret = []
    for detection in data[0,0,:,:]:
        score = float(detection[2])
        if score > thr:
            left = detection[3] * cols
            top = detection[4] * rows
            right = detection[5] * cols
            bottom = detection[6] * rows
            cls = int(detection[1])
            a = {}
            a["class"] = cls
            a["name"] = tf_labels.getLabel(cls)
            a["score"] = score
            a["x"] = int(left)
            a["y"] = int(top)
            a["w"] = int(right - left)
            a["h"] = int(bottom - top)
            ret.append(a)
    return ret

def detect(img, thr = 0.3):
    rows = img.shape[0]
    cols = img.shape[1]
    t = time.time()
    rc, out = inference(img)
    t = time.time() - t
    logging.debug("Inference took {:.4f}".format(t))
    if not rc:
        return rc, out
    return True, build_detection(out, thr, rows, cols)

def detect_draw(img, thr = 0.3):
    rc, d = detect(img, thr)
    if not rc:
        return rc, d

    dd.draw_detection(img, d)
    return True, img





if __name__ == '__main__':
    t0 = time.time()    
    init()
    t = time.time()
    print("Loading took {:.4f}".format(t - t0))
    img = cv.imread(sys.argv[1])

    t0 = time.time()    
    d = detect(img)
    t = time.time()
    print (d)
    print("Detection took {:.4f}".format(t - t0))

