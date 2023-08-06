## i-file-utils

This project holds certain utilities which can help with file operations. Currently, the functionalities available are:

1) Find common integers between files

## Time Complexity

### Steps

- The script aims to process huge files which cannot fit into memory
- So the algorithm take following approach:

1) Chunk the huge file into smaller files - This is configurable but defaults to **100 MB** chunks if not provided
2) When the chunking is done, the chunks are also sorted so that we can find the common elements easily later
3) The chunks are then merged back into a single file. This process is repeated for both the input files
4) And then we iterate through the files to find common elements

**NOTE**

- All the intermediate files generated are stored in temp which would be cleaned up automatically

### Big-O Notation

1) Let <code>Number of integers in File 1 = m</code>
2) Let <code>Number of integers in File 2 = n</code>
3) Let <code>Number of chunks = c</code>
4) Let <code>Number of elements in each chunk = k</code>
5) Step 1 and Step 2 would take <code>O(c * (k * log k)) + O(c * (k * log k))</code>
6) It would reduce to <code>O(c * (k * log k))</code>, _ignoring constant 2 from result from above_
7) Step 3 would need <code>O(k * log(c))</code>
8) Step 4 we would go through the same number of elements as input: <code>2 * (O(m) + O(n))</code>
9) Complexity of 8, would reduce to  <code>O(m) + O(n)</code>, _ignoring constant 2 again_
10) Overall complexity would be complexity of <code>Complexity of 6 + Complexity of 7 + Complexity of 9</code>

**NOTE:**

- The overall **_wall clock time can be reduced_** by parellising Steps 1 & 2
- The above is possible as there is no interdependency in chunking and sorting
- We could also tweak the chunk size to optimize the processing further

## Oh nice! How do I use it??

### Pre-requisites

1) Install python 3 and above version
2) Upgrade pip - https://pip.pypa.io/en/stable/installation/

## Install the package

1) https://pypi.org/project/iFileIntersection/
2) If lazy to open the link, run this command - pip install iFileIntersection

## I am all set! Help me run it

1) Running it is how you would run any other python program:
2) <code>python -m intersection.main --help</code>
3) Above command would show all the options you can pass in
4) <code>python -m intersection.main --file_1 <fully_qualified_path_to_first_file> --file_2 <
   fully_qualified_path_to_second_file> --out_file_path <fully_qualified_path_to_output_file></code>
5) If this package is a dependency to your package you can invoke the logic as follows:

   <code>from intersection.main import find_intersection</code>
   <code>find_intersection(file_path_1, file_path_2, output_file_path)</code>

## Contact

- Feel free to reach out to me at nikhilkm.dev@gmail.com if any questions