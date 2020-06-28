

class OutputColumn:
    def __init__(self, name, aggregation_function, aggregation_args, aggregation_kwargs):
        self._name = name
        self._aggregation_function = aggregation_function
        self._aggregation_args = aggregation_args
        self._aggregation_kwargs = aggregation_kwargs

    def process_data(self, subject_file):
        subjects_args = []
        for arg in self._aggregation_args:
            subjects_args += [subject_file[arg]]

        subject_kwargs = {}
        for key, arg in self._aggregation_kwargs:
            subject_kwargs[key] = subject_file[arg]

        return self._aggregation_function(*subjects_args, *subject_kwargs)

    @property
    def name(self):
        return self._name
