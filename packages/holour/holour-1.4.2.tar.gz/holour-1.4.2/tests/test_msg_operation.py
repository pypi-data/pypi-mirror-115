from unittest import TestCase

from holour import json_encode, json_decode
from holour.msg import Operation


class Test(TestCase):

    def test_operation(self):
        operation = Operation('uuid_1', 'product_1', {'x': 0.0, 'y': 0.0, 'z': 0.0, 'rx': 0.0, 'ry': 0.0, 'rz': 0.0})
        operation_string = json_encode(operation)
        expected_string = '{"_type": "operation", "uuid": "uuid_1", "product_uuid": "product_1", ' \
                          '"pose": {"x": 0.0, "y": 0.0, "z": 0.0, "rx": 0.0, "ry": 0.0, "rz": 0.0}, ' \
                          '"automated": false, "confirm_needed": false, "description": ""}'

        assert type(operation_string) == str
        assert operation_string == expected_string, f"Expected {expected_string}, got: {operation_string}"

        operation_decoded = json_decode(operation_string)
        assert type(operation_decoded) == Operation, f"Got: {type(operation_decoded)}. Expected {Operation}"
        assert operation_decoded == operation, "The decoded object must be equal to the encoded"

    def test_operation_equals(self):
        op1 = Operation('uuid_1', 'product_1', {'x': 0.0, 'y': 0.0, 'z': 0.0, 'rx': 0.0, 'ry': 0.0, 'rz': 0.0})
        op2 = Operation('uuid_1', 'product_1', {'x': 0.0, 'y': 0.0, 'z': 0.0, 'rx': 0.0, 'ry': 0.0, 'rz': 0.0})
        op3 = Operation('uuid_2', 'product_1', {'x': 0.0, 'y': 0.0, 'z': 0.0, 'rx': 0.0, 'ry': 0.0, 'rz': 0.0})

        assert op1 == op2
        assert op1 != op3
        assert op1 != "not status"

    def test_operation_repr(self):
        operation = Operation('uuid_1', 'product_1', {'x': 0.0, 'y': 0.0, 'z': 0.0, 'rx': 0.0, 'ry': 0.0, 'rz': 0.0},
                              description="Hard operation")
        expected, got = 'Hard operation', f'{operation}'

        assert expected in got, f"Expected {expected} in got: {got}"

