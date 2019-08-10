import csv
import json

from time import sleep
from json import dumps
from kafka import KafkaProducer, KafkaConsumer

def producer_transactions():
    kafka_producer = connect_kafka_producer()

    with open('data/payments.txt') as txt_file:
       list_transactions = csv.reader(txt_file)
       for transaction in list_transactions:
           print(transaction)
           publish_message(kafka_producer, 'payments', 'transaction', str(transaction))
       if kafka_producer is not None:
           kafka_producer.close()

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

producer_transactions()

if __name__ == '__main__':
    topic_name = 'payments'

    consumer = KafkaConsumer(topic_name, auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'], consumer_timeout_ms=1000)
    for msg in consumer:
        #record = json.loads(msg.value)
        print(msg.value)
    consumer.close()
    sleep(5)
