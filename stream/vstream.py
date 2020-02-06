from flask import Response, Flask, send_file, jsonify

import datetime
import time
import cv2 as cv
import io
import logging

import detect_client as detect

log_file = "video.log"
logging.basicConfig(filename=log_file,level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')



app = Flask(__name__)

vs = cv.VideoCapture("path")

def handle_frame(frame):
    t = time.time()
    err, D = detect.detect_img(frame)
    t = time.time() - t;
    logging.debug(("Detection done in {:.4f} seconds".format(t), D))
    if err == 0:
        detect.draw_detection(frame, D)
    return frame


        
def generate():
    while True:
        rc, frame = vs.read()
        if rc:
            handle_frame(frame)
            (rc, outFrame) = cv.imencode(".jpg", frame)
            if rc:
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(outFrame) + b'\r\n')


@app.route("/stream")
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=False, use_reloader=False)

