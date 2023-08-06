from refdatatypes.refbase import RefBase


class RefBool(RefBase):
    def __init__(self, value_: bool):
        super().__init__()
        self.value = value_

    @property
    def value(self) -> bool:
        return self._value[0]

    @value.setter
    def value(self, value_: bool):
        self._value[0] = bool(value_)
