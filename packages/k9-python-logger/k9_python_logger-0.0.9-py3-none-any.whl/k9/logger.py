import logging
from dataclasses import dataclass
from datetime import datetime
import json
from enum import Enum
from typing import Generic, List, TypeVar

from k9.internal.k9_core_client import K9Core
from jsonschema import Draft7Validator
import uuid

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
    log_level: int
    message: str
    # infrastructure: InfraProperties
    # attributes: T

    def __str__(self):
        msg = {
            "app_name": self.app_name,
            "correlation_id": self.correlation_id,
            "log_level": self.log_level,
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
    app_name: str

    def __init__(self, app_name: str):
        self.app_name = app_name

    # def __isValidMessage(self, message: str) -> bool:
    #     for err in self.schema.iter_errors(message):
    #         print("Teste: ", err)
    #     return True

    def __get_message(self, message: str, log_level: int, correlation_id: str):
        args = {
            "app_name": self.app_name,
            "correlation_id": correlation_id,
            "log_level": logging.getLevelName(log_level),
            "message": message
        }

        if args["correlation_id"] == '':
            args["correlation_id"] = str(uuid.uuid4())

        return LogMessage(**args)

    def log(self, message: str, log_level: int, correlation_id: str = ''):
        # self.__isValidMessage(message)
        msg = self.__get_message(
            message=message, correlation_id=correlation_id, log_level=log_level)
        K9Core().sendRequest(message=json.dumps(msg.__dict__))
        logging.log(level=log_level, msg=message)


if __name__ == "__main__":
    # attr = Teste(A="", B=432)
    # infra = InfraProperties(docker_id="", hostname="", ip="", k8s_cluster_name="",
    #                         k8s_container_id="", k8s_container_name="", k8s_deployment="", k8s_namespace="")
    # modelTeste = LogMessage[Teste](
    #     message="", app_name="", correlation_id="", log_level="", timestamp=datetime.utcnow().timestamp())
    # K9Core().sendRequest(modelTeste)
    K9Logger(app_name="hello-world").log(log_level=logging.INFO, message="Teste")
