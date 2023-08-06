class RefBase:
    def __init__(self):
        self._value = [None]

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
