#/usr/bin/env python

# This loads random articles from article SQLite database and saves words into a text file line-by-line

import sqlite3
import string

COUNT = 5000        # Number of articles to select


print "Reading database..."
connection = sqlite3.connect("articles.db")
cursor = connection.cursor()
cursor.execute("SELECT text FROM articles ORDER BY RANDOM() LIMIT %d;" % COUNT)

texts = [row[0] for row in cursor.fetchall()]
cursor.close()

print "Cleaning up text..."
text = ' '.join(texts)
# Remove all punctuation from text
punctuation_table = dict((ord(char), None) for char in string.punctuation)
text = text.translate(punctuation_table)
# Split by words

print "Writing output..."
f = open("words.txt", "wb")
for word in text.split():
    f.write("%s\n" % word.encode("utf-8"))
f.close()

print "Done."
