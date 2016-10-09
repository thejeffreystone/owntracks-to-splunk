#!/usr/bin/python
import os
import ast
import pprint
import paho.mqtt.client as mqtt
from os.path import join, dirname
from dotenv import load_dotenv
from splunk_http_event_collector import http_event_collector

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

message = 'ON'
def on_connect(mosq, obj, rc):
    mqttc.subscribe("owntracks/#", 0)
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    global message
    topic=OwnTracks2Data(msg.topic)
    data=ast.literal_eval(msg.payload)
    data.update(topic)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)
    getTheHECInThere(data)

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def OwnTracks2Data(topic):
    # this function was taken from mqttwarn (https://github.com/jpmens/mqttwarn)
    if type(topic) == str:
        try:
            # owntracks/username/device
            parts = topic.split('/')
            username = parts[1]
            deviceid = parts[2]
        except:
            deviceid = 'unknown'
            username = 'unknown'
        return dict(username=username, device=deviceid)
    return None

def getTheHECInThere(data):
    http_event_collector_key = os.environ.get("HEC_KEY")
    http_event_collector_host = os.environ.get("HEC_HOST")
    event = http_event_collector(http_event_collector_key, http_event_collector_host)
    payload = {}
    payload.update({"index":"owntracks"})
    payload.update({"sourcetype":"owntracks"})
    payload.update({"source":"mqtt-owntracks"})
    payload.update({"host":"tightbeam"})
    payload.update({"event":data})
    event.sendEvent(payload)

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
# Connect
mqttc.username_pw_set(os.environ.get("MQTT_USER"), os.environ.get("MQTT_PASS"))
mqttc.connect(os.environ.get("MQTT_SERVER"), os.environ.get("MQTT_PORT"), 60)

# Continue the network loop
mqttc.loop_forever()
