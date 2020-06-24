
import os
import ast
import datetime


def read_callback_lines(callback_log_file):
    with open(callback_log_file, 'r') as f:
        callback_lines = f.readlines()
    return callback_lines


def write_out_times(sorted_time_dct):
    out_file = os.path.join(os.getcwd(), 'sorted_node_times.txt')
    with open(out_file, 'wt') as f:
        for entry in sorted_time_dct:
            f.write(str(entry))
            f.write('\n')
    print('Wrote out {0}.'.format(out_file))


def parse_callback_times(callback_lines):
    time_dct = {}

    for line in callback_lines:
        line_dct = ast.literal_eval(line)

        if 'start' not in line_dct.keys() or 'finish' not in line_dct.keys():
            continue

        node_id = line_dct['id']
        start = line_dct['start']
        end = line_dct['finish']

        start_time = start.split('.')[0]
        end_time = end.split('.')[0]

        d1 = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        d2 = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
        diff = (d2 - d1).total_seconds()

        time_dct[node_id] = diff

    # pre-Python 3.6 version
    import operator
    sorted_time_dct = sorted(time_dct.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_time_dct

    for entry in sorted_time_dct:
        print(entry)


import sys

callback_lines = read_callback_lines(sys.argv[1])
sorted_time_dct = parse_callback_times(callback_lines)
write_out_times(sorted_time_dct)
