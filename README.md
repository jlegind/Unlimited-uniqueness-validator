# Unlimited-uniqueness-validator
### Validation of record identifier uniqueness regardless of file size.

The core class CheckDuplicates reads the input it gets into chunks continually. Each chunk is checked for duplicates and these duplicates are written into a dictionary object with each identifier as key and the number of times it appears as the value.
When the input file is exhausted and chunked, all the chunks are compared against each other `compare_chunks()` and the dictionary is updated with additional duplicates. `compare_chunks()` returns the dictionary of duplicates.  

Below is an example of how the CheckDuplicates class could be employed. This should be improved.
#### Task
This new class using the CheckDuplicates class for duplicate detection should allow for csv files and other types of column separators to be ingestable. Also identifiers consisting of multiple fields should be allowed.


```
def run_main(writes=0):
    dup = CheckDuplicates(2000000, threshold=2)
    #The first arg is how many values each chunk can have. This can be tweaked to fit to memory. 2M is a conservative figure.
    #Threshold sets the number of duplicates required to be a concern.  
    mypath = 'G:/dwc_archives/inaturalist.txt'
    write_path = 'G:/duplicates.txt'
    dwcP = DwcProcessor(mypath)
    #DwcProcessor could be an external class that reads occurrence text files

    
    for j in dwcP.read_field(0, ">", 0, "\t", 1):        
        dup.create_chunk(j)
    except:
        print 'error'
	
    dup.create_chunk(None)
    distill =  dup.compare_chunks()

    if writes == 0:
        print('Print to console...')
        for k, v in distill[0].items():
            print '%s\t%d' % (k, v)
    else:
        print 'writing to file', write_path
        #Some code writing to a file
		
def main():
    print(timeit.timeit("run_main(0)", setup="from __main__ import run_main", number=1)), 'time spent'
```
