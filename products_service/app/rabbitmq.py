import os
import json
import pika
from fastapi import HTTPException

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "product_events")

def publish_event(event_type: str, product_data: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        message = {"event": event_type, "data": product_data}
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message)
        )
        print(f" [x] Sent '{event_type}' event")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RabbitMQ error: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
