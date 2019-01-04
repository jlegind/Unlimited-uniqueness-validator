#-------------------------------------------------------------------------------
# Name:        check_duplicates_large
# Purpose:      To find properties that appear more than once in files that are
#               too large to hold in memory
# Author:      jlegind
#
# Created:     28-02-2014
# Copyright:   (c) jlegind 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import os
import shutil
import cPickle as pickle
from collections import Counter

class CheckDuplicates(object):
    cnt = Counter()
    n = 1
    v = 0
    my_list = []
    conglomerate = {}
    brine = []
    j = 0

    def __init__(self, chunk_size, threshold=2):
        self.chunk_size = chunk_size
        self.threshold = threshold
        ppath = 'c:/pickles/pickles'
        if(os.path.isdir(ppath)):
            print(ppath)
            os.rmdir(ppath)
        os.mkdir(ppath)

    def create_chunk(self, piece, stop=False):
        """Makes the chunk from my_list and sends it to chunk_check()"""

        if piece is None:
            self.chunk_check(self.my_list)
        if self.j < self.chunk_size:
            self.my_list.append(piece)
            self.j += 1
        if self.j >= self.chunk_size:
            #print self.j
            self.chunk_check(self.my_list)
            self.j = 0
            del self.my_list[:]

        #return self.chunk_check(self.my_list)

    def chunk_check(self, a_list):
        """Takes a list(chunk) and converts it to a dictionary listing each element
        the number of times it appears and a conglomerate of duplicates is created.
        The chunk is reduced and then pickled.
        Returns conglomerate."""
        my_list = a_list
        for index in my_list:
            self.cnt[index] += 1
        new_cnt = self.cnt.copy()
        path = 'c:/pickles/pickles/my_pickle%d' % (self.n)
        print path
        self.brine.append(path)

        for k, v in self.cnt.iteritems():
            if v >= self.threshold:
                try:
                    congl = self.conglomerate
                    if congl[k]:
                        congl[k] += new_cnt.pop(k)
                except KeyError:
                    congl[k] = new_cnt.pop(k)
        """Each chunk is processed into a conglomerate of all dictionary key-value pairs
        where the value > 1. Those key-value pairs are then removed from the chunk. """
        with open(path, 'wb') as ff:
            pickle.dump(new_cnt, ff, protocol=2)
        #The Count() object is pickled for comparison later
        self.n += 1
        #print self.cnt, 'test'

        self.cnt.clear()

        return self.conglomerate, 'Conglomerate'

    def compare_chunks(self):
        """All chunks are compared against one another. Returns conglomerate."""
        #WARNING!!! The threshold limit has not been implemented in this function !!!
        conglomerate = self.conglomerate
        while self.brine:
            with open(self.brine.pop(), 'rb') as a_file:
                print a_file
                my_chunk = pickle.load(a_file)
                test_chunk = my_chunk.copy()

                for k in my_chunk:
                    if k in conglomerate:
                        #Reduces the chunk as it appears in the conglomerate
                        conglomerate[k] += test_chunk.pop(k)

                for j in self.brine:
                    set1 = set(test_chunk)
                    with open(j, 'rb') as b_file:

                        #next_chunk = b_file
                        next_chunk = pickle.load(b_file)
                        set2 = set(next_chunk)
                        intersec = set1 & set2
                        #Tests key-value pairs across chunks and reduces accordingly
                        for k in intersec:
                            if k in conglomerate:
                                conglomerate[k] += 1
                                #print k, ':', conglomerate[k]
                            else:
                                conglomerate[k] = test_chunk.pop(k)

        shutil.rmtree('c:/pickles/pickles')
        return conglomerate, 'my conglomerate'
