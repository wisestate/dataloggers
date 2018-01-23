from ftplib import FTP
from time import time
import datetime
import csv
import os


def postFTP(fileName):
    ftp = FTP('192.168.1.100')
    #ftp = ftplib.FTP('localcost', 'user', 'user@user.com')
    ftp.login(user = 'Sebastia', passwd = 'Password')

    ftp.storbinary('STOR '+fileName, open(fileName, 'rb'))
    # print("File List: ")

    # files = ftp.dir()


    # print(files)

    ftp.quit()



with open('pendingFiles.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    lines = [l for l in readCSV]
    #print(lines)
    rownum = 0
    for row in lines:
        #print(lines[rownum][2])
        if lines[rownum][2] != 'Deleted':
            if lines[rownum][2] == 'No':
                try:
                    postFTP(lines[rownum][0])
                    lines[rownum][2] = 'Yes'
                except Exception as e:
                    print('No connection to the server. I\' ll try again later!')
                    break
            date = datetime.datetime.strptime(lines[rownum][1], "%Y-%m-%d-%H-%M-%S")
            dateTwoMonths = date + datetime.timedelta(days = 60)
            #print('Date then' + qwerty + 'Date now' +  asdf)
            if dateTwoMonths < datetime.datetime.utcnow():
                try:
                    print('Deleting file saved on ' + lines[rownum][1])
                    os.remove(lines[rownum][0])
                    lines[rownum][2] = 'Deleted'
                except Exception as e:
                    print('File no longer exists')
        rownum  = rownum + 1

    writer = csv.writer(open('pendingFiles.csv', 'w', newline=''))
    writer.writerows(lines)
