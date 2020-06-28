import os

from src.subject_data.subject_file_template import SubjectFileTemplate
from src.subject_data.subject_file_factory import SubjectFileFactory
from src.output_data.output_file_template import OutputFileTemplate

class Collator:
    def __init__(self):
        self._subject_file_template = None
        self._output_file_template = None
        self._subject_file_locations = []

    def set_subject_file_template(self, subject_file_template: SubjectFileTemplate):
        if type(subject_file_template) is not SubjectFileTemplate:
            raise TypeError('Subject file template must be a subject file template')
        else:
            self._subject_file_template = subject_file_template

    def set_output_file_template(self, output_file_template: OutputFileTemplate):
        if type(output_file_template) is not OutputFileTemplate:
            raise TypeError('Output file template must be an output file template')
        else:
            self._output_file_template = output_file_template

    def add_subject_file_location(self, path: str):
        if not os.path.exists(path):
            raise ValueError('The path {} does not exist'.format(path))
        else:
            self._subject_file_locations += [path]

    def collate(self):
        if not self.verify():
            raise ValueError('Collator needs a subject template, an output template, and at least one subject file '
                             'location')
        subject_factory = SubjectFileFactory(self._subject_file_template)
        for location in self._subject_file_locations:
            for file in os.listdir(location):
                if self._subject_file_template.matches_name_shape(file):
                    fullpath = os.path.join(location, file)
                    subject = subject_factory.make_subject_file(fullpath)
                    self._output_file_template.add_subject_data(subject)
        self._output_file_template.write()

    def verify(self):
        if not self._subject_file_template or not self._output_file_template:
            return False

        if len(self._subject_file_locations) <= 0:
            return False

        if not self._subject_file_template.verify():
            return False

        if not self._output_file_template.verify():
            return False

        return True
