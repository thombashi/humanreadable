"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""


class ParameterError(ValueError):
    """
    Exception raised if invalid parameter specified.
    """

    def __init__(self, *args, **kwargs):
        self.__value = kwargs.pop("value", None)
        self.__expected = kwargs.pop("expected", None)

        super().__init__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        item_list = [ValueError.__str__(self)]
        extra_msg_list = self._get_extra_msgs()

        if extra_msg_list:
            item_list.extend([":", ", ".join(extra_msg_list)])

        return " ".join(item_list)

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)

    def _get_extra_msgs(self):
        extra_msg_list = []

        if self.__expected:
            extra_msg_list.append(f"expected={self.__expected}")

        if self.__value:
            extra_msg_list.append(f"value={self.__value}")

        return extra_msg_list


class UnitNotFoundError(ParameterError):
    def __init__(self, *args, **kwargs):
        self.__available_units = kwargs.pop("available_units", None)

        super().__init__(*args, **kwargs)

    def _get_extra_msgs(self):
        extra_msg_list = []

        if self.__available_units:
            extra_msg_list.append(f"available-units={self.__available_units}")

        return super()._get_extra_msgs() + extra_msg_list
