from refdatatypes.refbase import RefBase


class Reffloat(RefBase):
    def __init__(self, value_: float):
        super().__init__()
        self.value = value_

    @property
    def value(self) -> float:
        return self._value[0]

    @value.setter
    def value(self, value_: float):
        self._value[0] = float(value_)

    def __str__(self) -> str:
        return str(self.value)
