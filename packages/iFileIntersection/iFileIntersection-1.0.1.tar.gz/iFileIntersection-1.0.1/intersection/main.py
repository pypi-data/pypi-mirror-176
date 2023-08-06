import logging
import tempfile
from contextlib import ExitStack
from os import makedirs
from os.path import join

from intersection.args import process_command_line_args
from intersection.file import chunk_file, next_value, write_value
from intersection.merge import merge_sorted_files
from intersection.validation import validate_file_exists


def setup_for_cleanup(method):
    """
    Decorator to cleanup all intermediate files used during the processing
    :param method: the method invoked for finding the intersection
    :return: returned value from underlying method invocation
    """

    def process(*args, working_directory=None, **kwargs):
        if working_directory:
            return method(*args, working_dir=working_directory, **kwargs)
        else:
            with tempfile.TemporaryDirectory() as working_directory:
                return method(*args, working_dir=working_directory, **kwargs)

    return process


FIRST_FILE_WORK_SUB_DIR = "_ONE"
SECOND_FILE_WORK_SUB_DIR = "_TWO"


@setup_for_cleanup
def find_intersection(first_file_path, second_file_path, output_file_path, chunk_size=None, working_dir=None):
    """
    Finds the common integers given two file paths.

    NOTE:
    - Assumption here is that the files provided are too huge.
    - Hence can't be kept in memory and processed to find the common integers

    :param first_file_path: fully qualified path to the first file containing integers
    :param second_file_path: fully qualified path to the second file containing integers
    :param output_file_path: fully qualified path to the output file where the results will be stored
    :param chunk_size: the size in MB to split the files into chunks. Chunks would be approx the size provided
    :param working_dir: the directory to  place intermediate files. If none specified a dir in temp is used
    :return: fully qualified path to the output file
    """
    # Validate file exists
    validate_file_exists(first_file_path)
    validate_file_exists(second_file_path)
    logging.info(f"Validated files {first_file_path} & {second_file_path} exists")

    # Generate a sorted file for both inputs
    first_file = _generate_sorted_file(first_file_path, FIRST_FILE_WORK_SUB_DIR, working_dir, chunk_size)
    logging.info(f"First file has been sorted and put back to {first_file}")
    second_file = _generate_sorted_file(second_file_path, SECOND_FILE_WORK_SUB_DIR, working_dir, chunk_size)
    logging.info(f"Second file has been sorted and put back to {second_file}")

    # Find the common integers in each
    _find_common(first_file, second_file, output_file_path)


def _generate_sorted_file(file_path, prefix_dir, working_directory, chunk_size):
    file_dir = join(working_directory, prefix_dir)
    makedirs(file_dir)
    sorted_chunk_paths = _chunk_and_sort_files(file_path, file_dir, chunk_size)
    logging.info(f"Chunked and sorted {file_path} into {len(sorted_chunk_paths)} files")
    return merge_sorted_files(sorted_chunk_paths, file_dir)


def _chunk_and_sort_files(file_name, destination_dir, chunk_size):
    sorted_files = []
    sorted_dir = join(destination_dir, "sorted")
    makedirs(sorted_dir)
    for counter, chunk in enumerate(chunk_file(file_name, chunk_size=chunk_size)):
        values = sorted([int(value) for value in chunk if value])
        sort_file_path = join(sorted_dir, str(counter))
        with open(sort_file_path, 'w') as chunk_f:
            chunk_f.writelines([f"{value}\n" for value in values])
        sorted_files.append(sort_file_path)
    return sorted_files


def _find_common(first_file, second_file, destination_file):
    logging.info(f"Finding common in {first_file} & {second_file}. Writing results to: {destination_file}")
    with ExitStack() as stack:
        first_file = stack.enter_context(open(first_file, 'r'))
        second_file = stack.enter_context(open(second_file, 'r'))
        destination_file = stack.enter_context(open(destination_file, 'w'))
        value_1 = next_value(first_file)
        value_2 = next_value(second_file)
        while value_1 and value_2:
            if value_1 == value_2:
                write_value(destination_file, value_1)
                value_1 = next_value(first_file)
                value_2 = next_value(second_file)
            elif value_1 < value_2:
                value_1 = next_value(first_file)
            else:
                value_2 = next_value(second_file)


def main():
    if __name__ == '__main__':
        logging.basicConfig(level=logging.DEBUG)
        parsed_args = process_command_line_args()
        find_intersection(parsed_args.file_1, parsed_args.file_2, parsed_args.out_file_path)
    # with tempfile.TemporaryDirectory() as temp_directory:
    #     # file_1_path = generate_input_file(temp_directory, "file_1.txt")
    #     # file_2_path = generate_input_file(temp_directory, "file_2.txt")
    #     file_1_path = "D:\\apple\\file_1.txt"
    #     file_2_path = "D:\\apple\\file_2.txt"
    #     intersection(file_1_path, file_2_path, "D:\\final_out.txt")


main()
