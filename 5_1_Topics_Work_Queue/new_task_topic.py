import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_workers', exchange_type='topic', durable=True)

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'
channel.basic_publish(
    exchange='topic_workers', 
    routing_key=routing_key, 
    body=message, 
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent))
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()