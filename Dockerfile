FROM python:3.7

WORKDIR /code

ADD sift.py .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# for SIFT and ORB
RUN pip install opencv-python

# for BRIEF
# RUN pip install opencv-contrib-python

# RUN pip install numpy
# RUN pip install matplotlib

CMD ["python", "./sift.py"]