
class Task:

    def __init__(self, uuid: str, name: str, sub_tasks: [str], operations: [str], execute_parallel: bool = False,
                 description: str = "", _type: str = ''):
        """
        :param name: name of the task
        :param sub_tasks: list of sub-task uuid's
        :param operations: list of operation uuid's
        :param execute_parallel: whether the task can be executed in parallel (true/false)
        :param description: a description of the task
        :param uuid: UUID of the task
        """
        self._type = 'task'
        self.uuid = uuid
        self.name = name
        self.sub_tasks: [str] = sub_tasks
        self.operations: [str] = operations
        self.execute_parallel = execute_parallel
        self.description = description

        if len(sub_tasks) <= 0 and len(operations) <= 0:
            raise ValueError("A task must have a least 1 subtask or component!")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Task):
            return other.uuid == self.uuid and other.name == self.name
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<id={self.uuid},name={self.name},sub_tasks={self.sub_tasks},operations={self.operations}," \
               f"execute_parallel={self.execute_parallel},description={self.description}>"
