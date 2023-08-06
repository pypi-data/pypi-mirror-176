import logging
import random
from os.path import join


def generate_input_file(directory, file_name, start=-500000, end=500000, num_of_elements=100000):
    """
    Generates a file which is huge enough to test the logic out
    :param directory: the directory to place the files in
    :param file_name: the name of the generated file
    :param start: the start range for the integer values to be placed in output file
    :param end: the end range for the integer values to be placed in output file
    :param num_of_elements: number of elements to be generated
    :return: the input file path
    """
    input_file = join(directory, file_name)
    logging.info(f"Generating input file: {input_file}")
    with open(input_file, 'w') as temp_f:
        for _ in range(num_of_elements):
            temp_f.write(f"{random.randint(start, end)}\n")
    return input_file
