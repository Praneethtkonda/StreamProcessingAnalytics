import json
import paho.mqtt.client as mqtt
import requests
import random
import time

city = ['Bangalore', 'Chennai', 'Mumbai', 'Delhi', 'Hyderabad']
api_key = "4256b3de394a56a86ee35e43af6f5c2e"
mqtt_broker_address="localhost"
mqtt_broker_port = 1883
mqtt_topic = "truck_details_mqtt"

def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)

def generate_data_and_publish(mqtt_client):
    for x in range(0, len(city)):
        obj = {}
        curr_city = city[x]
        
        data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={curr_city}&units=metric&APPID={api_key}"
        )
        obj['VehicleId'] = data.json().get('sys')['id']
        obj['City'] = curr_city
        obj['Longitute'] = round(data.json().get('coord')['lon'] + random.random() / 100, 4)
        obj['Latitude']  = round(data.json().get('coord')['lat'] + random.random() / 100, 4)
            
        obj['Temperature'] = data.json().get('main')['temp']
        obj['Humidity'] = data.json().get('main')['humidity']
        obj['Speed'] = random.randrange(0, 150, 5)
    
        print(json.dumps(obj))
        mqtt_client.publish(mqtt_topic, json.dumps(obj)) 

if __name__=="__main__":
    print("The cities are: ", city)
    print("Creating new client instance")
    client = mqtt.Client("mqtt_client_data_gen_python_tss") # create new instance
    client.on_message = on_message # attach function to callback
    print("Connecting to broker")
    client.connect(mqtt_broker_address, mqtt_broker_port, 60) #connect to broker
    client.loop_start()
    print("Subscribing to topic", mqtt_topic)
    client.subscribe(mqtt_topic)
    print("Publishing messages into topic", mqtt_topic)
    
    while True:
        generate_data_and_publish(client)
        time.sleep(5)

