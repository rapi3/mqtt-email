# mqtt-email.py
Python script that read email send by Dahua EZIP cctv camera and send MQTT alarm.
```
q: why ?
a: Because for EZIP camera don't exist until now an integration for IOT and you can't integrate in HA (untill now)

q: what it does ?
a: read emails sent by cctv camera, search for alarm string and if found it publish MQTT message in camera topic.

q: can work for any camera ?
a: yes with minimum modification at string to find it will work for any camera that can send email when it detect motion

q: what do I need to run ?
a: You need to have your Postfix email server and MQTT server running and optional Home Assistant.
```
----
To decode email sent by camera if encoded MIM Base 64 use:

https://online-free-tools.com/en/base_64_encoder_decoder

## EZIP camera when detect motion send message in this format:

```
Alarm Event: Motion Detection Start
Alarm Input Channel: 1
Alarm Start Time(D/M/Y H:M:S): 21/12/2021 22:15:33
Alarm Device Name: EZIP06
Alarm Name: IP Address: 192.168.2.155
```
we need to search forfirst line: "Alarm Event: Motion Detection Start"<br>
encoded will be: "QWxhcm0gRXZlbnQ6IE1vdGlvbiBEZXRlY3Rpb24gU3RhcnQ"

when string it is found script will publish message <b>Alarm</b> in camera named topic: <b>IOT/cctv/ez04</b><br>
sender-name it is taken form email:
```
Return-Path: <ez04@myhome.local
```
so you can have any nr of cameras sending messages to that email box and each camera will have his own topic.

----
## Home Assistant - optional
you need to create binary sensor motion for every camera<br>
There is no need to send message when Alarm is off because the sensor created will auto change state to off after 60s
```
# CCTV EZIP04 Alarm
- platform: mqtt
  state_topic: "IOT/cctv/ez04"
  name: "CCTV-EZ04"
  off_delay: 60
  payload_on: "Alarm"
  unique_id: 333-00000000844444444444
  device_class: motion
  ```
