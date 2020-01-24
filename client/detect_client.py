import requests
import time
import json
import sys
import os
import numpy as np

#URL = "http://192.168.1.243:5001/detect"
URL = "http://192.168.1.218:5001/detect"


def request_with_file(url, path):


def detect_file(path):
    with open(path, "rb") as f:
        params = dict (file = f)
        resp = requests.post(url, files=params, verify=False)
        if resp.status_code == requests.codes.ok:
            return True, resp.json
        return False, rsp.content


if __name__ == "__main__":
    t = time.time()    
    rc, R = detect_file("../detect-app/data/pic.jpg")
    t = time.time() - t

    if rc:    
        for r in R:
            print(r)    
        print("Detection done in {:.4f} seconds".format(t))
    else:
        print (R)



 