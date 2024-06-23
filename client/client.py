from threading import Event
from typing import Optional, Any
import paho.mqtt.client as mqtt

import json
import requests
from time import sleep


mqtt_client: Optional[mqtt.Client] = None

mqtt_connection_event = Event()

secret = -1

BASE_URL = 'http://0.0.0.0:5080/'


def send_secret_rest(secret_value: int):
    '''
    Add the logic to send this secret value to the REST server.
    We want to send a JSON structure to the endpoint `/secret_number`, using
    a POST method.
    Assuming secret_value = 50, then the request will contain the following
    body: {"value": 50}
    '''

    url = BASE_URL+"secret_number"
    payload = {"value": secret_value}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("Secret sent successfully")
    else:
        print(f"Failed to send secret: {response.status_code}, {response.text}")
    #pass


def on_mqtt_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    mqtt_connection_event.set()


def on_mqtt_message(client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage):
    '''Implement the logic to parse the received secret (we receive a json, but
    we are interested just on the value) and send this value to the REST
    server... or maybe the sending to REST should be done somewhere else...
    do you have any idea why?'''

    try:
        # Decode the message payload
        print('In json decode function')
        print(msg.payload)
        print(f"Type of msg.payload: {type(msg.payload)}")
        message = msg.payload.decode()
        # Parse the JSON message
        data = json.loads(message)
        # Extract the secret value
        secret_value = data.get('value')

        if secret_value is not None:
            print(f"Received secret value: {secret_value}")
            
        else:
            print("No 'value' found in the message")

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
    print('achaaa')
    client.connect('mqtt-broker', 1883)
    #client.connect('localhost', 1883)
    return client


def wait_for_server_ready():
    # Implement code to wait until the server is ready, it's up to you how
    # to do that. Our advice: Check the server source code and check if there
    # is anything useful that can help.
    # Hint: If you prefer, feel free to delete this method, use an external
    # tool and incorporate it in the Dockerfile
    #pass
    print('Ready mai agya')
    url = BASE_URL+"ready"  
    while True:
        try:
            response = requests.get(url)
            print('+++++++')
            print(response)
            if response.status_code == 200:
                print("Server is ready")
                break
        except requests.ConnectionError:
            print("Waiting for server to be ready...")
        sleep(3)


def main():
    global mqtt_client
    print('Client chl para')

    wait_for_server_ready()

    #mqtt client
    mqtt_client = connect_mqtt()
    mqtt_connection_event.wait()

    # At this point, we have our MQTT connection established, now we need to:
    # 1. Subscribe to the MQTT topic: secret/number
    print('before secret number')
    mqtt_client.subscribe("secret/number")

    # 2. Parse the received message and extract the secret number
    mqtt_client.on_message = on_mqtt_message(mqtt.Client,'123',mqtt.MQTTMessage)

    # 3. Send this number via REST to the server, using a POST method on the
    # resource `/secret_number`, with a JSON body like: {"value": 50}
    send_secret_rest(49)

    # 4. (Extra) Check the REST resource `/secret_correct` to ensure it was
    # properly set

    # 5. Terminate the script, only after at least a value was sent
    try:
        mqtt_client.loop_forever()  # Keep the script running to receive messages
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()


    '''try:
        mqtt_client.disconnect()
    except Exception:
        pass
    try:
        mqtt_client.loop_stop()
    except Exception:
        pass'''


if __name__ == '__main__':
    main()
