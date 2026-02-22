from confluent_kafka import Producer
import json
from datetime import datetime
import uuid
import asyncio

TOPIC_NAME = "testBusData"

#READ COORDINATES FROM GEOJSON
def get_coordinates(n):
    input_file = open(f'./data/bus{n}.json')
    json_array = json.load(input_file)
    coordinates = json_array['features'][0]['geometry']['coordinates']
    return coordinates

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


async def generate_checkpoint(producer, coordinates, busline):
    data = {}
    data['busline'] = busline
    
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(uuid.uuid4())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        # print(message)
        producer.produce(TOPIC_NAME, key=None, value=message.encode('ascii'), callback=delivery_report)
        producer.poll(0)
        await asyncio.sleep(1)

        if i == len(coordinates)-1:
            i = 0
        else:
            i += 1

async def main():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'linger.ms': 10,
        'batch.size': 16384,
        'compression.type': 'snappy',
        'retries': 3,
        'retry.backoff.ms': 100,
        'queue.buffering.max.messages': 10
    }
    producer = Producer(conf)
    
    try:
        await asyncio.gather(
            generate_checkpoint(producer, get_coordinates(1), '00001'),
            generate_checkpoint(producer, get_coordinates(2), '00002'),
            generate_checkpoint(producer, get_coordinates(3), '00003')
        )
    finally:
        producer.flush(timeout=30)

if __name__ == "__main__":
    asyncio.run(main())
