from pydantic import BaseModel, error_wrappers
from fastapi import Request, HTTPException
from typing import Callable, Type
import json
import re


def parse_param(model: Type[BaseModel]) -> Callable:
    async def middle(request: Request) -> BaseModel:
        regex = r"(?P<col>.*)\[(?P<op>.*)\]"
        results = {}

        for i, j in request.query_params.items():
            if m := re.search(regex, i):
                results[m.group("col")] = {
                    "op": m.group("op"),
                    "value": j,
                }
                continue

        try:
            return model(**results)

        except error_wrappers.ValidationError as e:
            raise HTTPException(422, json.loads(e.json())) from e

    return middle
