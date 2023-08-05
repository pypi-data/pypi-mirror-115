import sys

toolbox_file = sys.argv[1]
identifier = sys.argv[2]


pos_tags = set()

with open(toolbox_file,'r') as tf:
    lines = tf.readlines()

for ln in lines:
    if ln.startswith('\\' + identifier):
        tags = ln.split()
        for t in tags:
            pos_tags.add(t)

with open(identifier + '-tags.txt', 'w') as of:
    for t in sorted(list(pos_tags)):
        of.write(t+'\n')