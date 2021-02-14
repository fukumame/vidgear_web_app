FROM python:3.7

RUN apt-get update -y && apt-get install -y libopencv-dev \
    && apt-get install -y ffmpeg

RUN pip3 install numpy opencv-python flask vidgear