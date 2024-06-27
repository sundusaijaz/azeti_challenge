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
            correct = response.text
            print('Is secret number correct? ',correct)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status code: {response.status_code}, Response: {response.text}")
    
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


def send_secret_rest(secret_value: int):
    url = f"{REST_SERVER_URL}/secret_number"
    payload = {"value": secret_value}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Secret value sent successfully!")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status code: {response.status_code}, Response: {response.text}")
    
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


def on_mqtt_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe("secret/number")
    mqtt_connection_event.set()


def on_mqtt_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    '''
    This function is only for parsing MQTT message, rest request is in main() function. 
    Reason: If we send rest request here then it will send request every sec when client receives msg from broker.
    '''
    global secret
    try:
        payload = json.loads(msg.payload.decode())
        secret = payload.get("value")

        if secret is not None:
            print('Secret value got from MQTT broker: ',secret)

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



def main():
    global mqtt_client
 
    # client will subsribe to topic at on_mqtt_connect and message will be parse on on_mqtt_message
    mqtt_client = connect_mqtt()
    mqtt_connection_event.wait()
    time.sleep(3)

    # send to rest here to avoid duplicate requests
    send_secret_rest(secret)
    
    # check if secret is correct or not
    check_secret_correct(secret)

    try:
        mqtt_client.disconnect()
    except Exception as e:
        print('Exception: ',str(e))

    try:
        mqtt_client.loop_stop()
    except Exception as e:
        print('Exception: ',str(e))
    


if __name__ == '__main__':
    main()
