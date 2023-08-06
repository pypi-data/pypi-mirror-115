from enum import Enum
from typing import Union


class AddTask:

    def __init__(self, task_uuid: str, _type: str = ''):
        self._type = 'add_task'
        self.task_uuid = task_uuid

    def __eq__(self, other: object) -> bool:
        if isinstance(other, AddTask):
            return other.task_uuid == self.task_uuid
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<task_uuid={self.task_uuid}>"


class Destination(Enum):
    Human = 'Human'
    Robot = 'Robot'

    @staticmethod
    def from_str(label: str):
        if label in ('Human', 'human'):
            return Destination.Human
        elif label in ('Robot', 'robot'):
            return Destination.Robot
        else:
            raise NotImplementedError


class MoveOperation:

    def __init__(self, operation_uuid: str, destination: Union[str, Destination], _type: str = ''):
        self._type = 'move_operation'
        self.operation_uuid = operation_uuid
        self.destination = destination if type(destination) == Destination else Destination.from_str(destination)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MoveOperation):
            return other.operation_uuid == self.operation_uuid and \
                   other.destination == self.destination
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<operation_uuid={self.operation_uuid},destination={self.destination}>"


class CompleteOperation:

    def __init__(self, operation_uuid: str, _type: str = ''):
        self._type = 'complete_operation'
        self.operation_uuid = operation_uuid

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CompleteOperation):
            return other.operation_uuid == self.operation_uuid
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<operation_uuid={self.operation_uuid}>"
