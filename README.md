Testing Kafka
============


For start using kafka I create the docker-compose file, using as base a  Confluent's reposit [https://github.com/confluentinc/cp-docker-images]

## Steps to Run Test

1. Active Kafka and Zookeeper runing:
- ```docker-compose up -d ```
2. Add the topic "payment"
- ```docker-compose exec kafka kafka-topics --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 10 --topic payments```
3. Run the script
- ```python3 producer_consumer_transactions.py```

This process creates a new folder by customer name and files by transaction

## Requirements

Install kafka-python via pip
- ```pip install kafka-python```

## Usage

Start a cluster:

- ```docker-compose up ```

Destroy a cluster:

- ```docker-compose stop```

Verify that the services are up and running:

- ```docker-compose ps```

This docker-compose includes the topic "payments":

        environment:
                  KAFKA_CREATE_TOPICS: "payments:10:1:compact"

The topic ```payments``` have 10 partitions and 1 replica, and a `cleanup.policy`

If you like to create a new Kafka topic called "new_payments" with 10 partitions:
- ```docker-compose exec kafka kafka-topics --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 10 --topic new_payments```

Describe the topic created:
- ```docker-compose exec kafka kafka-topics --zookeeper zookeeper:2181 --describe --topic payments ```

Listing the Topics available in Kafka:
- ```docker-compose exec kafka kafka-topics --zookeeper zookeeper:2181 --list ```

Deleting a topic
- ```docker-compose exec kafka kafka-topics --zookeeper zookeeper:2181 --delete --topic new_payments```
