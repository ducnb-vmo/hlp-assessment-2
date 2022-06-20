from decouple import config
import pickle
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

from handler import payout_handler

app = FastAPI()


@app.on_event("startup")
async def startup():
    print(config("KAFKA_TOPIC_NAME"))
    consumer = AIOKafkaConsumer(
        config("KAFKA_TOPIC_NAME"),
        bootstrap_servers=f"{config('KAFKA_HOST')}:{config('KAFKA_POST')}",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            deserialized_data = pickle.loads(msg.value)
            print(deserialized_data)
            payout_handler(deserialized_data)
    finally:
        await consumer.stop()
