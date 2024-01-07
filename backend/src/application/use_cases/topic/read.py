from src.adapters.spi.repositories.topic_rule_repository import TopicRuleRepository
from src.adapters.spi.repositories.topic_repository import TopicRepository
from src.dto.topic.list_dto import TopicListDTO
from src.models.topic_rule import TopicRule
from src.dto.filter import Filter
from typing import Any, Literal
from kafka import KafkaProducer
from copy import deepcopy
import importlib
import json


class TopicReadCase:
    def __init__(
        self,
        producer: KafkaProducer,
        topic_repository: TopicRepository,
        topic_rule_repository: TopicRuleRepository,
    ):
        self.topic_rule_repository = topic_rule_repository
        self.topic_repository = topic_repository
        self.producer = producer

    def get_data_from_payload(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        data = payload.get("after") or payload.get("patch")

        if isinstance(data, str):
            try:
                data = json.loads(data)

            except json.decoder.JSONDecodeError:
                return None

        return data

    def get_topic_dto(self, topic_name: str) -> TopicListDTO:
        data = TopicListDTO()
        data.filter_name = Filter[str, Literal["eql", "like"]](
            **{
                "op": "eql",
                "value": topic_name,
            }  # type: ignore
        )

        data.filter_status = Filter[int, Literal["eql"]](
            **{
                "op": "eql",
                "value": 1,
            }  # type: ignore
        )

        return data

    def get_topic_rule(self, topic_name: str) -> list[TopicRule] | None:
        dto = self.get_topic_dto(topic_name)

        topics = self.topic_repository.list(
            0,
            dto,
        )

        if len(topics) == 0:
            return None

        rules = self.topic_rule_repository.get_by_topic_id(str(topics[0].id))

        if len(rules) == 0:
            return None

        return rules

    def parse_payload(self, msg) -> tuple[dict[str, Any], dict[str, Any]] | None:
        payload = json.loads(msg.value.decode("utf-8"))

        if payload["payload"]["op"].lower() not in ["u", "c"]:
            return None

        data = self.get_data_from_payload(payload["payload"])

        if data is None:
            return None

        return payload, data

    def exec_rules(
        self,
        rules: list[TopicRule],
        data: dict[str, Any],
        payload: dict[str, Any],
    ):
        table = payload["payload"]["source"].get(
            "table", payload["payload"]["source"].get("collection", "---")
        )

        try:
            for i in rules:
                data_to_proccess = deepcopy(data)

                for j in i.transformers:
                    module = importlib.import_module("external." + j.split(".")[0])

                    data_to_proccess = module.process(
                        data=data_to_proccess,
                        table=table,
                        database=payload["payload"]["source"]["name"],
                        connector=payload["payload"]["source"]["connector"],
                        operation=payload["payload"]["op"].lower(),
                    )

                if i.extras is not None and "topic_out" in i.extras:
                    print("===> Sending...")
                    self.producer.send(
                        i.extras["topic_out"],
                        {"data": data_to_proccess},
                    )

        except Exception as e:
            print(e)
            pass

    def handle(self, messages: list, topic_name: str):
        rules = self.get_topic_rule(topic_name)
        if rules is None:
            return

        for msg in messages:
            values = self.parse_payload(msg)

            if values is None:
                continue

            payload, data = values

            if (
                payload["payload"]["source"]["connector"] == "mongodb"
                and payload["payload"]["op"].lower() == "u"
            ):
                data = {
                    "data": data,
                    "filter": json.loads(payload["payload"]["filter"]),
                }

            self.exec_rules(rules, data, payload)
