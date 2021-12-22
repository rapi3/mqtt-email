# mqtt-email.py
Python script that read email send by Dahua EZIP cctv camera and send MQTT alarm.

q: why ?

a: Because for EZIP camera don't exist until now an integration for IOT and you can't integrate in HA (untill now)

q: what it does ?

a: read emails sent by cctv camera, search for alarm string and if found it publish MQTT message in camera topic.

q: can work for any camera ?

a: yes with minimum modification at string to find it will work for any camera that can send email when it detect motion
