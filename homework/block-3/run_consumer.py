from backoff_consumer import create_consumer

if __name__ == '__main__':
    consumer_topic = "backoff-topic-processed"
    session_windows_group = "backoff-group"
    create_consumer(consumer_topic, session_windows_group)
