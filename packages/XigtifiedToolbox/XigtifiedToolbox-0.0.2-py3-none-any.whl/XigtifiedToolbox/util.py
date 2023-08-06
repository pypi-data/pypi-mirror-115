import sys
from xigt.codecs import xigtxml

def fetch_igts(xc,igt_ids):
    subset = []
    for id in igt_ids:
        subset.append(xc[id])
    subset_xc = xigtxml.XigtCorpus(igts=subset)
    xigtxml.dump('debug.xml',subset_xc)

def split_igts(xc, percent):
    subset = []
    #for i,igt in enumerate(xc):
    #    if i > len(xc)*percent:
    #        break
    #    subset.append(igt)
    subset = xc[:int(len(xc)*percent)]
    subset_xc = xigtxml.XigtCorpus(igts=subset)
    xigtxml.dump('debug.xml',subset_xc)


def unique_id(toolbox_file, reftag):
    map = {}
    new_toolbox_lines = []
    with open(toolbox_file,'r') as f:
        lines = f.readlines()
    for ln in [l.strip() for l in lines]:
        if ln.startswith(reftag):
            if not ln in map:
                map[ln] = []
            n = len(map[ln])
            if n == 0:
                map[ln].append(ln)
                new_toolbox_lines.append(ln)
            else:
                newln = ln + '-' + str(n)
                map[ln].append(newln)
                new_toolbox_lines.append(newln)
        else:
            new_toolbox_lines.append(ln)
    with open('uniq.txt','w') as f:
        for ln in new_toolbox_lines:
            f.write(ln + '\n')
    with open('map.txt','w') as f:
        f.write('The following non-unique \\ref entries were replaced by unique ids:\n')
        for k in map:
            if len(map[k]) > 1:
                for v in map[k]:
                    f.write(k + ':\t' + v + '\n')

def all_tags_for_word(word, xc):
    attested_tags = set()
    count = 0
    for igt in xc:
        pos_tier = igt.get('pos') if igt.get('pos') else igt.get('w-pos')
        if not pos_tier:
            pos_tier = igt.get('gw-pos')
        aligned_tier = pos_tier.alignment
        for item in pos_tier:
            relevant_word = igt.get_item(item.alignment)
            if relevant_word.value() == word:
                count += 1
                attested_tags.add(item.text)
    with open('attested_tags.txt', 'w') as f:
        f.write(word + ': ' + 'count=' + str(count) + '\n')
        for tag in attested_tags:
            f.write(tag + '\n')







if __name__ == '__main__':
    print('Uncomment/add whatever you want it to do.')
    #unique_id(sys.argv[1], sys.argv[2])
    #with open(sys.argv[1], 'r') as f:
    #    xc = xigtxml.load(f)
    #split_igts(xc,0.25)
    #all_tags_for_word('akka',xc)