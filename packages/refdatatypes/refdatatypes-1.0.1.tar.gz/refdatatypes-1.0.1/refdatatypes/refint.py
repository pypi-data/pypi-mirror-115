from refdatatypes.refbase import RefBase


class RefInt(RefBase):
    def __init__(self, value_: int):
        super().__init__()
        self.value = value_

    @property
    def value(self) -> int:
        return self._value[0]

    @value.setter
    def value(self, value_: int):
        self._value[0] = int(value_)

    def __str__(self) -> str:
        return str(self.value)
