from flask import Response, Flask, send_file, jsonify

import datetime
import time
import cv2 as cv
import io


from collections import deque
from concurrent.futures import ThreadPoolExecutor
import threading
import detect_client as detect
import logging

M = 5

log_file = "video_mt.log"
logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


executor = ThreadPoolExecutor(max_workers = M)
Q = deque()



app = Flask(__name__)

vs = cv.VideoCapture("path")

def handle_frame(frame, n):
    t = time.time()
    err, D = detect.detect_img(frame)
    t = time.time() - t;
    logging.debug(("Detection {} done in {:.4f} seconds".format(n, t), D))

    if err != 0:
        D = None

    return (n, frame, D)

def handle_frame_x(a):
    ret = handle_frame(a["frame"], a["n"])
    return ret

n = 0
        
def generate():
    global n
    while True:
        rc, frame = vs.read()
        if frame is not None:
            frame_copy = frame.copy()
            future = executor.submit(handle_frame_x, ({"frame" : frame_copy, "n" : n}))
            n += 1
            Q.append(future)

        keep_polling = len(Q) > 0
        while(keep_polling):            
            top = Q[0]
            if top.done():
                (n, frame, D) = top.result()
                Q.popleft()
                try:
                    if D is not None:
                        detect.draw_detection(frame, D)
                except:
                    logging.error(("Wrong d", D))

                (rc, outFrame) = cv.imencode(".jpg", frame)
                if rc:
                    print("Frame", datetime.datetime.now())
                    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(outFrame) + b'\r\n')
                keep_polling = len(Q) > 0
            else:
                keep_polling = len(Q) >= M


@app.route("/stream")
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=False, use_reloader=False)

