from homework.consumer import create_consumer

if __name__ == '__main__':
    consumer_topic = "tumbling-windows-topic-processed"
    tumbling_windows_group = "tumbling-windows-group"
    create_consumer(consumer_topic, tumbling_windows_group)
