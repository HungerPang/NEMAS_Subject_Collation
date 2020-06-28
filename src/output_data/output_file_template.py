from .output_column import OutputColumn
from pandas import DataFrame

class OutputFileTemplate:
    def __init__(self, output_file_name):
        self._output_file_name = output_file_name
        self._columns = {}
        self._ouput_data = {'sub': []}

    # TODO add a way to put in expected exceptions to data type, eg. NR, None, Catch, etc.
    def add_column(self, name=None, aggregation_function=None, aggregation_args=[], aggregation_kwargs={}):
        if type(name) is not str:
            raise ValueError('Column name must be set to a string')
        elif type(aggregation_args) is not list:
            raise ValueError('Aggregation args should be a list of columns from the input to pass to the output')
        elif not callable(aggregation_function):
            raise ValueError('Aggregation function needs to be a callable, like a function')
        else:
            self._columns[name] = OutputColumn(name=name, aggregation_function=aggregation_function,
                                               aggregation_args=aggregation_args, aggregation_kwargs=aggregation_kwargs)
            self._ouput_data[name] = []

    def verify(self):
        return True

    def add_subject_data(self, subject_file):
        self._ouput_data['sub'] += [subject_file.subject_id]
        for name, column in self._columns.items():
            self._ouput_data[name] += [column.process_data(subject_file)]

    def write(self):
        data_frame = DataFrame(data=self._ouput_data)
        data_frame.to_csv(self._output_file_name, index=False)
