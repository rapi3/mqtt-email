#!/usr/bin/python3
# add in /etc/aliases
# usercctv: |/etc/postfix/script/mqtt-email.py
# Don't forget to: postalias /etc/aliases and afterwards reload Postfix with postfix reload
# add bash script to move saved emails from /tmp to user... /home/xxxxxx/Maildir/new/

import sys
import re
import os
import datetime
import paho.mqtt.publish as publish

# define here strings to search
# Alarm Event: Motion Detection Start
ezip_string = "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24gU3RhcnQ"
# Alarm Event: Motion Detection
# Alarm Input Channel
ipc_string = "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24NCkFsYXJtIElucHV0IENoYW5uZWw"
gs_string = "EVENT TYPE: Motion Detected"
# Alarm Event: Motion Detection Stop
ezip_end = "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24gU3RvcA"
# Alarm Event: Motion Detection end
ipc_end = "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24gZW5k"

sender = "name"

# find sender name from cctv email name:
def find_sender(message):
    global sender
    sender = re.search(r"(?<=Return-Path: <).+?(?=\@)", message)
    sender = sender.group()

# search in email body for camera strings defined up:    
def parse():
    message = sys.stdin.read()

    if ezip_string in message or ipc_string in message or gs_string in message:
        find_sender(message)
        publish.single('IOT/cctv/{}'.format(sender), "Alarm", hostname="your.mqtt.server.ip", client_id="mqtt-email", auth = {'username':"your_mqtt_user", 'password':"your_mqtt_pass"})
#        print('Debug: sender: ', sender)
#        print('Debug: EXECUTE MQTT !')
#        print ('Debug: Alarm start discard email')

    elif ezip_end in message or ipc_end in message:
        alarm = "end"
#        print ('Debug: Alarm end discard email')

    else:
        find_sender(message)
        strFilename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + format(sender) + ".emlcctv"
        output = open('/tmp/' + strFilename, 'w')
        output.write(str(message))
        output.close()
#        print ('Debug: Email saved in /tmp')

if __name__ == '__main__':
    parse()
