from homework.consumer import create_consumer

if __name__ == '__main__':
    consumer_topic = "checkpoints-hdfs-topic-processed"
    checkpoints_local_group = "checkpoints-hdfs-group"
    create_consumer(consumer_topic, checkpoints_local_group)
