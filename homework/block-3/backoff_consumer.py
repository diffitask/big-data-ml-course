import random
from time import sleep

from kafka import KafkaConsumer

def backoff(tries, sleep_time):
    def actual_decorator(handler_function):
        def wrapper(*args, **kwargs):
            for i in range(tries):
                print(f'Backoff attempt {i}: start trying to call handler function {handler_function.__name__}')
                success = handler_function(*args, **kwargs)
                if success:
                    print(f'Backoff attempt {i}: successful handler function call')
                    break

                print(f'Backoff attempt {i}: unsuccessful handler function call')
                print('Sleeping and retrying...')
                sleep(sleep_time)

            print('Ending backoff')
            print('-' * 60)
        return wrapper
    return actual_decorator


@backoff(tries=5, sleep_time=1)
def message_handler(message) -> bool:
    # generate some random number. if num % 2 == 0 => success.
    rand_num = random.randint(0, 10)
    print(f'Message handler random num: {rand_num}')

    if rand_num % 2 == 0:
        print(f"The message '{message}' was handled")
        return True
    return False


def create_consumer(topic, group_id):
    print("Connecting to Kafka brokers")
    consumer = KafkaConsumer(topic,
                             group_id=group_id,
                             bootstrap_servers='localhost:29092',
                             auto_offset_reset='earliest',
                             enable_auto_commit=True)

    for message in consumer:
        message_handler(message)
        print(f'Consumer got a message: {message}')
