# MIT License
#
# Copyright (c) 2018 Airthings AS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# https://airthings.com

from bluepy.btle import UUID, Peripheral
from datetime import datetime
import sys
import time
import struct
import re
import requests

class Sensor:
    def __init__(self, name, uuid, format_type, unit, scale):
        self.name = name
        self.uuid = uuid
        self.format_type = format_type
        self.unit = unit
        self.scale = scale

if len(sys.argv) != 2:
    print "USAGE: read_wave.py \"MAC\"\n where MAC is the address of the Wave and on the format AA:BB:CC:DD:EE:FF"
    sys.exit(1)

if not re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", sys.argv[1].lower()):
    print "USAGE: read_wave.py \"MAC\"\n where MAC is the address of the Wave and on the format AA:BB:CC:DD:EE:FF"
    sys.exit(1)

sensors = []
sensors.append(Sensor("DateTime", UUID(0x2A08), 'HBBBBB', "\t", 0))
sensors.append(Sensor("Temperature", UUID(0x2A6E), 'h', "deg C\t", 1.0/100.0))
sensors.append(Sensor("Humidity", UUID(0x2A6F), 'H', "%\t\t", 1.0/100.0))
sensors.append(Sensor("Radon 24h avg", "b42e01aa-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))
sensors.append(Sensor("Radon long term", "b42e0a4c-ade7-11e4-89d3-123b93f75cba", 'H', "Bq/m3\t", 1.0))

# Print header row
str_header = "\t"
for s in sensors:
    str_header += s.name + "\t"
print str_header

try:

    while 1:
        try:
            p = Peripheral(sys.argv[1])
            # Get and print sensor data
            str_out = ""
            post_data = "reading,device=basement "
            for s in sensors:
                ch  = p.getCharacteristics(uuid=s.uuid)[0]
                if (ch.supportsRead()):
                    val = ch.read()
                    val = struct.unpack(s.format_type, val)
                    if s.name == "DateTime":
                        str_out += str(datetime(val[0], val[1], val[2], val[3], val[4], val[5])) + s.unit
                    else:
                        str_out += str(val[0] * s.scale) + " " + s.unit
                        if post_data ==  "reading,device=basement ":
                            post_data += s.name.replace(" ", "\ ") + '=' + str(val[0] * s.scale)
                        else:
                            post_data += ',' + s.name.replace(" ", "\ ") + '=' + str(val[0] * s.scale)
            # print str_out
            # print post_data
            r = requests.post('http://192.168.1.40:8086/write?db=AirThingsWave', data = post_data)
            print(r)
            p.disconnect()
            time.sleep(15)

        except:
            time.sleep(5)

        finally:
            p.disconnect()

finally:
    p.disconnect()
