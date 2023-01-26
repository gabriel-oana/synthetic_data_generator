def split_sequence(max_value: int, step: int):

    batch_no = int(max_value / step)
    remainder = max_value - (batch_no * step)
    repeated_list = [step] * batch_no
    if remainder > 0:
        repeated_list.append(remainder)

    return repeated_list
