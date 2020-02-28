# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 14:21:15 2020

@author: Experimenter
"""

import collections, heapq

def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range (len(h))]


class Sentinel:
    pass


def david_eisenstat(lst):
    counts = collections.Counter(lst)
    heap = [(-count, key) for key, count in counts.items()]
    heapq.heapify(heap)
    output = []
    last = Sentinel()
    while heap:
        minuscount1, key1 = heapq.heappop(heap)
        if key1 != last or not heap:
            last = key1
            minuscount1 += 1
        else:
            minuscount2, key2 = heapq.heappop(heap)
            last = key2
            minuscount2 += 1
            if minuscount2 != 0:
                heapq.heappush(heap, (minuscount2, key2))
        output.append(last)
        if minuscount1 != 0:
            heapq.heappush(heap, (minuscount1, key1))
    return output