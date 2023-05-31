# Flag-headlines-with-Bloom-Filter
AFINN is a lexicon of English words rated for valence with an integer between minus five (negative) and plus five (positive). The lexicon used in this small project is from https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt'.
The purpose of this project is to flag headlines that include words with AFINN scores of -4 or -5.
There are three files:
1. 'generate-bloom-filter.py': Using two hash functions to create a hash table of size 1000 bit-vector with the 'bad' words (63 words with AFINN scores of -4 or -5). Also, the probability of binary data getting corrupt is high in its raw form, So binary-to-text encoding: Base64 is used to convert hash table into text.
2. ' 
