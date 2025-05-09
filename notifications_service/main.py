import pika
import json
# from fastapi import FastAPI
import os
from dotenv import load_dotenv
import time

load_dotenv()
# app = FastAPI()

notifications = []
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "product_events")

# @app.get("/notifications/")
# def get_notifications():
#     return {"notifications": notifications}

def callback(ch, method, properties, body):
    data = json.loads(body)
    message = f"Notification: {data}"
    notifications.append(message)
    print(message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
            break
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ...")
            time.sleep(2)

    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    print("Notification service is waiting for messages...")
    channel.start_consuming()

# This line should be run in a separate script or via background task if you want non-blocking start
# if __name__ == 'main':
#     start_consumer()
start_consumer()
