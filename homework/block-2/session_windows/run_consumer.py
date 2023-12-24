from homework.consumer import create_consumer

if __name__ == '__main__':
    consumer_topic = "session-windows-topic-processed"
    session_windows_group = "session-windows-group"
    create_consumer(consumer_topic, session_windows_group)
