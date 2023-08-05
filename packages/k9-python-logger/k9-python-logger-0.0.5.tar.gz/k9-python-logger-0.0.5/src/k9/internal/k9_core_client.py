import logging
from dataclasses import dataclass
from json import JSONDecodeError
from os import environ

import requests


@dataclass
class K9CoreResponse:
    id: str
    message: str
    app_name: str
    correlation_id: str
    span_id: str
    log_level: str
    
@dataclass
class K9CoreError():
    payload: dict
    status_code: int
    message: dict


class K9Core:
    host: str

    def __init__(self):
        self.host = f"{environ.get('K9_CORE_HOST')}/api/v1"

    def sendRequest(self, message: dict):
        r = requests.post(f"{self.host}/log", json=message)
        if r.ok:
            try:
                result = r.json()
                return K9CoreResponse(**result.data)
            except JSONDecodeError | AttributeError:
                logging.error("Invalid payload: ", r.text)
                return K9CoreError(message=message,status_code=r.status_code,payload=message)
           


if __name__ == "__main__":
    print(K9Core().sendRequest(dict(teste1="", teste2=123)))
