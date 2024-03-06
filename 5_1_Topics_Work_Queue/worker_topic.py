import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_workers', exchange_type='topic', durable=True)


binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

for binding_key in binding_keys:
    queue_name = binding_key
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(
        exchange='topic_workers', queue=queue_name, routing_key=binding_key)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback)
    
print(' [*] Waiting for logs. To exit press CTRL+C')

channel.start_consuming()