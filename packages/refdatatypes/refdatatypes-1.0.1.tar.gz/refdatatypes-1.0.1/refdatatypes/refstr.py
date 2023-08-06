from refdatatypes.refbase import RefBase


class RefStr(RefBase):
    def __init__(self, value_: str):
        super().__init__()
        self.value = value_

    @property
    def value(self) -> str:
        return self._value[0]

    @value.setter
    def value(self, value_: str):
        self._value[0] = str(value_)

    def __str__(self) -> str:
        return self.value
