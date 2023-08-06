class RefBase:
    def __init__(self, value_=None):
        self._value = [None]
        self._base_value_setter(value_)

    @property
    def value(self):
        return self._value[0]

    def _base_value_setter(self, value_):
        self._value[0] = value_

    def get_ref_addr(self) -> int:
        """
        Get address of value container. Still at same address.
        """
        return id(self._value)

    def get_value_addr(self) -> int:
        """
        Get address of value. Address could vary.
        """
        return id(self._value[0])

    def __str__(self) -> str:
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return bool(self.value)

    def __bytes__(self):
        return bytes(self.value)

    def __lt__(self, other):
        return self.value.__lt__(other)

    def __le__(self, other):
        return self.value.__le__(other)

    def __gt__(self, other):
        return self.value.__gt__(other)

    def __ge__(self, other):
        return self.value.__ge__(other)

    def __eq__(self, other):
        return self.value.__eq__(other)

    def __add__(self, other):
        self._base_value_setter(self.value.__add__(other))
        return self

    def __sub__(self, other):
        self._base_value_setter(self.value.__sub__(other))
        return self

    def __mul__(self, other):
        self._base_value_setter(self.value.__mul__(other))
        return self

    def __matmul__(self, other):
        self._base_value_setter(self.value.__matmul__(other))
        return self

    def __pow__(self, power, modulo=None):
        self._base_value_setter(self.value.__pow__(power, modulo))
        return self
