# mqtt-email.py
Python script that pasrse emails sent by Dahua EZIP & IPC CCTV camera and send MQTT alarm.<br>
Another variant of script that it will run as a local email server it is available here: https://github.com/rapi3/mqtt-email-srv<br>
```
q: why ?
a: Because for Dahua EZIP camera don't exist until now an integration for IOT and you can't integrate in HA (untill now).

q: what it does ?
a: parse emails sent by cctv camera, search for alarm string and if found it publish MQTT message in camera topic.

q: can work for any camera ?
a: yes, you need to add string to find and it will work for any camera that can send email when it detect motion.

q: what do I need to run ?
a: You need to have your Postfix email server and MQTT server running and optional Home Assistant.
```
----
Some camera will send mesages encoded in MIME 64 format.<br>
To decode email sent by camera if it is encoded MIME Base 64 use:

https://online-free-tools.com/en/base_64_encoder_decoder

----

<b>Dahua EZIP</b> camera when detect motion send email message (encoded) in this format:
```
Alarm Event: Motion Detection Start
Alarm Input Channel: 1
Alarm Start Time(D/M/Y H:M:S): 21/12/2021 22:15:33
Alarm Device Name: EZIP08
Alarm Name: 
IP Address: 192.168.2.155
```
we need to search for first line: "Alarm Event: Motion Detection Start"<br>
encoded will be: "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24gU3RhcnQ"

<b>Dahua IPC</b> camera when detect motion send email message (encoded) in this format:
```
Alarm Event: Motion Detection
Alarm Input Channel: 1
Alarm Start Time(D/M/Y H:M:S): 23/12/2021 10:27:46
Alarm Device Name: IPC06
Alarm Name: 
IP Address: 192.168.2.164
```
we need to search for first line and part of seccond line.<br>
encoded will be: "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24NCkFsYXJtIElucHV0IENoYW5uZWw"

<b>No Name</b> camera when detect motion send email message (not encoded) in this format:
```
	This is an automatically generated e-mail from your IPC.

		EVENT TYPE: Motion Detected
		EVENT TIME: 27/12/2021 17:42:19
		IPC NAME: IPC
		CHANNEL NUMBER: 01
		IPC IP: 192.168.2.111
```
we need to search for first line: "EVENT TYPE: Motion Detected"<br>

when string it is found script will publish message <b>Alarm</b> in camera named topic: <b>IOT/cctv/XXXX</b><br>
sender-name it is taken from cctv email:
```
Return-Path: <XXXX@myhome.local
```
so you can have any nr of cameras sending messages to that email box and each camera will have his own topic.

<b>You need to add in python code your MQTT server-ip, user & password.</b><br>
Modify the script as appropriate.<br>

# Postfix

this is required for script to be executed when mailbox usercctv will receive mail:<br>

add in /etc/aliases<br>
usercctv: |/etc/postfix/script/mqtt-email.py<br>

Don't forget to: postalias /etc/aliases and afterwards reload Postfix with postfix reload<br>

<b>Advice</b><br>
<i>Use one mailbox/postfix user for all cctv camera that send email alerts because any message sent to that mailbox will be processed by this script and will not be stored/saved on Postfix.<br>
Add another user in camera SMTP setting to send cc mesages for trouble events and set filters to discard motion alarm mesages processed by script.</i><br>

If you need to install and configure Postfix on rpi you can use this excelent tutorial from Sam Hobbs<br>
https://samhobbs.co.uk/2014/03/raspberry-pi-email-server

----
## Home Assistant - optional
you need to create binary sensor motion for every camera<br>
There is no need to send message when Alarm is off because the sensor created will auto change state to off after 60s
```
# CCTV EZIP08 Alarm
- platform: mqtt
  state_topic: "IOT/cctv/ez08"
  name: "CCTV-EZ08"
  off_delay: 60
  payload_on: "Alarm"
  unique_id: 333-00000000844444444444
  device_class: motion
  ```
![Home Assistant motion sensors ](https://github.com/rapi3/mqtt-email/blob/main/Screenshot_2021-12-22_20-19-55.png)

<sub>Tags: CCTV, Dahua, MQTT, email, IOT, Tasmota</sub>
