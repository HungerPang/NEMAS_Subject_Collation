import re
from pandas.io.parsers import read_csv, Series

# TODO: add a verify to make sure the columns found match the columns expected
class SubjectFile:
    def __init__(self, file_name, subject_file_template):
        self._file_name = file_name
        self._subject_file_template = subject_file_template
        self._column_names = []
        self._index = 0
        self._num_data_rows = 0
        if self._subject_file_template.matches_name_shape(file_name):
            self._subject_id = self._subject_file_template.extract_subject_id(file_name)
        else:
            self._subject_id = 'XXX'

        self._csv = read_csv(self._file_name)
        for template_column in self._subject_file_template.columns.values():
            for value_column in self._csv.columns:
                if template_column.name == value_column:
                    self._column_names += [template_column.name]

        template_cols = self._subject_file_template.columns
        block_col_name = self._subject_file_template.block_column_name
        block_vals = [val for val in [series for series in self._csv[block_col_name]]]
        while template_cols[block_col_name].matches_value_shape(block_vals[self._num_data_rows]):
            self._num_data_rows += 1

        if self._subject_file_template.block_column_name != self._subject_file_template.trial_column_name:
            trial_col_name = self._subject_file_template.trial_column_name
            trial_vals = [val for val in [series for series in self._csv[block_col_name]]]
            double_check = 0
            while template_cols[trial_col_name].matches_value_shape(trial_vals[double_check]):
                double_check += 1

            if self._num_data_rows == double_check:
                raise ValueError('Trial and block rows probably have different length')

        self._csv = read_csv(self._file_name)
        for template_column in self._subject_file_template.columns.values():
            for value_column in self._csv.columns:
                if template_column.name == value_column:
                    input_column = self._subject_file_template.columns[template_column.name]
                    input_data = [val for val in self._csv[template_column.name]][:self._num_data_rows]
                    self._csv[template_column.name] = Series(data=input_column.transform_column(input_data))

    @property
    def subject_id(self):
        return self._subject_id

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index < len(self._column_names):
            retval = [val for val in self._csv[self._column_names[self._index]]][:self._num_data_rows]
            self._index += 1
            return retval
        else:
            raise StopIteration

    def verify(self):
        if len(self._subject_file_template.columns) != len(self._column_names):
            return False

        return True

    # TODO transform the column data to the expected type
    def __getitem__(self, col_name):
        return [val for val in self._csv[col_name]][:self._num_data_rows]
