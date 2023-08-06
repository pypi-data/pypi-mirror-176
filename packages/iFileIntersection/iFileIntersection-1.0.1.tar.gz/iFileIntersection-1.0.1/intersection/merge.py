from contextlib import ExitStack
from os import makedirs
from os.path import join

from intersection.file import next_value, write_value


def merge_sorted_files(file_paths, destination_dir):
    """
    Merges K-sorted files into a single file
    :param file_paths: the list of file paths consisting of sorted values
    :param destination_dir: the directory to place the merged file in
    :return: file path to the merged outcome file
    """
    merged_dir = join(destination_dir, "merged")
    makedirs(merged_dir)
    while len(file_paths) > 1:
        file_paths = _merge(file_paths, merged_dir)
    return file_paths[0]


def _merge(file_paths, working_dir):
    files_to_merge = []
    for i in range(0, len(file_paths), 2):
        with ExitStack() as stack:
            file_1 = stack.enter_context(open(file_paths[i], 'r'))
            file_2 = stack.enter_context(open(file_paths[i + 1], 'r')) if (i + 1) < len(file_paths) else None
            merged_file_name = join(working_dir, str(i))
            merged_file = stack.enter_context(open(merged_file_name, 'w'))
            _merge_values(file_1, file_2, merged_file)
            files_to_merge.append(merged_file_name)
    return files_to_merge


def _merge_values(first_file, second_file, merged_file):
    value_1 = next_value(first_file)
    value_2 = next_value(second_file)
    while value_1 and value_2:
        if value_1 < value_2:
            write_value(merged_file, value_1)
            value_1 = next_value(first_file)
        elif value_1 > value_2:
            write_value(merged_file, value_2)
            value_2 = next_value(second_file)
        else:
            write_value(merged_file, value_1)
            value_1 = next_value(first_file)
            value_2 = next_value(second_file)

    if value_1:
        while value_1:
            write_value(merged_file, value_1)
            value_1 = next_value(first_file)

    if value_2:
        while value_2:
            write_value(merged_file, value_2)
            value_2 = next_value(second_file)
