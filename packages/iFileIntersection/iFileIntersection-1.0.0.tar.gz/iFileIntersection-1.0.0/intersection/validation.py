import os.path


def validate_file_exists(file_path):
    """
    Validates the file does exists. Throws an exception if it doesn't
    :param file_path: the file path
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Given input file {file_path} does not exists")
