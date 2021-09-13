#pip install requests
import requests
import random
import time
import json


city = ['Bangalore','Chennai','Mumbai','Delhi','Hyderabad']
print(city)

api_key = "4256b3de394a56a86ee35e43af6f5c2e"


def generate_data(t):
    for x in range(0,len(city)):
        obj = {}
        curr_city = city[x]
        
        data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={curr_city}&units=metric&APPID={api_key}"
        )
        obj['VehicleId'] = data.json().get('sys')['id']
        obj['City'] = curr_city
        
        if t == 0 :
            obj['Longitute'] = data.json().get('coord')['lon']
            obj['Latitude'] = data.json().get('coord')['lat']
        else :
            obj['Longitute'] = round(data.json().get('coord')['lon'] + random.random()/100,4)
            obj['Latitude']  = round(data.json().get('coord')['lat'] + random.random()/100,4)
            
        obj['Temperature'] = data.json().get('main')['temp']
        obj['Humidity'] = data.json().get('main')['humidity']
        obj['Speed'] = random.randrange(0, 150, 5)
    
        print(json.dumps(obj))    

def call_method():
    for t in range(0,10):
        print("t = ",t)
        generate_data(t)
        time.sleep(3)


call_method()

