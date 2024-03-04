import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(
    exchange='',
    routing_key='hello',
    body='안녕하세요. 토끼굴님.'
)

print(' [x] Sent "Hello World!"')
connection.close()