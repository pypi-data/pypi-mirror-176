import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Generic, List, TypeVar

from internal.k9_core_client import K9Core
from jsonschema import Draft7Validator

logging.basicConfig(
    format='[K9-%(levelname)s] msg=%(message)s', level=logging.DEBUG)

T = TypeVar("T")


class Schema(Enum):
    STANDART = "standart"


@dataclass
class ErrorMessage:
    path: str
    value: str
    message: str


LogErrors = List[ErrorMessage]


@dataclass
class Teste:
    A: str
    B: int


@dataclass
class InfraProperties:
    k8s_cluster_name: str
    k8s_container_name: str
    k8s_container_id: str
    k8s_namespace: str
    k8s_deployment: str
    docker_id: str
    ip: str
    hostname: str
    
    # def __str__(self):
    #     return f'{self.__dict__}'


@dataclass
class LogMessage(Generic[T]):
    app_name: str
    correlation_id: str
    timestamp: datetime
    message: str
    log_level: str
    # infrastructure: InfraProperties
    # attributes: T
    
    def __str__(self):
        msg = {
            "app_name": self.app_name,
            "correlation_id": self.correlation_id,
            "timestamp": self.timestamp,
            "message": self.message,
            "log_level": self.log_level,
            "timestamp": self.timestamp.timestamp()
        }
        return f'{msg}'


class LogError:
    schema: Schema
    details = LogErrors

    def __init__(self, schema: Schema, details: LogErrors):
        self.schema = schema
        self.details = details

    def __str__(self):
        return f'[k9-log-error] schema="{self.schema}" errors={self.details}'


class K9Logger:
    schema: Draft7Validator

    # def __init__(self):
    #     with open('./log.schema.json') as jsonSchema:
    #         schema = Draft7Validator(json.load(jsonSchema))
    #         self.schema = schema

    # def __isValidMessage(self, message: str) -> bool:
    #     for err in self.schema.iter_errors(message):
    #         print("Teste: ", err)
    #     return True

    def log(self, message: LogMessage):
        # self.__isValidMessage(message)
        K9Core().sendRequest(modelTeste.__dict__)
        logging.info(message)


if __name__ == "__main__":
    attr = Teste(A="", B=432)
    infra = InfraProperties(docker_id="", hostname="", ip="", k8s_cluster_name="",
                            k8s_container_id="", k8s_container_name="", k8s_deployment="", k8s_namespace="")
    modelTeste = LogMessage[Teste](
        message="", app_name="", correlation_id="", log_level="", timestamp=datetime.utcnow())
    K9Core().sendRequest(modelTeste.__dict__)
    K9Logger().log(modelTeste)
    # K9Core().sendRequest(dict(teste1="", teste2=123))
    
# if __name__ == "__main__":
#     attr = Teste(A="", B=432)
#     infra = InfraProperties(docker_id="", hostname="", ip="", k8s_cluster_name="",
#                             k8s_container_id="", k8s_container_name="", k8s_deployment="", k8s_namespace="")
#     modelTeste = LogMessage[Teste](
#         message="", infrastructure=infra, attributes=attr, app_name="", correlation_id="", log_level="", timestamp=datetime.utcnow())

#     K9Core().sendRequest(modelTeste.__dict__)
