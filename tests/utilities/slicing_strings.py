def slice_strings(expected, actual):
    actual_len = len(actual.split(' ')[0])
    part1 = expected[:actual_len]
    part2 = expected[actual_len:]

    return part1 + ' ' + part2
