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
import sys
import pprint
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pyModbusTCP.client import ModbusClient as ModbusIPClient

#Reads Value via Modbus RTU
def readValue(id, reg):
    rr = client.read_input_registers(address=int(reg), count = 1, unit=int(id))
    #print(rr.registers)
    return rr.registers[0]

#Reads Value via Modbus RTU 
def readValueIP(address, port, addr, reg):
    c = ModbusIPClient()
    c.host(address)
    c.port(int(port))
    value = -1
    if not c.is_open():
        if not c.open():
            print("Unable to connect to "+address+":"+str(port))
    if c.is_open():
        try:
            value = c.read_holding_registers(int(addr), int(reg))
        except Exception as e:
            raise e
        finally:
            c.close()
    return value[0]

#Uploads files to FTP
def csvManaging(ip, user, pwd, ftpServer):
    print("Trying to upload files...")
    with open('pendingFiles.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        lines = [l for l in readCSV]
        try:
            ftp = FTP(ip)
            ftp.login(user = user, passwd = pwd)
            rownum = 0
            directory = "./csv/"
            for row in lines:
                if lines[rownum][ftpServer+2] == 'No':
                    try:
                        filename = directory + lines[rownum][0]
                        print(ftp.storbinary('STOR '+ lines[rownum][0], open(filename, 'rb')))
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



def valueManager():
    rownum = 0
    lastDevice = "Null"
    high = 0
    low = 0
    scale = 1
    linesToSkip = 0
    linesSkipped = 0
    for row in values:
        if linesSkipped < linesToSkip :
            linesSkipped += 1
            continue
        else:
            linesSkipped = 0

        device = row[0]
        deviceType = int(row[1])
        print('This device is ' +device + ' of type ' + deviceType)
        if deviceType == 0:
            writeCSV(row[0], row[3], row[5], now)
        #Sennet
        elif deviceType == 2:
            scale = row[5]
            linesToSkip = 2
            lowRow = values[rownum+1]
            low = lowRow[5]
            highRow = values[rownum+2]
            high = highRow[5]
            value = ((65536*high)+low)*10**(scale-6)
            writeCSV(row[0], row[3], value, now)
        #Dexcell
        elif deviceType == 1:
            value = row[5]/1000
            writeCSV(row[0], row[3], value, now)
        elif deviceType == 10:
            writeCSV(row[0], row[3], row[5], now)
        elif deviceType == 11
            value = row[5]/5
            writeCSV(row[0], row[3], value, now)
        else:
            writeCSV(row[0], row[3], row[5], now)






def storeFile(date):
    myFile = open('pendingFiles.csv', 'a', newline='')
    with myFile:
        writer = csv.writer(myFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow([fileName, date, 'No', 'No'])

def writeCSV(device ,typeValue ,value, now):
    #print('Gets here')
    date = now.strftime("%Y/%m/%d  %H:%M:%S")
    myFile = open("./csv/" + fileName, 'a')
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

print('\n \n Starting execution')
location = 'Waiting to read configuration'
print(location)
print("I'm located at " + startLocation())
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=1, stopbits = 1, bytesize = 8,  parity='N', baudrate= 9600)
client.connect()
pp = pprint.PrettyPrinter(indent=4)
startime = time()
values = []
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
    scale = 1
    values 
    for row in readCSV:
        if not row:
            break
        if rownum == 0:
            header = row
            location = row[0]
            ip.append(row[3])
            usr.append(row[4])
            pwd.append(row[5])
            fileName = location +'-'+ dateName + '.csv'
            print("Filename: " + fileName)
            #print(row)
        else:
            if row[0] == location:
                ip.append(row[3])
                usr.append(row[4])
                pwd.append(row[5])
                #print(row)
            else:
                #Read RTU
                if int(row[1]) < 10:
                    value = readValue(row[4], row[5])
                else:
                    value = readValueIP(row[2], row[3], row[4], row[5])
                values.append([row[0], row[1], row[4], row[5], row[6], value])
            
           
        rownum = rownum + 1

    pp.pprint(values)

valueManager()
storeFile(dateName)
rownum = 0
for i in ip:
    csvManaging(ip[rownum],usr[rownum], pwd[rownum], rownum)
    rownum = rownum + 1 
    
sys.stdout.flush()