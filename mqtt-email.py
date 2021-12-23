#!/usr/bin/python3
# add in /etc/aliases
# usercctv: |/etc/postfix/script/mqtt-email.py
# Don't forget to: postalias /etc/aliases and afterwards reload Postfix with postfix reload

import sys
import re
import paho.mqtt.publish as publish

ezip_string = "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24gU3RhcnQ"
ipc_string = "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24NCkFsYXJtIElucHV0IENoYW5uZWw"

sender = "name"

def find_sender(message):
    global sender
    sender = re.search(r"(?<=Return-Path: <).+?(?=\@)", message)
    sender = sender.group()

def parse():
    message = sys.stdin.read()

    if ezip_string in message or ipc_string in message:
        find_sender(message)
        publish.single('IOT/cctv/{}'.format(sender), "Alarm", hostname="192.168.1.133", client_id="cctv-email", auth = {'username':"mqtt-email", 'password':"your_pass"})

if __name__ == '__main__':
    parse()
