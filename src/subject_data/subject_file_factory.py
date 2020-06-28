from .subject_file import SubjectFile

class SubjectFileFactory:
    def __init__(self, subject_file_template):
        self._subject_file_template = subject_file_template

    def make_subject_file(self, file_name):
        return SubjectFile(file_name, self._subject_file_template)
