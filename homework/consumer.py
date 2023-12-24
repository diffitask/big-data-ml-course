from kafka import KafkaConsumer


def create_consumer(topic, group_id):
    print("Connecting to Kafka brokers")
    consumer = KafkaConsumer(topic,
                             group_id=group_id,
                             bootstrap_servers='localhost:29092',
                             auto_offset_reset='earliest',
                             enable_auto_commit=True)

    for message in consumer:
        # save to DB
        print(message)


# if __name__ == '__main__':
#     consumer_topic = "checkpoints-local-topic-processed"
#     consumer_group = "checkpoints-local-group"
#     create_consumer(consumer_topic, consumer_group)
