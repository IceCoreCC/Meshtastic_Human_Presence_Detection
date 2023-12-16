import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from websocket import create_connection
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

client = InfluxDBClient(url="http://localhost:8086", token="Bk74zzmEJa_VU5_Gv4qspMc9gyR-tz8XatPRDOwt2NwLrLUqFUJax1dZT5V9Ar8OZ94qO0bAnOnh9R9Vspa_9g==", org="org")

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()



ws = create_connection("ws://localhost:8080")


def onReceive(packet, interface): # called when a packet arrives
    print(f"Received: ", packet["decoded"]["payload"])
    ws.send(str(packet["decoded"]["payload"]))
    

interface = meshtastic.serial_interface.SerialInterface()

pub.subscribe(onReceive, "meshtastic.receive")



while True:
    time.sleep(2)
    