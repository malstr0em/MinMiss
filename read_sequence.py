import os


def read_sequence(file_path):
    '''
    ﻿Reads a *.seq-file and returns a list corresponding to the sequence in the file
    :param file_path: a string containing the relative path to the *.seq-file
    :return: sequence: ﻿a list containing the sequence of the *.seq file
    '''

    sequence = list()
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, file_path)

    try:
        with open(file_path, "r") as f:
            print("Reading Sequence...")
            for line in f:
                sequence.append(int(line))

        print("Sequence read\nNumber of Elements: {1} \nLength: {0}".format(len(sequence), len(set(sequence))))
        return sequence

    except IOError as e:
        print(os.strerror(e.errno))
        exit()

    return sequence

