import pika
from homework import extract_info_from_page
from threading import Thread, Lock
from tinydb import TinyDB

# This list will hold the data scraped by the worker threads
scraped_data = []

# We use a lock to prevent simultaneous access to the scraped_data list
data_lock = Lock()

# We manually set the number of worker threads we want to use
thread_count = 3

# Initialize TinyDB
db = TinyDB('data.json')


# This is the function that each worker thread will run
def worker(thread_id):
    # We establish a connection to the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    # We create a channel on this connection
    channel = connection.channel()

    # We declare a queue on this channel. This is where the tasks will be published
    channel.queue_declare(queue='task_queue', durable=True)
    print(f'Worker {thread_id+1} is ready and waiting for tasks.')

    # This function handles the tasks that come from the queue
    def handle_message(ch, method, properties, body):
        print(f"Worker {thread_id+1} received URL {body}.")
        # We extract the information from the page at the given URL
        product_info = extract_info_from_page(body.decode())

        # We add the extracted information to our global list
        # We use the lock to ensure that no other thread is writing to the list at the same time
        with data_lock:
            scraped_data.append(product_info)
            db.insert(product_info)

        print(f"Worker {thread_id+1} finished processing URL {body}.")
        # We send an acknowledgement back to the RabbitMQ server
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # This loop continuously checks for new tasks in the queue
    try:
        while True:
            method_frame, _, body = channel.basic_get(queue='task_queue')

            # If there are no more tasks, we break the loop
            if body is None:
                print(f"Worker {thread_id+1} has no more tasks.")
                break

            # We handle the received task
            handle_message(channel, method_frame, None, body)
    finally:
        # We close the connection when we're done
        connection.close()


def main():
    # This list will hold our worker threads
    workers = []

    # We create and start the worker threads
    for i in range(thread_count):
        t = Thread(target=worker, args=(i,))
        workers.append(t)
        t.start()

    # We wait for all worker threads to finish
    for t in workers:
        t.join()

    print("All tasks have been completed.")


# Entry point of the script
if __name__ == "__main__":
    main()
