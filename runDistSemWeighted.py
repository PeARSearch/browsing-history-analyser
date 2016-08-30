""" Make page representation as the WEIGHTED sum of the most 'important'
words in the page (obtained via entropy calculation)
"""

import math
import os
import re
import sys

import numpy as np
from utils import load_entropies, normalise, cosine_similarity,\
doc_distribution, print_array

path_to_PeARS = "/home/aurelie/PeARS-org/browsing-history-analyser/"
num_dimensions = 400
stopwords = ["", "(", ")", "a", "about", "an", "and", "are", "around", "as", "at", "away", "be", "become", "became",
             "been", "being", "by", "did", "do", "does", "during", "each", "for", "from", "get", "have", "has", "had",
             "he", "her", "his", "how", "i", "if", "in", "is", "it", "its", "made", "make", "many", "most", "not", "of",
             "on", "or", "s", "she", "some", "that", "the", "their", "there", "this", "these", "those", "to", "under",
             "was", "were", "what", "when", "where", "which", "who", "will", "with", "you", "your"]

dm_dict = {}  # Dictionary to store dm file
doc_dists = []  # Which files already have a distribution
entropies_dict=load_entropies()


def weightFile(buff):
    word_dict = {}
    words = buff.split()
    for w in words:
        w = w.lower()
        if w in entropies_dict and w not in stopwords:
            if w in word_dict:
                word_dict[w] += 1
            else:
                word_dict[w] = 1
    for k, v in word_dict.items():
        if math.log(entropies_dict[k] + 1) > 0:
            word_dict[k] = float(v) / float(math.log(entropies_dict[k] + 1))
    return word_dict


def mkVector(word_dict):
    """ Make vectors from weights """
    # Initialise vbase and doc_dist vectors
    vbase = np.zeros(num_dimensions)
    # Add vectors together
    if len(word_dict) > 0:
        c = 0
        for w in sorted(word_dict, key=word_dict.get, reverse=True):
            if c < 5:
                # print w,word_dict[w]
                if w in dm_dict:
                    vbase = vbase + float(word_dict[w]) * np.array(dm_dict[w])
            c += 1

        vbase = normalise(vbase)

    # Make string version of document distribution
    doc_dist_str = ""
    for n in vbase:
        doc_dist_str = doc_dist_str + "%.6f" % n + " "

    # print "Computing nearest neighbours..."
    # sim_to_matrix(array(vbase),20)
    return doc_dist_str


def runScript(infile, out):
    docdists = open(out, "w")

    f = open(infile, 'r')
    buff = ""
    line_counter = 0
    for l in f:
        l = l.rstrip('\n')
        if "<doc" in l:
            doc_id = ""
            m = re.search("<doc url=\"(.*)\".*title=\"(.*)\"", l)
            url = m.group(1)
            title = m.group(2)
            print url
        else:
            if "</doc" not in l:
                # Ignore lines after number 20 and those with one word only
                if line_counter < 20: #and len(l.split()) > 1:
                    buff += l + " "
                    line_counter += 1
                else:
                    continue
            else:
                v = weightFile(buff)
                # s = mkVector(v)
                print buff
                s = doc_distribution(unicode(buff), entropies_dict, v)
                docdists.write(url + " " + print_array(s) + "\n")
                buff = ""
                line_counter = 0
    f.close()
    docdists.close()


# when executing as script
if __name__ == '__main__':
    runScript(sys.argv[1], sys.argv[2])
