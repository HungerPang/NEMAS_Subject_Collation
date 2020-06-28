import csv

from src.enums import ColumnDataType
from src.subject_data.subject_file_template import SubjectFileTemplate, SINGLE_DIGIT, DOUBLE_DIGIT
from src.subject_data.subject_file_factory import SubjectFileFactory

def main():
    input_template = SubjectFileTemplate()
    input_template.add_block_and_trial_column(name='Trial',value_shape=SINGLE_DIGIT + '_' + DOUBLE_DIGIT)
    input_template.add_column(name='resp', data_type=ColumnDataType.CORRECTNESS)
    input_template.add_column(name='Cue', data_type=ColumnDataType.STRING)
    input_template.add_column(name='Stim', data_type=ColumnDataType.STRING)

    factory = SubjectFileFactory(input_template)
    subject_file = factory.make_subject_file('C:/Users/anyst/Downloads/ETEMP1_fMRI_v2.2 229_2018_May_23_1601_RespRecoded.csv')
    vals = subject_file[0]
    cols = [col for col in subject_file]

    """
    output_template = OutputFileTemplate()
    output_template.add_column(name='fcff_accuracy', accuracy, ['resp', 'stim'])
    """
main()
