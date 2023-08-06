import logging

DEFAULT_CHUNK_SIZE_IN_MB = 25


def chunk_file(file_path: str, chunk_size=None):
    """
    Chunks the file based on available memory

    NOTE:
    - Recommended to use temp directory for destination_directory param.
    - This would ensure the directory is deleted automatically once the processing is complete

    :param file_path: the fully qualified path to the file to be chunked
    :param chunk_size: override chunk file size in MB
    """
    logging.info(f"File: {file_path}, Chosen Chunk Size: ~{chunk_size} MB")
    chunk_size = (chunk_size or DEFAULT_CHUNK_SIZE_IN_MB) * (1024 ** 2)  # Bytes
    with open(file_path, 'r') as f:
        chunk = f.readlines(chunk_size)
        while chunk:
            yield chunk
            chunk = f.readlines(chunk_size)


def next_value(file_cursor):
    """
    Reads the next available and value
    :param file_cursor: the cursor to the opened file
    :return: the integer value, None if not available
    """
    value = file_cursor.readline() if file_cursor else None
    return int(value) if value else None


def write_value(file_cursor, value: int):
    """
     Writes the value into the file
    :param file_cursor: the cursor to the opened file
    :param value: the value to be written
    """
    file_cursor.write(str(value))
    file_cursor.write("\n")
