import csv

from src.enums import ColumnDataType, OtherDataValues
from src.subject_data.subject_file_template import SubjectFileTemplate
from src.util import SINGLE_DIGIT, DOUBLE_DIGIT, NAME_END, MONTH_STRING, YYYY, TIME, DD, SUBJECT_ID
from src.subject_data.subject_file_factory import SubjectFileFactory
from src.output_data.output_file_template import OutputFileTemplate

from src.aggregation_functions.accuracy import accuracy

def main():
    input_template = SubjectFileTemplate()
    name_shape = SUBJECT_ID + '_' + YYYY + '_' + MONTH_STRING + '_' + DD + '_' + TIME + '_RespRecoded.csv' + NAME_END
    input_template.add_subject_name_shape(name_shape=name_shape)
    input_template.add_block_and_trial_column(name='Trial',value_shape=SINGLE_DIGIT + '_' + DOUBLE_DIGIT)
    input_template.add_column(name='resp', data_type=ColumnDataType.CORRECTNESS, replace_values=[OtherDataValues.NR])
    input_template.add_column(name='Cue', data_type=ColumnDataType.STRING)
    input_template.add_column(name='Stim', data_type=ColumnDataType.STRING, replace_values=[OtherDataValues.CATCH])
    input_template.add_column(name='rt', data_type=ColumnDataType.NUMBER, replace_values=[OtherDataValues.CATCH])

    factory = SubjectFileFactory(input_template)
    subject_file = factory.make_subject_file('C:/Users/anyst/Downloads/ETEMP1_fMRI_v2.2 229_2018_May_23_1601_RespRecoded.csv')
    vals = subject_file['Trial']
    cols = [col for col in subject_file]

    output_template = OutputFileTemplate('temp')
    output_template.add_column(name='fcff_accuracy', aggregation_function=accuracy, aggregation_args=['resp', 'Stim'])

    output_template.add_subject_data(subject_file)
    der = output_template.write()
    pass
main()
