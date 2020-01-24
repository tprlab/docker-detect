FROM python:3.7-stretch

RUN pip3 install flask
RUN pip3 install protobuf
RUN pip3 install requests
RUN pip3 install opencv_python

ADD http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz /
RUN tar -xvf /ssd_mobilenet_v1_coco_11_06_2017.tar.gz

ADD https://github.com/tprlab/docker-detect/archive/master.zip /
RUN unzip /master.zip

EXPOSE 5001

#CMD ["python3", "/docker-detect-master/detect-app/dnn_ctrl.py", "/docker-detect-master/detect-app/data/pic.jpg"]
CMD ["python3", "/docker-detect-master/detect-app/app.py"]
