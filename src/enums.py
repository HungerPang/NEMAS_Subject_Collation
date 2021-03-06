from enum import Enum

class ColumnDataType(Enum):
    STRING = 1
    NUMBER = 2
    CORRECTNESS = 3
    ENUM = 4


class OtherDataValues(Enum):
    NONE = 'None'
    NR = 'NR'
    CATCH = 'Catch'
    NOTHING = 'nothing'