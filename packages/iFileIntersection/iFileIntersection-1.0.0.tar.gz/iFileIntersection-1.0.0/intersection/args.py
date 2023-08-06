import argparse


def process_command_line_args():
    """
    Parses the command line arguments for the input files and necessary configurations for the program
    :return: parsed arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--file_1",
        help="Fully qualified path to the first file involved in finding intersection",
        required=True
    )
    arg_parser.add_argument(
        "--file_2",
        help="Fully qualified path to the second file involved in finding intersection",
        required=True,
    )
    arg_parser.add_argument(
        "--out_file_path",
        help="Fully qualified path to where the result must be stored",
        required=True,
    )
    arg_parser.add_argument(
        "--file_chunk_size",
        help="Size of chunks in MB to be used to split the files into",
        type=int,
        default=100,
    )
    return arg_parser.parse_args()
