import uuid as generate_uuid


class Product:

    def __init__(self, uuid: str, name: str, image: str, category: str, tags: [str] = None,
                 description: str = "", _type: str = ''):
        self._type = 'product'
        self.uuid = uuid if uuid != "" else str(generate_uuid.uuid4())
        self.name = name
        self.image = image
        self.category = category
        self.tags = tags if tags else []
        self.description = description

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Product):
            return other.uuid == self.uuid \
                   and other.name == self.name \
                   and other.image == self.image \
                   and other.category == self.category \
                   and other.tags == self.tags
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<id={self.uuid},name={self.name},image={self.image},category={self.category},tags={self.tags}>"
