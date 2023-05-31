#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 23:02:02 2023

@author: yuanyuan
"""
import numpy as np
import hashlib
import base64

url = 'https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt'
afinn = np.loadtxt(url, dtype = str, delimiter = '\t')


badwords = []
for i in range(len(afinn)):
    if -5 <= int(afinn[i, 1]) <= -4:
        badwords.append(afinn[i, 0])

num_badwords = len(badwords)  ## 63 bad words.


m = 1000 # hash table size
# using two hash functions
def h1(w):
    h = hashlib.md5(w.encode("utf-8"))
    return hash(h.digest())

def h2(w):
    h = hashlib.sha256(w.encode("utf-8"))
    return hash(h.digest())

def generate_bloom_filter(words):
    hash_table = [0] * m
    for word in words:
        hash1 = h1(word) % m
        hash2 = h2(word) % m
                
        if not (hash_table[hash1] and hash_table[hash2]):            
            hash_table[hash1] = 1
            hash_table[hash2] = 1
        else:
            print("Warning: word conflicts, {}, hash value {} and {}".format(word, hash1, hash2))        
    return hash_table

bloom_filter = generate_bloom_filter(badwords)

bloomfilter64 = base64.b64encode(bytes(bloom_filter)).decode()
# check base64 decoding is right
# d_bloom_filter = list(base64.b64decode(bloomfilter64.encode()))

with open("bloomfilter64.txt", "w") as text_file:
    text_file.write(bloomfilter64)
















