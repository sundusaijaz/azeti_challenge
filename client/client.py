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


def send_secret_rest(secret_value: int):
    url = f"{REST_SERVER_URL}/secret_number"
    payload = {"value": secret_value}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Secret value sent successfully!")
    else:
        print(f"Failed to send secret value. Status code: {response.status_code}, Response: {response.text}")


def on_mqtt_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe("secret/number")
    mqtt_connection_event.set()


def on_mqtt_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    global secret
    try:
        payload = json.loads(msg.payload.decode())
        secret = payload.get("value")
        if secret is not None:
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
    #client.connect('mqtt-broker', 1883)
    client.connect('localhost', 1883)
    return client


def wait_for_server_ready():
    url = f"{REST_SERVER_URL}/ready"
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("REST server is ready")
                break
        except requests.ConnectionError:
            pass
        time.sleep(1)


def main():
    global mqtt_client

    wait_for_server_ready()

    mqtt_client = connect_mqtt()
    print('CLIENT MQTT',mqtt_client)
    mqtt_connection_event.wait()

    try:
        mqtt_client.disconnect()
    except Exception:
        pass
    try:
        mqtt_client.loop_stop()
    except Exception:
        pass


if __name__ == '__main__':
    main()
