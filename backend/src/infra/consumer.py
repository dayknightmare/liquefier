from src.adapters.spi.repositories.topic_rule_repository import TopicRuleRepository
from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.application.use_cases.topic.read import TopicReadCase
from kafka import KafkaConsumer, KafkaProducer
from threading import Event


class StreamReader:
    def __init__(
        self,
        consumer: KafkaConsumer,
        producer: KafkaProducer,
        event: Event,
        topic_repository: TopicRepository,
        topic_rule_repository: TopicRuleRepository,
    ) -> None:
        self.consumer = consumer
        self.producer = producer
        self.event = event

        self.case = TopicReadCase(
            producer,
            topic_repository,
            topic_rule_repository,
        )

    def get_messages(self):
        try:
            while True:
                if self.event.is_set():
                    break

                pool = self.consumer.poll(
                    timeout_ms=100,
                )

                for topic, messages in pool.items():
                    self.consumer.commit_async()
                    self.case.handle(messages, topic.topic)

        except Exception as e:
            print(e)
            return
