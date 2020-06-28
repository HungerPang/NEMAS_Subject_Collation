import re
from .column import Column
from src.enums import ColumnDataType

SINGLE_DIGIT = '[\d]{1}'
DOUBLE_DIGIT = '[\d]{1,2}'
TRIPLE_DIGIT = '[\d]{1,3}'


class SubjectFileTemplate():
    def __init__(self):
        self._columns = {}
        self._block_column_name = None
        self._trial_column_name = None

    def add_column(self, name=None, data_type=None, value_shape=None):
        if type(name) is str and type(data_type) is ColumnDataType:
            new_column = Column(name, data_type, value_shape)
            self._columns[name] = new_column
        elif type(name) is str:
            raise TypeError('Column data type must be set to a ColumnDataType')
        else:
            raise ValueError('Column name must be set to a string')

    def add_trial_column(self, name, value_shape):
        if type(value_shape) is not str:
            raise TypeError('Trial column value_shape must be set to a string')
        else:
            try:
                value_shape = '^' + value_shape + '$'
                self.add_column(name=name, data_type=ColumnDataType.NUMBER, value_shape=re.compile(value_shape))
                self._trial_column_name = name
            except Exception:
                raise ValueError('Trial column value shape wasnt valid regex')

    def add_block_column(self, name, value_shape):
        if type(value_shape) is not str:
            raise TypeError('Block column value_shape must be set to a string')
        else:
            try:
                value_shape = '^' + value_shape + '$'
                self.add_column(name=name, data_type=ColumnDataType.NUMBER, value_shape=re.compile(value_shape))
                self._block_column_name = name
            except Exception:
                raise ValueError('Block column value shape wasnt valid regex')

    def add_block_and_trial_column(self, name, value_shape):
        if type(value_shape) is not str:
            raise TypeError('Block and trial column value_shape must be set to a string')
        else:
            try:
                value_shape = '^' + value_shape + '$'
                # TODO: make a specific kind of column that handles the trial/block better
                self.add_column(name=name, data_type=ColumnDataType.STRING, value_shape=re.compile(value_shape))
                self._trial_column_name = name
                self._block_column_name = name
            except Exception:
                raise ValueError('Block and trial value shape wasnt valid regex')

    @property
    def columns(self):
        return self._columns

    def verify(self):
        if not self._block_column_name or not self._trial_column_name:
            return False

        return True

    @property
    def block_column_name(self):
        return self._block_column_name

    @property
    def trial_column_name(self):
        return self._trial_column_name
