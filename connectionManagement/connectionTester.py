# -*- coding: utf-8 -*-
"""
@author: Sebastià
"""


from ftplib import FTP
from time import gmtime, strftime, time, sleep
import datetime
import csv
import os

def postFTP(fileName):
    ftp = FTP()
    ftp.connect('79.156.165.213', 2121)
    ftp.login(user = 'upload', passwd = 'Nuredduna')
     try:
        ftp.cwd('pings/')
    except Exception as e:
        ftp.mkd('pings')
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
startime = time()
print("\n")
now = datetime.datetime.utcnow()
dateName = now.strftime("%H-%M-%S %d/%m/%Y")

with open(location, "w") as text_file:
    text_file.write(date)
    
try:
    postFTP(location)
except Exception as e:
    print(e)
