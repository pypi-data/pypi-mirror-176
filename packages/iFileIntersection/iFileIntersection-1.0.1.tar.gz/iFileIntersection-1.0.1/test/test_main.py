import tempfile

from intersection.helper import generate_input_file
from intersection import find_intersection


def test_find_intersection():
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file_1 = generate_input_file(temp_dir, "input_1.txt", start=-15, end=15, num_of_elements=10)
        input_file_2 = generate_input_file(temp_dir, "input_2.txt", start=-15, end=15, num_of_elements=10)
        with tempfile.TemporaryFile(dir=temp_dir) as temp_output_file:
            find_intersection(input_file_1, input_file_2, temp_output_file.name)
            output = temp_output_file.readlines()
            se
    assert False
