import json
import requests
import time
from threading import Event
from typing import Optional, Any

import paho.mqtt.client as mqtt

mqtt_client: Optional[mqtt.Client] = None

mqtt_connection_event = Event()

secret = -1

REST_SERVER_URL = 'http://0.0.0.0:5080'

def check_secret_correct(secret_value: int):
    url = f"{REST_SERVER_URL}/secret_correct"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.text
            print('Data',data)
        else:
            print(f"Failed to check secret value. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error checking secret value: {e}")


def send_secret_rest(secret_value: int):
    url = f"{REST_SERVER_URL}/secret_number"
    payload = {"value": secret_value}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Secret value sent successfully!")
            check_secret_correct(secret)
        else:
            print(f"Failed to send secret value. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending secret value: {e}")


def on_mqtt_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe("secret/number")
    mqtt_connection_event.set()


def on_mqtt_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    global secret
    try:
        payload = json.loads(msg.payload.decode())
        secret = payload.get("value")
        print("message topic=",msg.topic)
        print("message qos=",msg.qos)
        print("message retain flag=",msg.retain)
        if secret is not None:
            print('Secret: ',secret)
            send_secret_rest(secret)
    except json.JSONDecodeError:
        print("Failed to decode JSON message")
    except Exception as e:
        print(f"Error processing message: {e}")


def connect_mqtt() -> mqtt.Client:
    client = mqtt.Client(
        clean_session=True,
        protocol=mqtt.MQTTv311
    )
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message
    client.loop_start()
    client.connect('localhost', 1883)
    return client


def wait_for_server_ready():
    url = f"{REST_SERVER_URL}/ready"
    max_attempts = 100 ## any num greater than 60 because database initialization can take time from 5-60 seconds 
    attempts = 0

    while attempts < max_attempts:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("REST server is ready")
                return True
        except requests.ConnectionError:
            pass
        
        print('Waiting for server to be ready')
        attempts += 1
        time.sleep(1)

    print(f"Failed to connect to REST server after {max_attempts} attempts")
    return False


def main():
    global mqtt_client

    is_ready = wait_for_server_ready()  ## waiting for server to be ready 

    if is_ready:  ## if not ready after 5 attempts then terminate code
        mqtt_client = connect_mqtt()
        mqtt_connection_event.wait()
        time.sleep(4) 

        try:
            mqtt_client.disconnect()
        except Exception as e:
            print('Exception: ',str(e))
        try:
            mqtt_client.loop_stop()
        except Exception as e:
            print('Exception: ',str(e))
        
    else:
        print("Server is not ready, exiting.")


if __name__ == '__main__':
    main()
