from kafka import KafkaConsumer
import json

def get_consumer():
    return KafkaConsumer(
        'post-events',
        bootstrap_servers='kafka:9092',
        group_id='stats-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest'
    )

def start_kafka_consumer():
    consumer = get_consumer()

    for message in consumer:
        event = message.value
        print(f"[Kafka] Received: {event}")
        # Тут могла бы быть вставка в ClickHouse
