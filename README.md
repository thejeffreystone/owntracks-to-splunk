#Owntracks to Splunk's Http Event Collector

Version: 0.1

I decided to try and build a simple script after seeing mqttwarn (https://github.com/jpmens/mqttwarn)

This code is presented **AS IS** under MIT license.

##Description:

This python script reads [owntracks](http://owntracks.org/) data off an MQTT topic and post the events to a Splunk http event collector.

##Supported product(s):

* Splunk v6.3.X

###Requirements:

A MQTT server with Owntracks data you want to get into Splunk of course.

paho-mqtt (`pip install paho-mqtt`)

dotenv (`pip install dotenv`)

[George Starcher's Splunk-Class-httpevent](https://github.com/georgestarcher/Splunk-Class-httpevent)

###Configuration:

You will need to copy .env.sample to .env and the edit the file to match your environment.

##Notes:

I built this little script because I wanted to push Owntracks events from my MQTT server to Splunk. And while there is a modular input for MQTT, I wanted to break out the topic before I sent the data to Splunk. While this was made for a specific topic (owntracks), you could easily modify it for any MQTT topic.
