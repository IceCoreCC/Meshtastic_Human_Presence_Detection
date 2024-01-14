import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from websocket import create_connection
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

BRUNO = "bruno"
CHARLIE = "charlie"
DIEGO = "diego"
EKKO = "ekko"

BUCKET_DAILY_WORKLOAD = "daily_workload"
BUCKET_VALUES = "values"
ORG = "org"

client = InfluxDBClient(url="http://localhost:8086", token="Bk74zzmEJa_VU5_Gv4qspMc9gyR-tz8XatPRDOwt2NwLrLUqFUJax1dZT5V9Ar8OZ94qO0bAnOnh9R9Vspa_9g==", org=ORG)
count = 0
ws = create_connection("ws://localhost:8080")
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()



def onReceive(packet, interface): # called when a packet arrives
    print(f"Received: ", packet["decoded"]["payload"])
    content = str(packet["decoded"]["payload"])
    ws.send(str(packet["decoded"]["payload"]))
    value = 0
    global count
    if "detected" in content:
        value = 1
    if CHARLIE in content:
        storeValue(CHARLIE, value)
        count += 30
    if BRUNO in content:
        storeValue(BRUNO, value)
    if DIEGO in content:
        storeValue(DIEGO, value)
    if EKKO in content:
        storeValue(EKKO, value)


def readFromValuesAndStoreIntoDailyValueTable():
        query = 'from(bucket:"values")\
        |> range(start: -15h)\
        |> filter(fn:(r) => r._measurement == "occupied")'
        result = query_api.query(org=ORG, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))

        bruno = []
        charlie = []
        ekko = []
        diego = []

        for element in results:
            if BRUNO in element:
                bruno.append(element[1])
            if CHARLIE in element:
                charlie.append(element[1])
            if EKKO in element:
                ekko.append(element[1])
            if DIEGO in element:
                diego.append(element[1])


        if bruno:
            p= Point("workload").field(BRUNO, (sum(bruno)/len(bruno) * 100))
            write_api.write(bucket=BUCKET_DAILY_WORKLOAD, org=ORG, record=p)

        if charlie:
            p= Point("workload").field(CHARLIE, (sum(charlie)/len(charlie) * 100))
            write_api.write(bucket=BUCKET_DAILY_WORKLOAD, org=ORG, record=p)

        if ekko:
            p= Point("workload").field(EKKO, (sum(ekko)/len(ekko) * 100))
            write_api.write(bucket=BUCKET_DAILY_WORKLOAD, org=ORG, record=p)

        if diego:
            p= Point("workload").field(DIEGO, (sum(diego)/len(diego) * 100))
            write_api.write(bucket=BUCKET_DAILY_WORKLOAD, org=ORG, record=p)


def storeValue(node, value):
    p = Point("occupied").field(node, value)
    write_api.write(bucket=BUCKET_VALUES, org=ORG, record=p)


interface = meshtastic.serial_interface.SerialInterface()

pub.subscribe(onReceive, "meshtastic.receive")


while True:
    time.sleep(2)
    if count >= 15 * 60 * 60: # hour * minutes * seconds
        count = 0
        readFromValuesAndStoreIntoDailyValueTable()

