from classes import *
import time

from paho.mqtt import client as mqtt_client


broker = 'dev.rightech.io'
port = 1883
topic = "base/state"
main_topic="base/controller/system"
topic_temperature = "base/controller/heater"
topic_soil_humidity = "base/controller/soil_irrigation"
topic_air_humidity ="base/controller/air_irrigation"
# generate client ID with pub prefix randomly
client_id = 'mqtt-mlg-greenhouse-mock'
username = 'mock'
password = 'mock'

sensors=Sensors(11.0,25.0,50.0)
equipment=Equipment()
controller=Controller(0)
controller.acceptCustomMode(11.0,25.0,50.0)#земля-вода

online=1
iteration=14
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"принял {msg.payload.decode()} из `{msg.topic}`")
        #print("что-то принял")
        if msg.topic == main_topic:
            if msg.payload.decode()== "1":
                print("Система запущена")
                controller.id=1
            else:
                print("Система отключена")
                controller.id=0
                equipment.changeModeHearer(0)
                equipment.changeModeBotWV(0)
                equipment.changeModeTotWV(0)
                
        if msg.topic == topic_temperature:#1
            if msg.payload.decode()== "1":
                print("включен обогрев")
                equipment.changeModeHearer(1)
            else:
                print("обогрев выключен")
                equipment.changeModeHearer(0)
 
        if msg.topic == topic_air_humidity:#1
            if msg.payload.decode()== "1":
                print("включен верхний полив")
                equipment.changeModeTotWV(1)
            else:
                print("выключен верхний полив")
                equipment.changeModeTotWV(0)

        if msg.topic == topic_soil_humidity:#0
            if msg.payload.decode()== "1":
                print("включен нижний полив")
                equipment.changeModeBotWV(1)
            else:
                print("выключен нижний полив")
                equipment.changeModeBotWV(0)
            
    client.subscribe(main_topic)
    client.on_message = on_message


def publish(client):
    iteration=14
    while True:
        time.sleep(5)
        if controller.id==1:
            #if iteration%5==0: #каждые 5 секунд контроллер отдает приказы
                
            if equipment.mode_heater==1:
                sensors.heat()
            else:
                sensors.cooling()
            
            if equipment.modeBotWV==1:
                sensors.wateringBot()
            else:
                sensors.drainageBot()
                
            if equipment.modeTopWV==1:
                sensors.wateringTop()
            else:
                sensors.drainageTop()

            msg= '{ "temperature": ' +str(sensors.getTemp()) +', "air_humidity": '+str(sensors.getAir_h())+', "soil_humidity": '+str(sensors.getSoil_h())+ ' }'

            result = client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            print(msg)
        iteration += 1


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
