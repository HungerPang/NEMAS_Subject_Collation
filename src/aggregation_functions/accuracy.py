from src.enums import OtherDataValues


def accuracy(resp, stim):
    total = 0
    sum = 0
    for resp, stim in zip(resp, stim):
        if resp is not OtherDataValues.NR:
            total += 1
            sum += resp
    return sum/total
