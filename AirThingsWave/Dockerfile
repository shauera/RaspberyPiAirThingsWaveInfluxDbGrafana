FROM resin/rpi-raspbian:stretch

RUN apt-get update
RUN apt-get install git build-essential libglib2.0-dev python-setuptools python-pip libglib2.0-dev
RUN git clone https://github.com/IanHarvey/bluepy.git /home/docker-conf
RUN cd /home/docker-conf && python setup.py build && python setup.py install
RUN curl airthings.com/tech/find_wave.py --output find_wave.py && curl airthings.com/tech/read_wave.py --output read_wave.py


