import pika
from in_class import parse

# URL to scrape
source_url = "https://999.md/ro/list/transport/cars"

# Manually set the number of pages to scrape
page_limit = 2

# Scrape links from website
scraped_links = parse(source_url, page_limit)

# Establish connection to RabbitMQ server
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
rabbit_channel = rabbit_connection.channel()

# Declare task queue
rabbit_channel.queue_declare(queue='task_queue', durable=True)

# Send each link to the task queue
for link in scraped_links:
    rabbit_channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=link,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))

# Close connection to RabbitMQ server
rabbit_connection.close()
