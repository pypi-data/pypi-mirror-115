
class Operation:

    def __init__(self, uuid: str, product_uuid: str, pose: dict, automated: bool = False, confirm_needed: bool = False,
                 description: str = "", _type: str = ''):
        assert type(uuid) == str
        assert type(product_uuid) == str
        assert type(pose) == dict
        assert type(automated) == bool
        assert type(confirm_needed) == bool
        assert type(description) == str
        for key in ['x', 'y', 'z', 'rx', 'ry', 'rz']:
            assert key in pose, f"The following must be in pose-dict: {key}. Pose: {pose}"
            assert type(pose[key]) == float, f"{key} must be of type float instead of: {type(pose[key])}."

        self._type = 'operation'
        self.uuid = uuid
        self.product_uuid = product_uuid
        self.pose = pose
        self.automated = automated
        self.confirm_needed = confirm_needed
        self.description = description

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Operation):
            return other.uuid == self.uuid \
                   and other.product_uuid == self.product_uuid \
                   and other.pose == self.pose \
                   and other.automated == self.automated \
                   and other.confirm_needed == self.confirm_needed \
                   and other.description == self.description
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<uuid={self.uuid},product_uuid={self.product_uuid},pose={self.pose},automated={self.automated}," \
               f"confirm_needed={self.confirm_needed},description={self.description}>"
