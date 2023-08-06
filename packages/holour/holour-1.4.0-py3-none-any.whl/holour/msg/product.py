
class Product:

    def __init__(self, uuid: str, name: str, image: str, category: str, task_uuid: str = "", tags: [str] = None,
                 description: str = "", _type: str = ''):
        assert type(uuid) == str
        assert type(name) == str
        assert type(image) == str
        assert type(category) == str
        assert type(task_uuid) == str
        assert type(tags) == list or tags is None
        assert type(description) == str

        self._type = 'product'
        self.uuid = uuid
        self.name = name
        self.image = image
        self.category = category
        self.task_uuid = task_uuid
        self.tags = tags if tags else []
        self.description = description

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Product):
            return other.uuid == self.uuid \
                   and other.name == self.name \
                   and other.image == self.image \
                   and other.category == self.category \
                   and other.task_uuid == self.task_uuid \
                   and other.tags == self.tags \
                   and other.description == self.description
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<id={self.uuid},name={self.name},image={self.image},category={self.category}" \
               f",task_uuid={self.task_uuid},tags={self.tags},description={self.description}>"
