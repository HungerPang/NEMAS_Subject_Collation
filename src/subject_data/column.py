import re

class Column:
    def __init__(self, name, data_type, value_shape):
        self._name = name
        self._data_type = data_type
        self._value_shape = value_shape

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type

    def matches_value_shape(self, value):
        return self._value_shape.match(value)