#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 11:27:01 2023

@author: yuanyuan
"""
import sys

import hashlib
import base64
import subprocess

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

pipe = subprocess.Popen(["hadoop", "fs", "-cat", "/user/yuanyuan/bloomfilter64.txt"], stdout=subprocess.PIPE)
bloomfilter64 = pipe.communicate()[0]
bloom_filter_vec = list(base64.b64decode(bloomfilter64))
# print("{}, {}".format(len(bloom_filter_vec),sum(bloom_filter_vec)))

def h1(w):
    h = hashlib.md5(w.encode("utf-8"))
    return hash(h.digest())
    
def h2(w):
    h = hashlib.sha256(w.encode("utf-8"))
    return hash(h.digest()) 

def bloom_filter(rdd):
    
    head = rdd.collect()
    if len(head) != 0:
        words = head[0]
        for word in words.split(' '):
            hash1 = h1(word) % 1000
            hash2 = h2(word) % 1000
            if bloom_filter_vec[hash1]==1 and bloom_filter_vec[hash2]==1:
                print(words)
                return    
        # print('{}'.format(head))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: dstream-with-bloomfilter.py <hostname> <port>", file=sys.stderr)
        sys.exit(-1)
    sc = SparkContext(appName="dstream-with-bloomfilter")
    ssc = StreamingContext(sc, 1)
    
    ssc.checkpoint("~/big-data-repo")

    lines = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))

    headline = lines.window(1,1)
    
    headline.foreachRDD(bloom_filter)
    
    # headline.pprint()

    ssc.start()
    ssc.awaitTermination()
    