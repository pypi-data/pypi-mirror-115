'''
Usage: python3 collect_tags_xigt.py xigt_file.xml pos_tier_id gloss_tier_ids

E.g.:

python3 ../sample_data/eng.xml pos g

This will simply collect all grams from the tiers that correspond to the supplied tier ids (e.g. pos and g) and output
two files: pos-tags.txt and glosses.txt. These files can then be copied somewhere safe and then the path to them
should be given to MOM in the config file: pos-tags.txt should be divided into verb tags and noun/pronoun tags (two
separate files). glosses.txt should be filtered to only contain glosses (as opposed to stem translations).

Note: Again, you need to *MANUALLY* delete everything you don't want in those files. But it isn't too bad: it usually
only takes a few minutes per dataset. True grams tend to gravitate to the top generally and to the top of each letter
of the alphabet.
'''

import sys
from xigt.codecs import xigtxml
from FeatDict import FeatureDictionary

class TagCollector():
    def __init__(self,xigt_file,pos_tier_id,gloss_tier_ids):
        self.xigt_file = xigt_file
        self.pos_tier_id = pos_tier_id
        self.gloss_tier_ids = gloss_tier_ids

    def collect_tags(self):
        self.pos_tags = set()
        self.glosses = set()
        with open(self.xigt_file, encoding='utf-8') as file:
            xc = xigtxml.load(file)
        for igt in xc:
            pos_tier = igt.get(self.pos_tier_id)
            if pos_tier:
                for item in pos_tier:
                    if item.value():
                        self.pos_tags.add(item.value())
            for g_id in self.gloss_tier_ids:
                gl_tier = igt.get(g_id)
                if gl_tier:
                    for item in gl_tier:
                        if item.value():
                            self.glosses.add(item.value())

    def write_tags_to_file(self, filename,tags):
        with open(filename, 'w', encoding='utf8') as of:
            for t in sorted(list(tags)):
                of.write(t+'\n')


    def check_for_standard_glosses(self):
        fd = FeatureDictionary()
        unknown_features = set()
        for g in self.glosses:
            for gram in g.strip('-=').split('.'):
                if (not gram.lower() in fd.all_keys):
                        unknown_features.add(gram)
        with open('unknown_features.txt', 'w', encoding='utf8') as f:
            for feat in sorted(list(unknown_features)):
                f.write(feat + '\n')
        print('The following glosses could not be mapped to anything in the Feature Dictionary:')
        print(';'.join(sorted(list(unknown_features))))
        print('If there are not just stems but also glosses for morphosyntactic features among them, '
              'consider adding the lower case version of them to the appropriate part '
              'of the Feature Dictionary. Look in unknown_features.txt')

def main():
    tc = TagCollector(sys.argv[1],sys.argv[2],sys.argv[3].split(','))
    tc.collect_tags()
    tc.write_tags_to_file('pos_tags.txt',tc.pos_tags)
    tc.write_tags_to_file('glosses.txt',tc.glosses)
    tc.check_for_standard_glosses()

if __name__ == '__main__':
    main()
