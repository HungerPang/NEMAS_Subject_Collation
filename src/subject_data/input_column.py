from src.enums import ColumnDataType

class InputColumn:
    def __init__(self, name, data_type, value_shape, replace_values):
        self._name = name
        self._data_type = data_type
        self._value_shape = value_shape
        self._replace_values = replace_values

    @property
    def name(self):
        return self._name

    @property
    def data_type(self):
        return self._data_type

    def matches_value_shape(self, value):
        return self._value_shape.match(value)

    def transform_column(self, data_col):
        if self._data_type == ColumnDataType.STRING:
            output_data = data_col
        elif self.data_type == ColumnDataType.NUMBER:
            output_data = []
            for val in data_col:
                rep_vals = {rep.value: rep for rep in self._replace_values}
                if val in rep_vals.keys():
                    for key, replace in rep_vals.items():
                        if val == key:
                            output_data += [replace]
                else:
                    try:
                        output_data += [float(val)]
                    except ValueError:
                        raise ValueError('The value {} in column {} cant be converted and doesnt have a replace '
                                         'value'.format(val, self._name))
        elif self.data_type == ColumnDataType.CORRECTNESS:
            output_data = []
            for val in data_col:
                rep_vals = {rep.value: rep for rep in self._replace_values}
                if val in rep_vals.keys():
                    for key, replace in rep_vals.items():
                        if val == key:
                            output_data += [replace]
                else:
                    if val == '0':
                        output_data += [False]
                    elif val == '1':
                        output_data += [True]
                    else:
                        raise ValueError('The value {} in column {} cant be converted and doesnt have a replace '
                                         'value'.format(val, self._name))
        else:
            raise ValueError('Column data type {}, for column {} is unknown'.format(self._data_type, self._name))

        return output_data