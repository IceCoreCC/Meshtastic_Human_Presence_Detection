import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
from websocket import create_connection
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

#  cubicle device names / names stored inside influxdb
BRUNO = "bruno"
CHARLIE = "charlie"
DIEGO = "diego"
EKKO = "ekko"

# bucket constants
BUCKET_DAILY_WORKLOAD = "daily workload"
BUCKET_VALUES = "values"
ORG = "org"

# url and authentication to access influxdb
client = InfluxDBClient(url="http://localhost:8086", token="Bk74zzmEJa_VU5_Gv4qspMc9gyR-tz8XatPRDOwt2NwLrLUqFUJax1dZT5V9Ar8OZ94qO0bAnOnh9R9Vspa_9g==", org=ORG)

# counter variable to check when to store values inside "daily workload" table
count = 0

# connect client to websocket server
ws = create_connection("ws://localhost:8080")

# InfluxDB API
write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


# This method is called when the meshtastic device recieves a message over the detection sensor.
# When called, the message is being sent to the websocket server and the values are stored inside the influxdb.
# The count variable is updated every 30 seconds. Every 30 seconds, all devices send a message telling, if a person was detected or not. 
def onReceive(packet): 
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
    

# This method is called at the end of each day.
# It calculates the average workload of each device by adding all values from the first table.
# The calculated workload is then stored in the "daily workload" table
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


# Stores a value inside the table
def storeValue(node, value):
    p = Point("occupied").field(node, value)
    write_api.write(bucket=BUCKET_VALUES, org=ORG, record=p)

# creates connection to the meshtastic device   
interface = meshtastic.serial_interface.SerialInterface()

# pub/sub subscription
pub.subscribe(onReceive, "meshtastic.receive")

# endless loop to keep listener up and keep track of daily counter
while True:
    time.sleep(2)
    if count >= 15 * 60 * 60: # hour * minutes * seconds
        count = 0
        readFromValuesAndStoreIntoDailyValueTable() 
    
