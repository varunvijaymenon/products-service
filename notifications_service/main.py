# import pika
# import json
# # from fastapi import FastAPI
# import os
# from dotenv import load_dotenv
# import time
# import logging
# import traceback


# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s [%(levelname)s] %(message)s',
#     handlers=[
#         logging.FileHandler("consumer.log"),
#         logging.StreamHandler()
#     ]
# )

# print('Application started')
# load_dotenv()
# # app = FastAPI()

# notifications = []
# RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
# RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "product_events")
# RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5672)

# # @app.get("/notifications/")
# # def get_notifications():
# #     return {"notifications": notifications}

# def callback(ch, method, properties, body):
#     print("Received:", body)
#     try:
#         data = json.loads(body)
#     except Exception as e:
#         print(e)
#         data = body
#     message = f"Notification: {data}"
#     notifications.append(message)
#     print(message)
#     ch.basic_ack(delivery_tag=method.delivery_tag)

# def start_consumer():
#     print(RABBITMQ_HOST,RABBITMQ_QUEUE,RABBITMQ_PORT, 'inside consumer')
#     while True:
#         try:
#             connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=int(RABBITMQ_PORT)))
#             break
#         except pika.exceptions.AMQPConnectionError:
#             print("Waiting for RabbitMQ...")
#             time.sleep(2)

#     channel = connection.channel()
#     channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
#     channel.basic_qos(prefetch_count=1)
#     channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
#     print("Notification service is waiting for messages...")
#     channel.start_consuming()

# # This line should be run in a separate script or via background task if you want non-blocking start
# # if __name__ == 'main':
# #     start_consumer()
# start_consumer()




import pika
import json
import os
import time
import logging
import traceback
from dotenv import load_dotenv

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("consumer.log"),
        logging.StreamHandler()
    ]
)

logging.info("Application started")

# Load env vars
load_dotenv()

# RabbitMQ configuration
notifications = []
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "events")
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))

def callback(ch, method, properties, body):
    logging.info(f"Received: {body}")
    try:
        data = json.loads(body)
    except Exception as e:
        logging.error("Failed to parse JSON")
        logging.error(traceback.format_exc())
        data = body

    message = f"Notification: {data}"
    notifications.append(message)
    logging.info(message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    logging.info(f"Connecting to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}, queue={RABBITMQ_QUEUE}")
    
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
            )
            logging.info("Connected to RabbitMQ")
            break
        except pika.exceptions.AMQPConnectionError as e:
            logging.warning("Waiting for RabbitMQ to be ready...")
            logging.debug(traceback.format_exc())
            time.sleep(2)

    try:
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
        logging.info("Notification service is waiting for messages...")
        channel.start_consuming()
    except Exception as e:
        logging.error("Failed to consume messages")
        logging.error(traceback.format_exc())

if __name__ == '__main__':
    start_consumer()
