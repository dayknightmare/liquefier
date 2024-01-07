from kafka import KafkaConsumer, KafkaProducer
from src.utils.envs import settings
from typing import Self
import json
import uuid


class StreamMeta(type):
    _instances = {}

    def __call__(cls: Self, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(StreamMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class Stream(metaclass=StreamMeta):
    def __init__(self):
        self.group_id = "liquefier-group-" + str(uuid.uuid4())
        self.__consumer = self.__create_consumer()
        self.__producer = self.__create_producer()

    def get_consumer(self) -> KafkaConsumer:
        return self.__consumer

    def get_producer(self) -> KafkaProducer:
        return self.__producer

    def __create_consumer(self) -> KafkaConsumer:
        consumer = KafkaConsumer(
            bootstrap_servers=settings.kafka_hosts.split(";"),
            group_id=self.group_id,
        )

        return consumer

    def __create_producer(self) -> KafkaProducer:
        producer = KafkaProducer(
            value_serializer=lambda m: json.dumps(m, default=str).encode("ascii"),
            bootstrap_servers=settings.kafka_hosts.split(";"),
        )

        return producer

    def close(self):
        self.__consumer.close()
