import sys
from xigt.codecs import xigtxml


xigt_file = sys.argv[1]
word = sys.argv[2]

pos_tags = set()
glosses = set()

with open(xigt_file, encoding='utf-8') as file:
    xc = xigtxml.load(file)

for igt in xc:
    if igt.get('m'):
        for item in igt.get('m'):
            if item.value() == word:
