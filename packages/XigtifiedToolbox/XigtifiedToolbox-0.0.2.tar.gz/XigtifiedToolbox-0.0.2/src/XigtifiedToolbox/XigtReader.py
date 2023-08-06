import os
import re
import sys

import editdistance
from xigt import xigtpath as xp
from xigt.codecs import xigtxml
parent_dir = os.path.join(os.getcwd(),os.pardir)
sys.path.append(parent_dir)
from . import MorphTypeGuesser, FeatDict

ROOTS = {'root','stem','bound_root','bound root'}

class Xigt_Reader:
    def __init__(self, settings, verbose=False):
        self.settings = settings
        self.verb_tags = settings.verb_tags
        self.noun_tags = settings.noun_tags
        self.patterns = settings.patterns
        self.use_gloss_for_patterns = settings.use_gloss_to_precluster
        self.hyphens = settings.hyphens
        self.full_xc = None
        self.xc = []
        self.igt2items = {}
        self.items = {}
        self.items['verb'] = []
        self.items['noun'] = []
        self.ignore_igt = settings.ignore_igt
        self.ignore_chars = settings.ignore_chars
        self.verbose = verbose
        self.allowed_diff = settings.allowed_diff
        self.allomorphs = settings.allomorphs
        self.ungrammatical = settings.ungrammatical
        self.mtg = MorphTypeGuesser.MorphTypeGuesser(settings.known_glosses_file)
        self.lexitem_classes = settings.lexitem_classes
        self.assume_morph_boundaries = settings.assume_morph_boundaries
        self.all_bare = settings.all_bare
        self.skipped_igt = {} # id : reason
        self.skipped_words = {}

    def process_igts(self, file_name):
        print("Using file " + file_name)
        with open(file_name, encoding='utf-8') as file:
            xc = xigtxml.load(file)
            self.full_xc = xc
        print ("Processing Xigt IGTs...")
        (count,skipped, pos_words) = self.construct_pos_items(xc,self.verb_tags,self.noun_tags)
        print("Skipped {0} out of {1} words due to morpheme-to-gloss alignment issues. "
              "Look in output/skipped_items.txt".format(skipped,count))
        for pos in pos_words:
            self.items[pos] = sorted(pos_words[pos], key=lambda x: x.tokenized_text)
        self.igt2items = map_igt2words(self)

    def print_skipped(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write('SKIPPED WORDS:\n')
            for igt_id in self.skipped_words:
                if len(self.skipped_words[igt_id]) > 0:
                    f.write(igt_id + '\t')
                    for wd_id in self.skipped_words[igt_id]:
                        f.write(wd_id + '\t' + self.skipped_words[igt_id][wd_id] + '\n')
            f.write('SKIPPED IGT:\n')
            for igt_id in self.skipped_igt:
                f.write(igt_id + '\t' + self.skipped_igt[igt_id] + '\n')

    def collect_relevant_word_ids(self, xc, verb_tags,noun_tags):
        igt_to_word_ids = {}
        igt_to_word_ids['verb'] = {}
        igt_to_word_ids['noun'] = {}
        igt_count = 0
        igt_skipped = 0
        empty = 0
        for igt in xc:
            igt_count += 1
            igt_to_word_ids['verb'][igt.id] = []
            igt_to_word_ids['noun'][igt.id] = []
            self.skipped_words[igt.id] = {} # position : reason
            if not igt.get('p'):
                empty += 1
                self.skipped_igt[igt.id] = 'empty'
                if self.verbose:
                    print("Skipping empty IGT {0}".format(igt.id))
                continue
            if igt.get('p')[0].value() in self.ignore_igt:
                empty += 1
                self.skipped_igt[igt.id] = 'empty'
                if self.verbose:
                    print("Skipping empty IGT {0}".format(igt.id))
                continue
            else:
                self.normalize_text(igt)
                self.xc.append(igt)
            # extract all words from the corpus which have the right pos tag and seem part of natural dialog
            pos_tier = igt.get('pos') if igt.get('pos') else igt.get('w-pos')
            if not pos_tier:
                pos_tier = igt.get('m-pos')
            if not pos_tier:
                pos_tier = igt.get('gw-pos')
            if not pos_tier:
                pos_tier = igt.get('x')
            if not pos_tier:
                self.skipped_igt[igt.id] = 'no POS tier'
                if self.verbose:
                    print("No POS tier in IGT #{0} ({1}) skipping it".format(igt_count,igt.id))
                igt_skipped +=1
                continue
            else:
                aligned_tier = pos_tier.alignment
                if aligned_tier == 'w':
                    for item in pos_tier:
                        if item.text in verb_tags:
                            igt_to_word_ids['verb'][igt.id].append(item.alignment)
                        elif item.text in noun_tags:
                            igt_to_word_ids['noun'][igt.id].append(item.alignment)
                # KPH added to get alignment when gw-pos alignes to gw
                elif aligned_tier == 'gw':
                    for item in pos_tier:
                        if item.text in verb_tags:
                            aligned_word = igt.get('gw').get(item.alignment).alignment
                            igt_to_word_ids['verb'][igt.id].append(aligned_word)
                        elif item.text in noun_tags:
                            aligned_word = igt.get('gw').get(item.alignment).alignment
                            igt_to_word_ids['noun'][igt.id].append(aligned_word)
                elif aligned_tier == 'm':
                    tagged_words = {}# KPH we want to make sure that the same word isn't added multiple times, so we'll collect the words each tag points to and add them to igt_to_words at the end
                    for item in pos_tier:
                        if item.text in verb_tags or item.text in noun_tags:
                            relevant_word_id = igt.get_item(item.alignment).alignment
                            if not relevant_word_id:
                                relevant_word_id = igt.get_item(item.alignment).segmentation
                            if not relevant_word_id:
                                if self.verbose:
                                    print('Unexpected alignment structure: pos tier not '
                                                'aligned to either morphemes or words. '
                                      'Skipping IGT #{0} ({1})'.format(igt_count,igt.id))
                                igt_skipped += 1
                                self.skipped_igt[igt.id] = 'misalignment'
                                continue
                            if item.text in verb_tags:
                                if relevant_word_id in tagged_words:
                                    if 'verb' in tagged_words[relevant_word_id]:
                                        tagged_words[relevant_word_id]['verb'].append(item.alignment)
                                    else:
                                        tagged_words[relevant_word_id]['verb'] = [item.alignment]
                                else:
                                    tagged_words[relevant_word_id] = {'verb': [item.alignment]}
                                # if not relevant_word_id in igt_to_word_ids['verb'][igt.id]:
                                #     igt_to_word_ids['verb'][igt.id].append(relevant_word_id)
                            if item.text in noun_tags:
                                if relevant_word_id in tagged_words:
                                    if 'noun' in tagged_words[relevant_word_id]:
                                        tagged_words[relevant_word_id]['noun'].append(item.alignment)
                                    else:
                                        tagged_words[relevant_word_id]['noun'] = [item.alignment]
                                else:
                                    tagged_words[relevant_word_id] = {'noun': [item.alignment]}
                                    # if not relevant_word_id in igt_to_word_ids['noun'][igt.id]:
                                    #     igt_to_word_ids['noun'][igt.id].append(relevant_word_id)
                    for word_id in tagged_words:
                        if 'verb' in tagged_words[word_id] and 'noun' not in tagged_words[word_id]:
                            igt_to_word_ids['verb'][igt.id].append(word_id)
                        elif 'noun' in tagged_words[word_id] and 'verb' not in tagged_words[word_id]:
                            igt_to_word_ids['noun'][igt.id].append(word_id)
                        elif 'verb' in tagged_words[word_id] and 'noun' in tagged_words[word_id]:
                            # KPH if either morpheme is the root, we want to go with that pos. otherwise, we'll default to verb
                            roots = []
                            for pos in ['verb', 'noun']:
                                for morph_id in tagged_words[word_id][pos]:
                                    if self.assume_morph_boundaries:
                                        type = self.mtg.infer_morph_type_with_boundary(igt.get('m').get(morph_id).value())
                                    else:
                                        gloss_id = ''
                                        for g in igt.get('g'):
                                            if g.alignment == morph_id:
                                                gloss_id = g.id
                                        morpheme_glosses, root_indices = self.mtg.infer_morph_type_without_boundary([(igt.get('m').get(morph_id), [igt.get('g').get(gloss_id)])])
                                        if root_indices != []:
                                            type = 'root'
                                        else:
                                            type = ''
                                    if type == 'root':
                                        roots.append(pos)
                            if 'verb' in roots and 'noun' not in roots:
                                igt_to_word_ids['verb'][igt.id].append(word_id)
                            elif 'noun' in roots and 'verb' not in roots:
                                igt_to_word_ids['noun'][igt.id].append(word_id)
                            else:
                                igt_to_word_ids['verb'][igt.id].append(word_id)

                else:
                    if self.verbose:
                        print('Unexpected alignment structure: pos tier not '
                                    'aligned to either morphemes or words. '
                          'Skipping IGT #{0} ({1})'.format(igt_count,igt.id))
                    igt_skipped += 1
                    self.skipped_igt[igt.id] = 'misalignment'
                    continue
        return (igt_count, igt_skipped, igt_to_word_ids)


    def normalize_text(self,igt):
        if igt.get('m'):
            for m in igt.get('m'):
                m.text = m.value().lower().rstrip(self.ignore_chars)
                m.text = m.text.lstrip(self.ignore_chars)
        if igt.get('w'):
            for w in igt.get('w'):
                w.text = w.value().lower().rstrip(self.ignore_chars)
                w.text = w.text.lstrip(self.ignore_chars)

    def construct_pos_items(self,xc,verb_tags,noun_tags):
        words_count = 0
        words_skipped = 0
        pos_words = {}
        pos_words['verb'] = []
        pos_words['noun'] = []
        (igt_count, igt_skipped, igt_to_word_ids) = self.collect_relevant_word_ids(xc,verb_tags,noun_tags)
        for pos_tag in ['verb','noun']:
            for igt_id in igt_to_word_ids[pos_tag]:
                igt = xc.get(igt_id)
                word_to_morphs = {}
                this_igt_words = []
                success = True
                try:
                    for word_id in igt_to_word_ids[pos_tag][igt_id]:
                        word_to_morphs[word_id] = []
                        if igt.get('m'):
                            morphemes = xp.findall(igt, 'tier[@type="morphemes"]/item[referent()/@id='+word_id+']')
                            if len(morphemes) == 0:
                                if self.verbose:
                                    print('Morphemes are not aligned to a word in IGT {0}'.format(igt_id))
                                success = False
                            string = ''.join([i.value() for i in morphemes if i.value()]).strip(',.!?-=_')
                            if ''.join([i.value() for i in morphemes if i.value()]).strip(',.!?') == '':
                                if self.verbose:
                                    print('Word is the empty string or only contains punctuation'.format(igt_id))
                                    success = False
                            for m in morphemes:
                                aligned_glosses = self.find_aligned_glosses(m.id,igt)
                                if len(aligned_glosses) == 0:
                                    success = False
                                    if self.verbose:
                                        print('Morphemes are not aligned to glosses in IGT {0} word {1}'.format(igt_id, word_id))
                                    continue
                                else:
                                    word_to_morphs[word_id].append((m,aligned_glosses))
                    for wd_id in word_to_morphs:
                        if len(word_to_morphs[wd_id]) == 0:
                            words_count += 1
                            words_skipped += 1
                            if self.verbose:
                                print('w{0}, igt {1}'.format(wd_id, igt.id) + '\t' + 'No gloss')
                            self.skipped_words[igt.id][wd_id + '\t' + igt.get_item(word_id).value()] = 'No gloss'
                            continue

                        # ECC: place a check before creating a POS_Word object
                        # don't include words with "mixed morphemes" (those with affixes that are both verby and nouny)
                        # attempts to prevent mis-tagging words
                        # for example a verb w/ a nominalizer affix may be marked as a noun, even though it's a verb
                        if self.has_mixed_morphemes(pos_tag, word_to_morphs[wd_id]):
                            continue


                        pos_word = POS_Word(word_id=wd_id, igt=igt,
                                            morphemes_glosses=word_to_morphs[wd_id],
                                            patterns=self.patterns, mtg=self.mtg, hyphens=self.hyphens,
                                            lexitem_classes=self.lexitem_classes,
                                            assume_morph_boundaries = self.assume_morph_boundaries,
                                            all_bare=self.all_bare, use_gloss_for_patterns=self.use_gloss_for_patterns)
                        (text_matches, error) = pos_word.check_text(self.allowed_diff,self.allomorphs)
                        if not text_matches or pos_word.misaligned:
                            words_count += 1
                            words_skipped += 1
                            if error == 'Success':
                                error = 'misalignment'
                            if self.verbose:
                                print('{0}'.format(igt.id) + '\t' + error)
                            self.skipped_words[igt.id][wd_id + '\t' + pos_word.parent_word.value()] = error
                            continue
                        if pos_word.tokenized_text[0] in self.ungrammatical:
                            words_count += 1
                            words_skipped += 1
                        else:
                            try:
                                words = self.analyze_compound(pos_word)
                                for w in words:
                                    words_count += 1
                                    (valid_word, error) = w.validate()
                                    if not valid_word:
                                        words_skipped += 1
                                        if self.verbose:
                                            print(error + ' in word {0} in igt {1}; Skipping it'.format(wd_id,igt.id))
                                        self.skipped_words[igt.id][w.parent_word.id + '\t' + w.parent_word.value()] = error
                                    else:
                                        this_igt_words.append(w)
                            except:
                                if self.verbose:
                                    print("Possible misalignment in igt {0}".format(igt.id))
                                    error = 'misalignment'
                                    self.skipped_words[igt.id][w.parent_word.id + '\t' + w.parent_word.value()] = error
                                    raise Exception('Misalignment in igt {0}'.format(igt.id))
                    if success:
                        pos_words[pos_tag].extend(this_igt_words)
                except:
                    igt_skipped += 1
                    self.skipped_igt[igt.id] = 'misalignment'
        print('Skipped {0} out of {1} IGT. '
              'Look in output/skipped_items.txt for reason codes.'.format(igt_skipped,igt_count))
        return(words_count,words_skipped,pos_words)

    def analyze_compound(self,word):
        if not word.has_compound_tok:
            return [word]
        parts = []
        start = 0
        end = len(word.morphemes)
        for idx in word.compound_tok_indices:
            morphs = word.morphemes[start:idx]
            new_wd = POS_Word(word_id=word.original_id, igt=word.parent_igt, morphemes=morphs, mtg=self.mtg,
                              hyphens=self.hyphens,
                              lexitem_classes=self.lexitem_classes,
                              patterns=self.patterns,
                              assume_morph_boundaries = self.assume_morph_boundaries,
                              all_bare=self.all_bare, use_gloss_for_patterns=self.use_gloss_for_patterns)
            parts.append(new_wd)
            start = idx+1
        if start < end:
            morphs = word.morphemes[start:end]
            last_wd = POS_Word(word_id=word.original_id, igt=word.parent_igt, morphemes=morphs, mtg=self.mtg,
                               hyphens=self.hyphens,
                               patterns=self.patterns,
                               lexitem_classes=self.lexitem_classes,
                               assume_morph_boundaries = self.assume_morph_boundaries,
                               all_bare=self.all_bare, use_gloss_for_patterns=self.use_gloss_for_patterns)
            parts.append(last_wd)
        return parts

    def find_aligned_glosses(self,m_id, igt):
        aligned_glosses = []
        gloss_tier = igt.get('g')
        word_lvl_gloss_tier = igt.get('wt')
        if self.settings.implicitg2morph:
            g_id = 'g' + re.search('([0-9]+\.[0-9]+)',m_id).group(1)
            if igt.get_item(g_id).value() is None:
                w_id = 'w' + re.search('([0-9]+)',m_id).group(1)
                for wt in word_lvl_gloss_tier:
                    if wt.alignment == w_id:
                        aligned_glosses.append(wt)
            else:
                aligned_glosses.append(igt.get_item(g_id))
        else:
            for item in gloss_tier:
                if item.alignment == m_id:
                    aligned_glosses.append(item)
        return aligned_glosses

    def has_mixed_morphemes(self, pos_tag, morphemes):
        """
        Check to see if the list of morphemes has a mixture of 'verby' and 'nouny' morphemes

        :param pos_tag: the tag this word was already marked as
        :type pos_tag: str
        :param morphemes: the list of morphemes to check
        :type morphemes: list
        :return: whether the morphemes were mixed
        :rtype: bool
        """
        noun_glosses = FeatDict.collect_nouny_keys()
        verb_glosses = FeatDict.collect_verby_keys()

        # the word has already been marked, so set the appropriate flag
        # if the word is believed to be a noun, and we later find a verby morpheme, it should be thrown out
        if pos_tag == 'noun':
            noun_flag = True
            verb_flag = False
        elif pos_tag == 'verb':
            noun_flag = False
            verb_flag = True

        for m in morphemes:
            # split in case of a compound gloss, e.g. PST.IMP
            morph_glosses = re.split('\.|-|=', m[1][0].text.lower())

            for gloss in morph_glosses:
                if gloss in noun_glosses:
                    noun_flag = True
                elif gloss in verb_glosses:
                    verb_flag = True
                else:
                    # morpheme gloss was ambiguous, ignore it
                    continue

                if noun_flag and verb_flag:
                    # a mixture has been encountered, so the word has mixed morphemes
                    return True

        return False




class POS_Word:
    def __init__(self, word_id, igt, mtg, morphemes_glosses=None, patterns=None,
                 morphemes=None, hyphens=True, lexitem_classes=False,
                 all_bare=True, assume_morph_boundaries = True,use_gloss_for_patterns=True):
        self.original_id = word_id
        self.hyphens = hyphens
        self.misaligned = False
        self.parent_word = igt.get_item(word_id)
        self.parent_igt = igt
        self.root = None
        self.prefixes = []
        self.suffixes = []
        self.all_roots = []
        self.no_known_affix = True
        self.has_compound_tok = False
        self.compound_tok_indices = []
        self.tokenized_text = ''
        self.word_text = self.parent_word.value()
        self.is_compound = False
        self.assume_morph_boundaries = assume_morph_boundaries
        self.case_frame = {}
        self.transitivity = None
        if morphemes_glosses:
            self.morphemes = []
            i=0
            prev_tok = None
            if not assume_morph_boundaries:
                morphemes_glosses, root_indices = mtg.infer_morph_type_without_boundary(morphemes_glosses)
            for (m,g) in morphemes_glosses:
                txt = m.text if m.text else m.value()
                #TODO data-specific(? Abui) compound treatment
                tok = Word_Token(xigt_morph=m,glosses=g, patterns=patterns,real_token=True,mtg=mtg,parent_word=self,
                                 use_gloss=use_gloss_for_patterns)
                if not txt.endswith('-') and not txt.startswith('-') and '-' in txt:
                    tok.orth = re.sub('-','~~~',txt)
                self.tokenized_text += tok.orth
                if self.detect_misalignment(i=i,tok=tok, morphemes_glosses=morphemes_glosses,prev_tok=prev_tok):
                    self.misaligned = True
                    return
                if tok.type in ROOTS:
                    self.root = tok
                    self.all_roots.append(tok)
                if prev_tok:
                    #TODO data-specific(? Abui) compound treatment
                    if self.implicit_compounding(tok, prev_tok):
                        self.is_compound = True
                        ct = Word_Token(xigt_morph=None,glosses=['~'],patterns=None,
                                        real_token=False,fake_type='CMP',mtg=mtg,parent_word=self,
                                        use_gloss=use_gloss_for_patterns)
                        self.morphemes.append(ct)
                        self.has_compound_tok = True
                        self.compound_tok_indices.append(i)
                        i += 1
                    if (prev_tok.type == 'prefix' or prev_tok.type == 'proclitic') and tok.type == 'enclitic':
                        self.root = tok
                        tok.type = 'root'
                if tok.type == 'COMPOUND_TOK':
                    self.has_compound_tok = True
                    self.is_compound = True
                    self.compound_tok_indices.append(i)
                self.morphemes.append(tok)
                i += 1
                prev_tok = tok
            if not assume_morph_boundaries:
                for i in root_indices:
                    self.root = self.morphemes[i] #TODO: this only takes one root
                    self.all_roots.append(self.morphemes[i])
        else:
            if morphemes:
                self.morphemes = morphemes
                for tok in morphemes:
                    if tok.real_token:
                        self.tokenized_text += tok.orth
                    if tok.type in ROOTS:
                        self.root = tok
            #else:
            #    root_tok = Word_Token(xigt_morph=None,glosses=None, patterns=None,real_token=True,mtg=None,parent_word=self)
            #    self.morphemes = [root_tok]
            #    self.root = root_tok
            #    self.all_roots.append(root_tok)
        if self.root:
            if len(self.morphemes) > 1 and not (self.is_compound or self.has_compound_tok):
                self.ordered_morphemes = self.order_morphs(True)
            else:
                self.ordered_morphemes = list(self.morphemes)
        else:
            raise Exception("No root found in word {0} in IGT {1}".format(self.original_id, self.parent_igt.id))

        # This is currently Abui-specific. I added a "all_bare" setting
        # to choose whether to use the EMPTY- prefix or not, however,
        # the implementation does not pay attention to suffixes and so is inadequate for the name:
        # it really only shows that a stem occurs without a prefix.
        # It really should look at whether the stem is indeed bare.
        if lexitem_classes:
            if len(self.morphemes) > 1 \
                    and not self.misaligned \
                    and not (self.is_compound or self.has_compound_tok):
                try:
                    first_tok = self.ordered_morphemes[1]
                except:
                    print(self.word_text + ' ' + self.parent_igt.id)
                    raise Exception('No ordered morphemes!')
                #TODO Abui-specific(?)
                if first_tok.type == 'prefix' and first_tok.known_affix_type:
                    self.no_known_affix = False
            #TODO Abui-specific(?)
            if not all_bare:
                if self.no_known_affix and not self.misaligned and not (self.is_compound or self.has_compound_tok):
                    empty_prefix = Word_Token(xigt_morph=None,glosses=[],
                                              patterns=None,real_token=False,fake_type='DUMMY',mtg=mtg,parent_word=self,
                                              use_gloss=use_gloss_for_patterns)
                    self.morphemes.append(empty_prefix)
                    try:
                        self.ordered_morphemes.insert(self.ordered_morphemes.index(self.root)+1,empty_prefix)
                    except:
                        print(self.word_text + ' ' + self.parent_igt.id)
                        raise Exception('No ordered morphemes')

    def detect_misalignment(self,i,tok,morphemes_glosses,prev_tok=None):
        if (i == 0 and (tok.type == 'suffix' or tok.type == 'enclitic')):
            return True
        if (i == len(morphemes_glosses) - 1 and (tok.type == 'prefix' or tok.type == 'proclitic')):
            return True
        if prev_tok:
            if (prev_tok.type == 'prefix' or prev_tok.type == 'proclitic'):
                if tok.type == 'COMPOUND_TOK' or tok.type == 'suffix' or tok.type == 'enclitic':
                    return True
        return False


    def implicit_compounding(self, tok, prev_tok):
        if tok.type in ROOTS and prev_tok.type in ROOTS:
            return True
        if tok.type in ROOTS or tok.type == 'prefix' or tok.type == 'proclitic':
            if (prev_tok.type == 'suffix' or prev_tok.type == 'enclitic'):
                return True
        if (tok.type == 'prefix' or tok.type == 'proclitic'):
            if (prev_tok.type in ROOTS or prev_tok.type == 'suffix' or prev_tok.type == 'enclitic'):
                return True
        return False

    def __str__(self):
        return self.tokenized_text

    def __repr__(self):
        return self.tokenized_text

    def check_text(self, allowed_diff,allomorphs):
        reconstructed_text = re.sub('[-=\?\.\!\,\:\;\(\)\'\"\`#]','',self.tokenized_text.lower())
        phrase_text = re.sub('[-=\?\.\!\,\:\;\(\)\'\"\`#]','',self.word_text.lower())
        ed = editdistance.eval(reconstructed_text,phrase_text)
        if ed > allowed_diff \
                and not self.known_phon_diff(phrase_text,reconstructed_text,allomorphs) \
                and not self.is_compound_spelling(phrase_text,reconstructed_text):
            return(False, 'Possible misalignment: {0} aligned to {1}'.format(phrase_text,reconstructed_text))
        return (True, 'Success')

    # Is the only difference the ~ character (compound spelling)?
    def is_compound_spelling(self,str1,str2):
        diff = set(str2).difference(set(str1))
        return len(diff) == 1 and '~' in diff

    def known_phon_diff(self, str1, str2, allomorphs):
        for p in allomorphs:
            if p[2] == 0:
                if str1.startswith(p[0]) and str2.startswith(p[1]):
                    return True
            elif p[2] == -1:
                if str1.endswith(p[0]) and str2.endswith(p[1]):
                    return True
            elif p[2] == 2:
                if p[0] in str1 or p[0] in str2:
                    return True
            else:
                if str1 == p[0] and str2 == p[1]:
                    return True
        return False

    def validate(self):
        if not self.root:
            return (False, 'No root')
        for m in self.morphemes:
            if not m.orth:
                return (False, 'No orth')
            if len(m.glosses) == 0:
                return (False, 'No gloss')
        return (True, 'Success')

    def order_morphs(self, prefixes_first):
        ordered = []
        ordered.append(self.root)
        prefixes = []
        suffixes = []
        idx = self.morphemes.index(self.root)
        left_tokens = self.morphemes[0:idx]
        right_tokens = self.morphemes[idx+1:]
        for tok in left_tokens:
            if tok.real_token or tok.known_affix_type == 'empty-': #TODO: Abui-specific?
                prefixes.append(tok)
        for tok in right_tokens:
            if tok.real_token:
                suffixes.append(tok)
        prefixes.reverse()
        self.prefixes = prefixes
        self.suffixes = suffixes
        for i,p in enumerate(prefixes):
            p.position = i+1
        for i,s in enumerate(suffixes):
            s.position = i+1
        if prefixes_first:
            ordered.extend(prefixes)
            ordered.extend(suffixes)
        else:
            ordered.extend(suffixes)
            ordered.extend(prefixes)
        return ordered

class Word_Token:
    def __init__(self, xigt_morph, glosses, patterns, real_token, mtg, parent_word, fake_type=None,use_gloss=True):
        # TODO: this probably should not be part of Word_Token instances; it is confusing later
        self.known_glosses = mtg.known_glosses
        if not real_token:
            self.real_token = False
            if fake_type == 'DUMMY': #TODO: The below is Abui-specific(?)
                self.type = 'prefix'
                self.known_affix_type = 'empty-'
                self.orth = 'EMPTY-'
                self.glosses = ['EMPTY-']
                self.is_known = True
                parent_word.no_known_affix = False
            if fake_type == 'CMP':
                self.type = 'COMPOUND_TOK'
                self.known_affix_type = None
                self.glosses = ['~']
                self.orth = '~'
                self.is_known = False
            self.features = []
            self.mom_features = []
        else:
            self.type = None
            morph_text = xigt_morph.text if xigt_morph.text else xigt_morph.value()
            self.real_token = True
            if xigt_morph.type:
                self.type = xigt_morph.type.lower()
                if self.type in ROOTS:
                    self.type = 'root'
            elif parent_word.assume_morph_boundaries:
                self.type = mtg.infer_morph_type_with_boundary(morph_text)
            if self.type and self.type == 'COMPOUND_TOK':
                self.real_token = False
            self.orth = morph_text
            self.glosses = [g.value() for g in glosses]
            if parent_word.hyphens:
                insert_hyphens(self)
            self.features = []
            self.mom_features = []
            if self.type:
                self.features = self.infer_features(self.glosses)
            self.known_affix_type = self.infer_known_type(patterns,use_gloss=use_gloss)
            self.is_known = self.known_affix_type is not None
            #else:
            #    self.type = 'root'
            #    morph_text = parent_word.parent_igt.get_item(parent_word.original_id).value()
            #    gw_id = 'gw' + re.search('([0-9]+)',parent_word.original_id).group(1)
            #    self.orth = morph_text
            #    alignment = parent_word.parent_igt.get_item(gw_id).content
            #    self.glosses = [parent_word.parent_igt.get_item(gw_id)]


    def __str__(self):
        return self.orth

    def __repr__(self):
        return self.orth

    def infer_features(self, glosses):
        feature_grams = []
        for g in glosses:
            grams = re.split('\.| ',g)
            for gr in grams:
                #if gr.strip('-=') in self.known_glosses:
                if g in self.known_glosses or g.strip('-=') in self.known_glosses:
                    feature_grams.append(gr.strip('-=()+;,/').lower())#KPH removing some extra punctuation so these will match features
        return feature_grams

    def infer_known_type(self, patterns, use_gloss=True):
        precluster_strings = [self.orth] if not use_gloss else self.glosses
        if self.type in ROOTS or patterns==None:
            return None
        for p in patterns:
            for s in precluster_strings:
                match = re.search(p,s)
                if match:
                    if not p == '.+':
                        return p
                    else:
                        return s


def map_igt2words(xigt_reader):
    map = {}
    for pos in xigt_reader.items:
        for item in xigt_reader.items[pos]:
            if not item.parent_igt.id in map:
                map[item.parent_igt.id] = {}
            map[item.parent_igt.id][item.original_id] = item
    return map


def insert_hyphens(m):
    if not m.type:
        return m
    if m.type == 'prefix' and not m.orth.endswith('-'):
        m = add_hyphen(m,'end','-')
    elif m.type == 'proclitic' and not m.orth.endswith('='):
        m = add_hyphen(m,'end','=')
    elif m.type == 'suffix' and not m.orth.startswith('-'):
        m = add_hyphen(m,'start','-')
    elif m.type == 'enclitic' and not m.orth.startswith('='):
        m = add_hyphen(m,'start','=')
    return m

def add_hyphen(m,position, char):
    new_glosses = []
    if position == 'end':
        m.orth = m.orth + char
        for g in m.glosses:
            if not g.endswith(char):
                new_glosses.append(g + char)
    elif position == 'start':
        m.orth = char + m.orth
        for g in m.glosses:
            if not g.startswith(char):
                new_glosses.append(char + g)

    m.glosses = new_glosses
    return m



if __name__ == '__main__':
    xr = Xigt_Reader(sys.argv[1])
