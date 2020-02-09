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

M = 4

log_file = "video_mt.log"
logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


executor = ThreadPoolExecutor(max_workers = M)
Q = deque()



app = Flask(__name__)

vs = cv.VideoCapture("/home/pi/street-320-na.mp4")
#vs.set(cv.CAP_PROP_FRAME_WIDTH, 320)
#vs.set(cv.CAP_PROP_FRAME_HEIGHT, 240)

def handle_frame(frame):
    t = time.time()
    err, jpeg_d = detect.detect_draw_img(frame)
    t = time.time() - t;
    logging.debug("Detection done in {:.4f} seconds".format(t))
    return jpeg_d if err == 0 else None
       
def generate():
    global n
    while True:
        rc, frame = vs.read()
        #handle_frame(frame)
        if frame is not None:
            future = executor.submit(handle_frame, (frame.copy()))
            Q.append(future)
            #print("Added", len(Q))

        keep_polling = len(Q) > 0
        while(keep_polling):            
            top = Q[0]
            if top.done():
                outFrame = top.result()
                Q.popleft()
                #print("Done frame", n)
                #(rc, outFrame) = cv.imencode(".jpg", frame)
                if outFrame:
                    print("Frame", datetime.datetime.now())
                    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(outFrame) + b'\r\n')
                keep_polling = len(Q) > 0
            else:
                keep_polling = len(Q) >= M
                #if keep_polling:
                #    time.sleep(0.1)


@app.route("/stream")
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=False, use_reloader=False)

