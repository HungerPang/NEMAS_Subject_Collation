import re
from .input_column import InputColumn
from src.enums import ColumnDataType


class SubjectFileTemplate():
    def __init__(self):
        self._columns = {}
        self._block_column_name = None
        self._trial_column_name = None
        self._name_shape = None

    def add_subject_name_shape(self, name_shape=None):
        if type(name_shape) is not str:
            raise TypeError('Subject name shape must be a string')
        else:
            try:
                self._name_shape = re.compile(name_shape)
            except Exception as e:
               raise ValueError('Bad regex input for subject name shape').with_traceback(e)

    def add_column(self, name=None, data_type=None, value_shape=None, replace_values=[]):
        if type(name) is str and type(data_type) is ColumnDataType:
            self._columns[name] = InputColumn(name, data_type, value_shape, replace_values)
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

    def matches_name_shape(self, val):
        return self._name_shape.search(val)

    def extract_subject_id(self, val):
        match = self._name_shape.search(val)
        if match:
            if match.group('SubjectId'):
                return match.group('SubjectId')
            else:
                raise ValueError("Subject name shape doesnt contain the Subject id block, which is to say"
                                 " the name shape doesnt contain a capture block named SubjectId")
        else:
            raise ValueError('No match found while extracting subject id')

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
