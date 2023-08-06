import json
from typing import Any

from holour.msg import *


class JsonEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Status):
            return obj.__dict__
        elif isinstance(obj, Vector3):
            return obj.__dict__
        elif isinstance(obj, Pose):
            return obj.__dict__
        elif isinstance(obj, Poses):
            return obj.__dict__
        elif isinstance(obj, ForceTorque):
            return obj.__dict__
        elif isinstance(obj, Script):
            return obj.__dict__
        elif isinstance(obj, WaypointConfig):
            return obj.__dict__
        elif isinstance(obj, Operation):
            return obj.__dict__
        elif isinstance(obj, Product):
            return obj.__dict__
        elif isinstance(obj, Task):
            return obj.__dict__
        elif isinstance(obj, AddTask):
            return obj.__dict__
        elif isinstance(obj, MoveOperation):
            return obj.__dict__
        elif isinstance(obj, CompleteOperation):
            return obj.__dict__
        elif isinstance(obj, Destination):
            return obj.value
        else:
            return json.JSONEncoder.default(self, obj)


class JsonDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object, *args, **kwargs)

    @staticmethod
    def dict_to_object(obj):
        if isinstance(obj, dict):
            if '_type' in obj and obj['_type'] == 'status':
                return Status(**obj)
            if '_type' in obj and obj['_type'] == 'vector3':
                return Vector3(**obj)
            if '_type' in obj and obj['_type'] == 'pose':
                return Pose(**obj)
            if '_type' in obj and obj['_type'] == 'poses':
                return Poses(**obj)
            if '_type' in obj and obj['_type'] == 'force_torque':
                return ForceTorque(**obj)
            if '_type' in obj and obj['_type'] == 'script':
                return Script(**obj)
            if '_type' in obj and obj['_type'] == 'waypoint_config':
                return WaypointConfig(**obj)
            if '_type' in obj and obj['_type'] == 'operation':
                return Operation(**obj)
            if '_type' in obj and obj['_type'] == 'product':
                return Product(**obj)
            if '_type' in obj and obj['_type'] == 'task':
                return Task(**obj)
            if '_type' in obj and obj['_type'] == 'add_task':
                return AddTask(**obj)
            if '_type' in obj and obj['_type'] == 'move_operation':
                return MoveOperation(**obj)
            if '_type' in obj and obj['_type'] == 'complete_operation':
                return CompleteOperation(**obj)
        return obj


def json_encode(data: Any) -> str:
    return JsonEncoder().encode(data)


def json_decode(data: str) -> Any:
    return JsonDecoder().decode(data)
