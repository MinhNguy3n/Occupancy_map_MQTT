#! /usr/bin/env python3
import paho.mqtt.client as mqtt
import time
from occupancy_msg import Ocuppancy

broker_hostname = "localhost"
port = 1883
topic = "/occupancy/map"
occupancy_data = {} # placeholder for occupancy data


""" on_connect: callback function for on_connect event (updated paho v.2.0)
        client: the client instance for this callback
        userdata: the private user data as set in Client() or user_data_set()
        flags: response flags sent by the broker    
        reason_code: reason code if disconnection 
        properties: the properties for connection
"""
def on_connect(client, userdata, flags, reason_code, properties):
    if flags.session_present:
        print("Session already present")
    if reason_code == 0:
        print(f"client connected to {broker_hostname} with port {port}")
    else:
        print(f"Connection failed, return code: {reason_code}") 

""" print_occupancy_matrix: Print the occupancy matrix
        occupancy_matrix: the occupancy matrix to be printed
"""
def print_occupancy_matrix(occupancy_matrix):   
    for i in range(100):
        for j in range(100):
            print(occupancy_matrix[i][j], end = ' ')
        print()

""" on_disconnect: callback function for on_disconnect event (updated paho v.2.0)
        client: the client instance for this callback
        userdata: the private user data as set in Client() or user_data_set()
        flags: response flags sent by the broker
        reason_code: reason code if disconnection 
        properties: the properties for the connection
"""
def on_disconnect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"Client disconnected")
    else:
        print("Unexpected disconnection")

""" on_subscribe: callback function for on_subscribe event 
        client: the client instance for this callback
        userdata: the private user data as set in Client() or user_data_set()
        mid: message ID of the subscribe message
        reason_codes: list of return codes for each topic
        properties: the properties for the subscription
"""
def on_subscribe(client, userdata, mid, reason_codes, properties):
    for sub_result in reason_codes:
        if sub_result >= 128:
            print(f"Failed to subscribe to topic {topic}")
        else:
            print(f"Subscribed to topic {topic}")

""" on_message: callback function for on_message event
        client: the client instance for this callback
        userdata: the private user data as set in Client() or user_data_set()
        message: an instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
"""
def on_message(client, userdata, message):
    global occupancy_data
    print(f"Received message on topic {message.topic} with QoS {message.qos}")
    message_payload = message.payload.decode('utf-8') # message_payload is a encoded string of occupancy 2D matrix 

    occupancy_data = eval(message_payload)
    # print the occupancy matrix
    # print_occupancy_matrix(occupancy_data)

if __name__ == '__main__':
    # Create a client instance that subscribe to topic /occupancy
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"User")
    client.username_pw_set(username="user", password="embeddedAIUser")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    client.connect(broker_hostname, port)
    client.subscribe(topic, qos=2)
    client.loop_start()

    try:
        i = 0
        while True:
            time.sleep(1)
            print(f"Waiting for message from topic {topic} ...")

    except KeyboardInterrupt:
        print("Interrupted, disconnecting...")
        client.loop_stop()
        client.disconnect()
            
    finally:
        client.loop_stop()
        client.disconnect()
