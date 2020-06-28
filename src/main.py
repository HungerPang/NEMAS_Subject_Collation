import csv

from src.enums import ColumnDataType, OtherDataValues
from src.subject_data.subject_file_template import SubjectFileTemplate
from src.util import SINGLE_DIGIT, DOUBLE_DIGIT, NAME_END, MONTH_STRING, YYYY, TIME, DD, SUBJECT_ID
from src.subject_data.subject_file_factory import SubjectFileFactory
from src.output_data.output_file_template import OutputFileTemplate
from src.collator import Collator

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

    output_template = OutputFileTemplate('C:/Users/anyst/colaltion_test.csv')
    output_template.add_column(name='fcff_accuracy', aggregation_function=accuracy, aggregation_args=['resp', 'Stim'])

    collator = Collator()
    collator.set_output_file_template(output_file_template=output_template)
    collator.set_subject_file_template(subject_file_template=input_template)
    collator.add_subject_file_location('C:/Users/anyst/collation_daters')
    collator.collate()
main()
