from kafka import KafkaConsumer
from threading import Event
from typing import Any
import json


class StreamReader:
    def __init__(self, consumer: KafkaConsumer, event: Event) -> None:
        open("file.txt", "w").close()
        self.consumer = consumer
        self.event = event

    def get_messages(self):
        try:
            while True:
                if self.event.is_set():
                    break

                pool = self.consumer.poll(
                    timeout_ms=100,
                )

                for _, messages in pool.items():
                    self.consumer.commit_async()
                    self.iter_messages(messages)

        except Exception:
            return

    def add_line(self, txt: str):
        with open("file.txt", "a") as f:
            f.write(txt + "\n")

    def get_data_from_payload(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        data = payload.get("after") or payload.get("patch")

        if isinstance(data, str):
            try:
                data = json.loads(data)

            except json.decoder.JSONDecodeError:
                return None

        return data

    def iter_messages(self, messages: list):
        for msg in messages:
            payload = json.loads(msg.value.decode("utf-8"))

            if payload["payload"]["op"].lower() not in ["u", "c"]:
                continue

            data = self.get_data_from_payload(payload["payload"])

            if data is None:
                continue

            if (
                payload["payload"]["source"]["connector"] == "mongodb"
                and payload["payload"]["op"].lower() == "u"
            ):
                data = {
                    "data": data,
                    "filter": json.loads(payload["payload"]["filter"]),
                }

            table = payload["payload"]["source"].get(
                "table", payload["payload"]["source"].get("collection", "---")
            )

            txt = (
                f"Received message from {payload['payload']['source']['connector']}\n"
                + f"Connector: {payload['payload']['source']['name']}\n"
                + f"Table: {table}\n"
                + f"Data: {json.dumps(data)}\n"
            )

            self.add_line(txt)

            print(txt)
