## Aggregating Occupancy 2D map with MQTT communication 

### Install required pip packages
Make sure that neccessary package is install by running:
`pip install -r requirements.txt`

### Install latest Docker engine 
#### *Ubuntu*
Instruction to follow [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

#### *Windows*
Instruction to install on WSL2 [here](https://docs.docker.com/desktop/install/windows-install/) 

***Note***
To manage docker from non-root users follow instruction [here](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) 

### Procedure
The neccessary image configuration of eclipse-mosquitto docker container can be found in /mosquitto/config/

Run the following command to start the container
```console
docker-compose up -d
```

To start, execute the server application execute the `./example/server.py` script

the publisher node (to topic /occupancy/point): script `./example/mosquitto_pub.py`

the subscriber node (to topic /occupancy/map): script `example/mosquitto_sub.py`

Current implementation has four authenticated MQTT clients: *sensor1*, *sensor2*, *user* and *server*

To add more authenticated users to the MQTT channel, run the mosquitto_passwd command:
```console
mosquitto_passwd -b ./mosquitto/config/passwd <user_name> <password>
```