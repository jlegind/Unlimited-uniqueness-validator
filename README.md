# Unlimited-uniqueness-validator
### Validation of record identifier uniqueness regardless of file size.

The core class CheckDuplicates reads the input it gets into chunks continually. Each chunk is checked for duplicates and these duplicates are written into a dictionary object with each identifier as key and the number of times it appears as the value.
When the input file is exhausted and chunked, all the chunks are compared against each other `compare_chunks()` and the dictionary is updated with additional duplicates. `compare_chunks()` returns the dictionary of duplicates.  

Below is an example of how the CheckDuplicates class could be employed. This should be improved.
#### Task
This new class using the CheckDuplicates class for duplicate detection should allow for csv files and other types of column separators to be ingestable. Also identifiers consisting of multiple fields should be allowed.


```
def run_main(readpath, writepath, field_index=0, writes=0):
    dup = chk.CheckDuplicates(2000000, threshold=2)
    # The first arg is how many values each chunk can have. This can be tweaked to fit to memory. 2M is a conservative figure.
    # Threshold sets the number of duplicates required to be a concern.
    mypath = readpath
    write_path = writepath
    dwcP = dwcProcessor.DwcProcessor(mypath, delimiter=',')
    # DwcProcessor could be an external class that reads occurrence text files
    # try:
    for j in dwcP.read_field(field_index):

        dup.create_chunk(j)

    dup.create_chunk(None)
    distill = dup.compare_chunks()

    if writes == 0:
        print('Print to console...')
        for k, v in distill[0].items():
            print '%s\t%d' % (k, v)
    else:
        print('writing to file', write_path)
        # Some code writing to a file

```
