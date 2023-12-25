from homework.consumer import create_consumer

if __name__ == '__main__':
    consumer_topic = "sliding-windows-topic-processed"
    sliding_windows_group = "sliding-windows-group"
    create_consumer(consumer_topic, sliding_windows_group)
