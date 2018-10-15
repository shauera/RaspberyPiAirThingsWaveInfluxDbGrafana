FROM resin/rpi-raspbian:latest

RUN apt-get update && apt-get install libfontconfig1
RUN curl https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.3.0_armhf.deb --output grafana_5.3.0_armhf.deb && sudo dpkg -i grafana_5.3.0_armhf.deb

ENTRYPOINT service grafana-server start && tail -f /var/log/grafana/grafana.log

