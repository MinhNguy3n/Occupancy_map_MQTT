#! /usr/bin/env python3
from mosquitto_sub import on_connect, on_disconnect, broker_hostname, port
import paho.mqtt.client as mqtt
import time

import matplotlib.pyplot as plt
import matplotlib.cm as cm

occupancy_data = {}
topic_sub = "/occupancy/point"
topic_pub = "/occupancy/map"
occupancy_map_updated = False

    
""" init_occupancy_matrix: Initialize the occupancy matrix (as dictionary)
        return: a 100x100 matrix of occupancy data with all values set to 0
"""
def init_occupancy_matrix():
    occupancy_matrix = [[0] * 100 for _ in range(100)] 
    for coordinates, occupancy_value in occupancy_data.items():
        x, y = coordinates
        occupancy_matrix[x][y] = occupancy_value
    return occupancy_matrix

""" print_occupancy_matrix: Print the occupancy matrix
        occupancy_matrix: the occupancy matrix to be printed
"""
def print_occupancy_matrix(occupancy_matrix):   
    for i in range(100):
        for j in range(100):
            print(occupancy_matrix[i][j], end = ' ')
        print()

""" aggregate_occupancy_point: Update the occupancy matrix with new occupancy data 
        new_occupancy_data: the new occupancy data
        return: the updated occupancy matrix
"""
def aggregate_occupancy_point(coordinates, occupancy_value):
    x,y = coordinates
    if(occupancy_data[x][y] != occupancy_value):
        occupancy_data[x][y] = occupancy_value
        return True
    else:
        return False

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
            print(f"Failed to subscribe to topic {topic_sub}")
        else:
            print(f"Subscribed to topic {topic_sub}")

""" on_message: callback function for on_message event
        client: the client instance for this callback
        userdata: the private user data as set in Client() or user_data_set()
        message: an instance of MQTTMessage. This is a class with members topic, payload, qos, retain.
"""
def on_message(client, userdata, message):
    message_payload = str(message.payload.decode('utf-8'))
    print(f"Received message {message_payload} on topic {message.topic} with QoS {message.qos}")
    
    # Publish the updated occupancy matrix
    new_occupancy_data = message.payload.decode('utf-8')
    coordinates, occupancy_value = new_occupancy_data.split(',')

    coordinates = tuple(map(int, coordinates.split(' ')))
    occupancy_value = int(occupancy_value)
    
    if (aggregate_occupancy_point(coordinates, occupancy_value)): # aggreate the occupancy point
        global occupancy_map_updated
        occupancy_map_updated = True
        print("Detect new value for Occupancy matrix")

if __name__ == '__main__':
    occupancy_data = init_occupancy_matrix()  # Initialize the occupancy matrix

    server = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"Server")
    server.username_pw_set(username="server", password="embeddedAIServer")
    server.on_connect = on_connect
    server.on_message = on_message
    server.on_disconnect = on_disconnect
    server.on_subscribe = on_subscribe
    
    plt.ion() # enable real-time plotting
    fig = plt.figure()
    mat = fig.add_subplot(121)
    mat.imshow(occupancy_data, cmap=cm.Greys) # plot the occupancy matrix as grayscale map
    plt.show()
    try:
        server.connect(broker_hostname, port)
        server.subscribe(topic_sub, qos=2)
        server.loop_start()
        while True:
            print("Server application is running...")
            if occupancy_map_updated: # publish the updated occupancy matrix to /occupancy/map
                result = server.publish(topic_pub, str(occupancy_data), qos=2)
                status = result[0]
                if status == 0:
                    print(f"Sent to topic {topic_pub} with new occupancy matrix")
                else:
                    print(f"Failed to send message to topic {topic_pub}")
                occupancy_map_updated = False
                # update the occupancy map in the GUI
                mat.imshow(occupancy_data, cmap=cm.Greys)
                
            time.sleep(1)
            plt.pause(0.1) # pause for 0.1 second

    except KeyboardInterrupt:
        print("Interrupted, disconnecting...")
        server.loop_stop()
        server.disconnect()
    finally:
        server.loop_stop()
        server.disconnect()
