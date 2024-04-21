#! /usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import random
from occupancy_msg import Ocuppancy

random.seed(time.time())
    
occupancy_data = {}
broker_hostname = "localhost"
port = 1883
topic = "/occupancy/point"

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
        print(f"Connected to {broker_hostname} with port {port}")
    else:
        print(f"Connection failed, return code: {reason_code}") 
    
""" on_disconnect: callback function for on_disconnect event (updated paho v.2.0)
        client: the client instance for this callback
        userdata: the private user data as set in Client() or user_data_set()
        flags: response flags sent by the broker
        reason_code: reason code if disconnection 
        properties: the properties for the connection
"""
def on_disconnect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Disconnected")
    else:
        print(f"Unexpected disconnection, reason code: {reason_code}")

if __name__ == '__main__':
    # Create a publishing client (updated paho v.2.0)
    client1 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"Client1")
    client1.username_pw_set(username="sensor1", password="embeddedAI1")
    client1.on_connect = on_connect
    client1.on_disconnect = on_disconnect

    ## Uncomment the following lines to enable a second client
    # client2 = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"Client2")
    # client2.username_pw_set(username="sensor2", password="embeddedAI2")
    # client2.on_connect = on_connect
    # client2.on_disconnect = on_disconnect

    try:
        client1.connect(broker_hostname, port)
        # client2.connect(broker_hostname, port)
        client1.loop_start()
        # client2.loop_start()
        while True:
            x = random.randint(0,99)
            y = random.randint(0,99)
            occupied = random.randint(0, 1)
            message = Ocuppancy(x,y,occupied)
            
            result = client1.publish(topic, payload=message.encode(), qos=2)
            status = result[0]
            if status == 0:
                print(f"Sent to topic {topic} with message {message}")
            else:
                print(f"Failed to send message to topic {topic}")

            ## Uncomment the following lines to enable client2 to publish
            # result = client2.publish(topic, payload=message.encode(), qos=2)
            # status = result[0]
            # if status == 0:
            #     print(f"Sent to topic {topic} with message {message}")
            # else:
            #     print(f"Failed to send message to topic {topic}")           

            time.sleep(0.1) # delay 0.1 second
    except KeyboardInterrupt:
        print("Keyboard Interrupted, disconnecting...")
        client1.loop_stop()
        client1.disconnect()
        # client2.loop_stop()
        # client2.disconnect()
    finally:
        client1.disconnect()
        client1.loop_stop()
        # client2.loop_stop()
        # client2.disconnect()
        print("Client disconnected")