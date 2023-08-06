import os, sys
import re
import copy

class MorphTypeGuesser:
    def __init__(self, known_glosses_file):
        if known_glosses_file:
            with open(known_glosses_file, 'r') as f:
                glosses = [ g.strip() for g in f.readlines() ]
        else:
            glosses = set()
        self.known_glosses = set(glosses)


    def infer_morph_type_with_boundary(self, orth):
        if orth == '-' or orth == '=':
            return 'COMPOUND_TOK'
        if orth.startswith('-'):
            return 'suffix'
        if orth.endswith('-'):
            return 'prefix'
        if orth.startswith('='):
            return 'enclitic'
        if orth.endswith('='):
            return 'proclitic'
        else:
            return('root') #note: this only works for good segmentation, e.g not for Russian ODIN

    def infer_morph_type_without_boundary(self, morphemes_glosses):
        new_morphemes_glosses = []
        idx = 0
        last_root = 999
        root_indices = []
        for (m,g) in morphemes_glosses:
            new_m = copy.copy(m)
            # First see if a morpheme is clearly a gloss
            for g_i in g:
                if g_i.value() in self.known_glosses:
                    if idx < last_root:
                        new_m.type = 'prefix'
                        break
                    else:
                        new_m.type = 'suffix'
                        break
                else:
                    new_m.type = 'root'
                    last_root = idx
                    root_indices.append(idx)
                    break
            new_morphemes_glosses.append((new_m,g))
            idx += 1
        return new_morphemes_glosses, root_indices
