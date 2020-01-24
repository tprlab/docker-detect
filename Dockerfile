FROM python:3.7-stretch

RUN pip3 install flask
RUN pip3 install protobuf
RUN pip3 install requests

ADD https://files.pythonhosted.org/packages/d8/38/60de02a4c9013b14478a3f681a62e003c7489d207160a4d7df8705a682e7/opencv_python-4.1.2.30-cp37-cp37m-manylinux1_x86_64.whl /
RUN pip3 install /opencv_python-4.1.2.30-cp37-cp37m-manylinux1_x86_64.whl


ADD http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz /
RUN tar -xvf /ssd_mobilenet_v1_coco_11_06_2017.tar.gz

ADD https://github.com/tprlab/docker-detect/archive/master.zip /
RUN unzip /master.zip

EXPOSE 5001

#CMD ["python3", "/docker-detect-master/detect-app/dnn_ctrl.py", "/docker-detect-master/detect-app/data/pic.jpg"]
CMD ["python3", "/docker-detect-master/detect-app/app.py"]
