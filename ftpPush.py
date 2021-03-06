# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:55:05 2017

@author: Sebastià
"""


from ftplib import FTP
from time import gmtime, strftime, time, sleep
import datetime
import csv
import os
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def readValue(id, reg):
    rr = client.read_input_registers(address=int(reg), count = 1, unit=int(id))
    #print(rr.registers)
    return rr.registers[0]


def csvManaging(ip, user, pwd, ftpServer):
    print("Trying to upload files...")
    with open('pendingFiles.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        lines = [l for l in readCSV]
        try:
            ftp = FTP(ip)
            ftp.login(user = user, passwd = pwd)
            rownum = 0
            for row in lines:
                if lines[rownum][ftpServer+2] == 'No':
                    try:
                        print(ftp.storbinary('STOR '+lines[rownum][0], open(lines[rownum][0], 'rb')))
                        lines[rownum][ftpServer+2] = 'Yes'
                    except Exception as e:
                        print("There was a problem uploading the file " + lines[rownum][0] + ". The error returned was:")
                        print("\n \n \n ")
                        print(e)
                        print("\n \n \n ")
                        print("I' ll try again later!")
                        rownum = -1
                        break

                if lines[rownum][ftpServer+2] != 'Deleted':
                    date = datetime.datetime.strptime(lines[rownum][1], "%Y-%m-%d-%H-%M-%S")
                    dateTwoMonths = date + datetime.timedelta(days = 60)
                    #print('Date then' + qwerty + 'Date now' +  asdf)
                    if dateTwoMonths < datetime.datetime.utcnow():
                        try:
                            print('Deleting file saved on ' + lines[rownum][1] )
                            os.remove(lines[rownum][0])
                            lines[rownum][2] = 'Deleted'
                        except Exception as e:
                            print('The file created on ' + lines[rownum][1] +' no longer exists')
                rownum  = rownum + 1
            if rownum != -1:
                print("Files uploaded correctly to server " + ip + ".")
            ftp.close()
        except Exception as e:
            print("An error ocurred connecting to the server " + ip + ". The error returned was:")
            print("\n \n \n ")
            print(e)
            print("\n \n \n ")
            print("I' ll try again later!")
        #print(lines)
        
        writer = csv.writer(open('pendingFiles.csv', 'w', newline=''))
        writer.writerows(lines)


def storeFile(date):
    myFile = open('pendingFiles.csv', 'a', newline='')
    with myFile:
        writer = csv.writer(myFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([fileName, date, 'No', 'No'])

def writeCSV(device ,typeValue ,value, now):
    #print('Gets here')
    date = now.strftime("%Y/%m/%d  %H:%M:%S")
    myFile = open(fileName, 'a')
    with myFile:
        writer = csv.writer(myFile, delimiter=';')
        writer.writerow(['UTC', date, device, int(typeValue), value])

def startLocation():
    with open('config.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            location = row[0]
            break

    return location

print('Starting execution')
location = 'Waiting to read configuration'
print(location)
print("I'm located at " + startLocation())
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1, stopbits = 1, bytesize = 8,  parity='N', baudrate= 9600)
client.connect()
while True:
    startime = time()
    print("\n")
    now = datetime.datetime.utcnow()
    dateName = now.strftime("%Y-%m-%d-%H-%M-%S")
    print("Reading values at " , dateName)
    with open('config.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        rownum = 0
        header = 0
        ip = []
        usr = []
        pwd = []

        for row in readCSV:
            if not row:
                break
            if rownum == 0:
                header = row
                location = row[0]
                ip.append(row[1])
                usr.append(row[2])
                pwd.append(row[3])
                fileName = location +'-'+ dateName + '.csv'
                print("Filename: " + fileName)
                #print(row)
            else:
                if row[0] == location:
                    ip.append(row[1])
                    usr.append(row[2])
                    pwd.append(row[3])
                    #print(row)
                else:
                    value = readValue(row[1], row[2])
                    #print(value)
                    writeCSV(row[0], row[3], value, now)
                
               
            rownum = rownum + 1
   

    storeFile(dateName)
    rownum = 0
    for i in ip:
        csvManaging(ip[rownum],usr[rownum], pwd[rownum], rownum)
        rownum = rownum + 1 
    sleep(30 - ((time()-startime)%60))

