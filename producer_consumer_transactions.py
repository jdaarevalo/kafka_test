#!/usr/bin/env python
# coding: utf-8

import os
import json
import datetime
from time import sleep

from kafka import KafkaProducer, KafkaConsumer

time = datetime.datetime.now().strftime("%Y_%m_%d__%f")
directory = "output_" + time

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

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

def producer_transactions():
    file = open("data/payments.txt")
    transactions = file.readlines()
    if len(transactions) > 0:
        kafka_producer = connect_kafka_producer()

        for transaction in transactions:
            print(transaction)
            publish_message(kafka_producer, 'payments', 'transaction', transaction)
        if kafka_producer is not None:
            kafka_producer.close()

if __name__ == '__main__':
    producer_transactions()

    consumer = KafkaConsumer("payments",
                             auto_offset_reset='earliest',
                             bootstrap_servers=['localhost:9092'],
                             fetch_max_wait_ms=10000,
                             consumer_timeout_ms=10000)

    for msg in consumer:
        response = msg.value
        try:
            transaction = json.loads(response.decode())
            os.makedirs(directory +"/"+ transaction["customer"], exist_ok=True)
            file_name = directory +"/"+ transaction["customer"] +"/"+ transaction["payment_id"] +".txt"
 
            f = open(file_name, "a")
            f.write(str(transaction)+"\n")
            f.close()
        except Exception as ex:
            print(response)
            print(response.decode())
            print('Exception while writing files')
            print(str(ex))
