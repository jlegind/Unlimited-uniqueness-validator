import check_duplicates_beta_extended as chk
import dwcProcessor
import timeit

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
        # print 'printing j: ', j
        dup.create_chunk(j)
    # except:
    #     print 'error'


    dup.create_chunk(None)
    distill = dup.compare_chunks()

    if writes == 0:
        print('Print to console...')
        for k, v in distill[0].items():
            print '%s\t%d' % (k, v)
    else:
        print('writing to file', write_path)
        # Some code writing to a file


def main():
    print(timeit.timeit("run_main(0)", setup="from __main__ import run_main", number=1)), 'time spent'