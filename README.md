# Unlimited-uniqueness-validator
Validation of record identifier uniqueness regardless of file size

The 

```
def run_main(writes=0):
	dup = CheckDuplicates(2000000, threshold=2)
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
