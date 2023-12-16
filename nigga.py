from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

client = InfluxDBClient(url="http://localhost:8086", token="Bk74zzmEJa_VU5_Gv4qspMc9gyR-tz8XatPRDOwt2NwLrLUqFUJax1dZT5V9Ar8OZ94qO0bAnOnh9R9Vspa_9g==", org="org")

write_api = client.write_api(write_options=SYNCHRONOUS)
query_api = client.query_api()


query = 'from(bucket:"values")\
|> range(start: -50m)\
|> filter(fn:(r) => r._measurement == "occupied")'
result = query_api.query(org='org', query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), record.get_value()))
        

bruno = []
charlie = []
ekko = []
diego = []


for element in results:
    if "Bruno" in element:
        bruno.append(element[1])
    if "Charlie" in element:
        charlie.append(element[1])
    if "Ekko" in element:
        ekko.append(element[1])
    if "Diego" in element:
        diego.append(element[1])


sum = 0
for n in bruno:
    sum += n

print("Bruno workload: ", '%.2f'%(sum/len(bruno) * 100) , "%")

p= Point("workload").field("Bruno", (sum/len(bruno) * 100))
write_api.write(bucket="daily workload", org="org", record=p)


sum = 0
for n in charlie:
    sum += n

print("Charlie workload: ", '%.2f'%(sum/len(charlie) * 100) , "%")


p= Point("workload").field("Charlie", (sum/len(charlie) * 100))
write_api.write(bucket="daily workload", org="org", record=p)


sum = 0
for n in ekko:
    sum += n

print("Ekko workload: ", '%.2f'%(sum/len(ekko) * 100) , "%")


p= Point("workload").field("Ekko", (sum/len(ekko) * 100))
write_api.write(bucket="daily workload", org="org", record=p)


sum = 0
for n in diego:
    sum += n

print("Diego workload: ", '%.2f'%(sum/len(diego) * 100) , "%")


p= Point("workload").field("Diego", (sum/len(diego) * 100))
write_api.write(bucket="daily workload", org="org", record=p)