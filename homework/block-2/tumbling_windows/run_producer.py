from homework.producer import create_producer, write_data

if __name__ == '__main__':
    producer_topic = "tumbling-windows-topic"
    producer = create_producer()
    write_data(producer, producer_topic)
