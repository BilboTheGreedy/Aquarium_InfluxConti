#!/usr/bin/env python

import re
import sys
import time
import serial
from influxdb import InfluxDBClient
from influxdb import SeriesHelper
from datetime import datetime
current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def decodeMessage(line):
        decoded = line.decode('utf-8')
        return decoded

def sendToInflux(metric,tag,value,valuename,timestamp):

    json_body = [
        {
            "measurement": metric,
            "tags": {
                "sensor": tag
            },
            "time": timestamp,
            "fields": {
                valuename: float(value)
            }
        }
    ]

  
    host = '192.168.202.111'
    port = 8086
    user = 'aquarium'
    password = 'aquarium'
    dbname = 'aquarium'

    client = InfluxDBClient(host, port, user, password, dbname)
    client.create_database(dbname)
    client.write_points(json_body)

def decodeMessage(line):
		raw = line.decode('utf-8').split(':') #value from my probe box is delimited by ':'
		current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
		if raw[0] == 'TMP1':
			print(raw[1].strip())
			sendToInflux("probes",raw[0].strip(),raw[1].strip(),'value',current_time)
		elif raw[0] == 'PH':
			print(raw[1].strip())
			sendToInflux("probes",raw[0].strip(),raw[1].strip(),'value',current_time)
		elif raw[0] == 'EC':
			print(raw[1].strip())
			sendToInflux("probes",raw[0].strip(),raw[1].strip().split(',')[0],'EC',current_time)
			sendToInflux("probes",raw[0].strip(),raw[1].strip().split(',')[1],'TDS',current_time)
			sendToInflux("probes",raw[0].strip(),raw[1].strip().split(',')[2],'SAL',current_time)
			sendToInflux("probes",raw[0].strip(),raw[1].strip().split(',')[3],'SG',current_time)


def connect():
        global lastConnectionTry, ser
        lastConnectionTry = time.time()

        ser = serial.Serial('/dev/ttyAMC0',9600)
        read = ser.read()
        while read is not None:
                read = ser.readline()
                decodeMessage(read)
                


connect()
