# -*- coding: utf-8 -*-
import sys
import os
import sllematizer

exceptions = ["leta"]

# Counters
lines = 0
candidates = 0
locations = 0
names = 0

def get_stopwords():
    f = open("stopwords.txt", "rb")
    stopwords = [word.decode("utf-8").strip() for word in f.readlines() if not word.startswith("#")]
    return set(stopwords)

def is_line_candidate(line):
    return line[0].isupper() or line.endswith(u"ski") or line.endswith(u"ški") or line.endswith(u"ska") or line.endswith(u"sko")

def get_lemmatizer():
    lib = os.path.dirname(__file__) + "/libLemmatizer.dylib"
    dic = os.path.dirname(__file__) + "/lemma_sl.bin"
    lemm = sllematizer.RdrLemmatizer(dic, lib)
    return lemm

def load_locations():
    known_locations = []
    f = open("tuja_imena.txt", "rb")
    for line in f:
        line = line.decode("utf-8").strip()
        words = line.split()
        known_locations.extend(words)

    lemmatizer = get_lemmatizer()
    known_locations = [lemmatizer.lemmatize(word).lower() for word in known_locations]
    return set(known_locations)

def load_names():
    names = []
    lemmatizer = get_lemmatizer()

    f = open("imena.txt", "rb")
    for line in f:
        line = line.decode("utf-8").strip()
        line = lemmatizer.lemmatize(line)
        names.append(line.lower())
    f.close()

    f = open("priimki.txt", "rb")
    for line in f:
        line = line.decode("utf-8").strip()
        line = lemmatizer.lemmatize(line)
        names.append(line.lower())
    f.close()

    return set(names)

f_path = sys.argv[1]
print "Opening file", f_path

stopwords = get_stopwords()
known_locations = load_locations()
known_names = load_names()

in_file = open(f_path, "rb")
out_file = open("tagged.txt", "wb")

lemmatizer = get_lemmatizer()

for line in in_file:
    lines += 1

    line = line.decode("utf-8").strip()
    cls = "O"

    if is_line_candidate(line):
       if line.lower() not in stopwords and \
          len(line) > 3 and \
          line.lower() not in exceptions:
         

           line_lem = lemmatizer.lemmatize(line)
           candidates += 1

           if line_lem.lower() in known_names:
              cls = "PERSON"
              names += 1
           # Check if it's a know location
           elif line_lem.lower() in known_locations:
              cls = "LOC"
              locations += 1
    out_file.write("%s\t%s\n" % (line.encode("utf-8"), cls,))

out_file.close()

print "Lines", lines, "Candidates", candidates
print "Locations", locations, "Names", names
