FROM resin/rpi-raspbian:latest

RUN apt-get update
RUN curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
RUN . /etc/os-release
RUN echo "deb https://repos.influxdata.com/debian jessie stable" | tee /etc/apt/sources.list.d/influxdb.list
RUN apt-get install --force-yes apt-transport-https
RUN apt-get update
RUN apt-get install influxdb

ENTRYPOINT influxd
