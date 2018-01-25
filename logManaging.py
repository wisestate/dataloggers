# -*- coding: utf-8 -*-
"""
@author: Sebastià
"""

from ftplib import FTP
from time import time
import datetime
import csv
import os


def postFTP(fileName):
    ftp = FTP()
    ftp.connect('79.156.165.213', 2121)
    ftp.login(user = 'upload', passwd = 'Nuredduna')
    try:
        ftp.cwd('logs/'+location)
    except Exception as e:
        ftp.mkd('logs/'+location)
    else:
        ftp.storbinary('STOR '+fileName, open(fileName, 'rb'))
    ftp.quit()


def startLocation():
    with open('../config.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            location = row[0]
            break

    return location

location = startLocation()
basePath = "/home/pi/dataCollecting/logManager/logs"
for fname in os.listdir(basePath)
    path = os.path.join(basePath, fname)
    try:
        postFTP(path)
    except Exception as e:
        print('An error ocurred')
    else:
        os.remove(path)