import paho.mqtt.client as mqtt #import the client1
import time

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


broker_address="localhost"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address, 1883, 60) #connect to broker
client.loop_start() #start the loop
print("Subscribing to topic","spa_mqtt_topic")
client.subscribe("spa_mqtt_topic")
print("Publishing message to topic","spa_mqtt_topic")
# client.publish("spa_mqtt_topic","OFF")
# time.sleep(10) # wait
status = "OFF"
while True:
    if status == "OFF":
        client.publish("spa_mqtt_topic", "ON")
        status = "ON"
    else:
        client.publish("spa_mqtt_topic", "OFF")
        status = "OFF"
    time.sleep(5)
client.loop_stop() #stop the loop

