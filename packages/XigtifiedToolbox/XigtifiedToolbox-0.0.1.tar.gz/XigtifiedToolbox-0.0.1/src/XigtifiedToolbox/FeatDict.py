'''
Update this dictionary with your glosses if needed.
Make sure everything you enter is consistently lower case.
'''

import sys

class IterMixin(object):
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

'''
These dictionaries' role is:
1) to map a variety of possible glosses to a standard set
2) to map standard features to feature types (e.g. masculine to gender)
3) (possibly) to elicit mappings of unknown glosses found in the dataset from the user?
The dictionaries do not decide whether the feature should be inherent (gender on nouns)
or agreement (gender on verb's subject) feature.
'''
# Constants. These come from Leipzig glossing rules: https://www.eva.mpg.de/lingua/resources/glossing-rules.php
# Customized grammars will misbehave if two different features have the same name. To avoid this, make sure that no two
# feature categories share a feature of the same name. For example, purposive is both a mood and a case. To avoid
# conflicts in customized grammars, PURPOSIVE_MOOD and PURPOSEIVE_CASE have different values 'prp' and 'purp'
SUBJECT = 'subj' # this is cononical for head features in morphology
OBJECT = 'obj'
ZERO = '0'
FIRST = '1st' # these match the numbers used by number library
SECOND = '2nd'
THIRD = '3rd'
FOURTH = '4th'
NONFIRST = 'non-1st' # these match the numbers used by number library
NONSECOND = 'non-2nd'
NONTHIRD = 'non-3rd'
FIRSTINCL = '1i'
FIRSTEXCL = '1e'
SINGULAR = 'sg'
NONSINGULAR = 'nsg'
NONPLURAL = 'npl'
DUAL = 'du'
PLURAL = 'pl'
GREATERPAUCAL = 'gpauc'
GREATERPLURAL = 'grpl'
INVERSE = 'invn'
PAUCAL = 'pauc'
FEMININE = 'f'
MASCULINE = 'm'
NEUTER = 'n'
ANIMATE = 'anim'
INANIMATE = 'inanim'
NOMINATIVE = 'nom'
ACCUSATIVE = 'acc'
ERGATIVE = 'erg'
ABSOLUTIVE = 'abs'
GENITIVE = 'gen'
DATIVE = 'dat'
PURPOSIVE_MOOD = 'prp'
PURPOSIVE_CASE = 'purp'
PARTITIVE = 'prt'
COMPARATIVE = 'compv'
EQUATIVE = 'eqt'
PRIVATIVE = 'priv'
PROPRIETIVE = 'propr'
AVERSIVE = 'avr'
FORMAL = 'frml'
TRANSLATIVE = 'trans'
INSTRUMENTAL = 'ins'
LOCATIVE = 'loc'
INTERSETCTIVE = 'inter'
AT = 'at'
POSTERIOR = 'post'
IN = 'in'
NEAR = 'circ'
ANTERIOR = 'ante'
NEXTTO ='apud'
ON = 'on'
ONHONRIZONTAL = 'onhr'
ONVERTICAL = 'onvr'
UNDER = 'sub'
DISTAL = 'sub'
OBVIATIVE = 'obv'
PROXIMATE = 'prox'
ESSIVE = 'ess'
ALLATIVE = 'all'
ABLATIVE = 'abl'
APPROXIMATIVE = 'apprx'
TERMINATIVE = 'term'
PROLATIVE = 'prol'
VERSATIVE = 'vers'
VOCATIVE = 'voc'
OBLIQUE = 'obl'
COMITATIVE = 'com'
BENEFACTIVE = 'ben'
POSSESSIVE = 'poss'
PAST = 'pst'
DISTANT = 'dist'
PRESENT = 'pres'
ONEDAY = '1day'
FUTURE = 'fut'
NONFUTURE = 'nfut'
NONPAST = 'npst'
REMOTE = 'rem'
HODIERNAL = 'hod'
IMMEDIATE = 'immed'
RECENT = 'rct'
PRETERITE = 'pret'
SUBJUNCTIVE = 'sbjv'
NONFACTIVE = 'nfact'
INDICATIVE = 'ind'
IMPERATIVE = 'imp'
IRREALIS = 'irr'
REALIS = 'real'
OPTATIVE = 'opt'
ADMIRATIVE = 'adm'
NONPURPOSIVE = 'nprp'
CONDITIONAL = 'cond'
HYPOTHETICAL = 'hyp'
DEBITIVE = 'deb'
DEDUCTIVE = 'ded'
LIKELY = 'lkly'
OBLIGATIVE = 'oblig'
PERMISSIVE = 'perm'
PROHIBITIVE = 'proh'
SIMULATIVE = 'sim'
YES = 'plus'
IMPERFECTIVE = 'ipfv'
PERFECTIVE = 'pfv'
COMPLETIVE = 'cmpl'
INCEPTIVE = 'incep'
MOMENTANEOUS = 'mom'
RESULTATIVE = 'res'
INCLUSIVE = 'incl'
EXCLUSIVE = 'excl'
HABITUAL = 'hab'
REPETITIVE = 'rep'
ITERATIVE = 'iter'
POTENTIAL = 'pot'
USITATIVE = 'usit'
INTENTIVE = 'intt'
PROGRESSIVE = 'prog'
GRADUATIVE = 'grad'
CONTINUATIVE = 'cont'
DISTRIBUTIVE = 'distr'
PROSPECTIVE = 'prosp'
RELATIVE_ASPECT = 'rel'
DURATIVE = 'dur'
CLASSIFIER = 'cl'
CAUSATIVE = 'caus'
PASSIVE = 'pass'
ANTIPASSIVE = 'antip'
ACTIVE = 'act'
REFLEXIVE = 'refl'
RECIPROCAL = 'recip'
APPLICATIVE = 'appl'
EMPHATIC = 'emph'
ACCOMPANIERFOCUS = 'acfoc'
AGENTFOCUS = 'agfoc'
BENEFICIARYFOCUS = 'bfoc'
CONVEYEDFOCUS = 'cfoc'
INSTRUMENTFOCUS = 'ifoc'
LOCATIONFOCUS = 'lfoc'
PATIENTFOCUS = 'pfoc'
MIDDLE = 'mid'
DIMINUATIVE = 'dim'
AUGMENTATIVE = 'aug'
FINITE = 'finite'
NONFINITE = 'nonfinite'
INFINITIVE = 'inf'
NOMINALIZED = 'nmz'
TOPIC = 'top'
FOCUS = 'foc'
SUPERLATIVE = 'sprl'
ABSOLUTE = 'ab'
RELATIVE_CASE = 'rl'
DEFINITE = 'def'
INDEFINITE = 'indf'
SPECIFIC = 'spec'
NONSPECIFIC = 'nspec'
ACCOMPLISHMENT = 'accmp'
ACHEIVEMENT = 'ach'
ACTIVITY = 'acty'
ATELIC = 'atel'
DYNAMIC = 'dyn'
PUNCTUAL = 'pct'
SEMELFACTIVE = 'semel'
STATIVE = 'stat'
TELIC = 'tel'
HUMAN = 'hum'
NONHUMAN = 'nhum'
ABOVE = 'abv'
BELOW = 'bel'
EVEN = 'even'
MEDIAL = 'med'
NOREF = 'noref'
INVISIBLE = 'nvis'
PHORIC = 'phor'
FIRSTPERSONREFERENCE = 'ref1'
SECONDPERSONREFERENCE = 'ref2'
VISIBLE = 'vis'
ASSUMED = 'assum'
AUDITORY = 'aud'
DIRECT = 'drct'
FIRSTHAND = 'fh'
HEARSAY = 'hrsy'
INFERRED = 'infer'
NONFIRSTHAND = 'nfh'
NONVISUALSENSORY = 'nvsen'
QUOTATIVE = 'quot'
REPORTED = 'rprt'
SENSORY = 'sen'
DECLARATIVE = 'decl'
INTERROGATIVE = 'int'
AVOIDANCE = 'avoid'
COLLOQUIAL = 'col'
HIGHSTATUS = 'forreg'
HUMBLING = 'form'
INFORMAL = 'high'
LITERARY = 'humb'
LOWSTATUS = 'infm'
POLITE = 'lit'
ELEVATEDSTATUS = 'stelev'
SUPREMESTATUS = 'stsupr'
PARTICIPLE = 'ptcp'


subject_feature_vals = {'sbj':SUBJECT,'subject':SUBJECT,'s':SUBJECT,'subj':SUBJECT,
                        'a':SUBJECT, 's/a':SUBJECT, 'agent':SUBJECT, 'a/s':SUBJECT, 'sp':SUBJECT, 'agt':SUBJECT}

object_feature_vals = {'obj':OBJECT,'object':OBJECT,'o':OBJECT, 'p':OBJECT, 'patient':OBJECT,
                       'pat':OBJECT, 'theme':OBJECT, 'op':OBJECT}

perFeatures = {"1":FIRST, "1st":FIRST, "2nd":SECOND, "2":SECOND, "3":THIRD, "3rd":THIRD,
               "n1":NONFIRST, "non-1st":NONFIRST, "n2":NONSECOND, "non-2nd":NONSECOND,
                            "non-3rd":NONTHIRD, "n3":NONTHIRD, "4":FOURTH, "4th":FOURTH,
               "1e": FIRSTEXCL, "1i": FIRSTINCL}# removed the following becasue they are not handled by the grammar matrix , '0':ZERO, 'n0':ZERO, 'obv':OBVIATIVE, 'prx':PROXIMATE, 'prox':PROXIMATE}

numFeatures = {"sing":SINGULAR,  "singular":SINGULAR, "plural":PLURAL,
                        "dual":DUAL, "du": DUAL, "d": DUAL, "dl": DUAL,
                        "sg":SINGULAR, "pl":PLURAL, 'nons' : NONSINGULAR,
               'nonsingular' : NONSINGULAR, 'nonsing' : NONSINGULAR, 'nonsg' : NONSINGULAR,
               'nonplural': NONPLURAL, 'nonpl':NONPLURAL, 'npl': NONPLURAL, 'ns': NONSINGULAR,
               'gpauc':GREATERPAUCAL, 'grpl':GREATERPLURAL, 'invn':INVERSE, 'inv':INVERSE}

genFeatures = {"f":FEMININE, "m":MASCULINE, "n":NEUTER, 'fem':FEMININE,'masc':MASCULINE,'neut':NEUTER,
               'feminine':FEMININE,'masculine':MASCULINE,'neutral':NEUTER,'neuter':NEUTER,'animate':ANIMATE,
               'inanimate':INANIMATE,'anim':ANIMATE,'inan':INANIMATE,'inanim':INANIMATE}

perGenFeatures = {'1masc':(FIRST,MASCULINE), '2masc':(SECOND,MASCULINE), '3masc':('3rd',MASCULINE),
                               '1fem':(FIRST,FEMININE), '2fem':(SECOND,FEMININE), '3fem':('3rd',FEMININE),
                               '1neut':(FIRST,NEUTER), '2neut':(SECOND,NEUTER), '3neut':('3rd',NEUTER),
                               '1m':(FIRST,MASCULINE), '2m':(SECOND,MASCULINE), '3m':('3rd',MASCULINE),
                               '1f':(FIRST,FEMININE), '2f':(SECOND,FEMININE), '3f':('3rd',FEMININE),
                               '1n':(FIRST,NEUTER), '2n':(SECOND,NEUTER), '3n':('3rd',NEUTER)}

perNumFeatures = {"1pl":(FIRST,PLURAL), "1sg":(FIRST,SINGULAR), "2pl":(SECOND,PLURAL),
                          "2sg":(SECOND,SINGULAR), "3sg":(THIRD,SINGULAR), "3pl":(THIRD,PLURAL),
                          "1plural":(FIRST,PLURAL), "1singular":(FIRST,SINGULAR), "2plural":(SECOND,PLURAL),
                          "2singular":(SECOND,SINGULAR), "3singular":(THIRD,SINGULAR), "3plural":(THIRD,PLURAL),
                  "1du": (FIRST, DUAL), "1du": (FIRST, DUAL), "2du": (SECOND, DUAL),
                  "2du": (SECOND, DUAL), "3du": (THIRD, DUAL), "3du": (THIRD, DUAL),
                  "1dual": (FIRST, DUAL), "2dual": (SECOND, DUAL), "3dual": (THIRD, DUAL),
                  "1p": (FIRST, PLURAL), "2p": (SECOND, PLURAL), "3p": (THIRD, PLURAL),
                  "1p": (FIRST, SINGULAR), "2p": (SECOND, SINGULAR), "3p": (THIRD, SINGULAR)}

perNumGenFeatures = {'1sm':(FIRST,SINGULAR,MASCULINE),'2sm':(SECOND,SINGULAR,MASCULINE),'3sm':(THIRD,SINGULAR,MASCULINE),
                     '1pm': (FIRST, PLURAL, MASCULINE), '2pm': (SECOND, PLURAL, MASCULINE),'3pm': (THIRD, PLURAL, MASCULINE),
                     '1sf': (FIRST, SINGULAR, FEMININE), '2sf': (SECOND, SINGULAR, FEMININE),'3sf': (THIRD, SINGULAR, FEMININE),
                     '1pf': (FIRST, PLURAL, FEMININE), '2pf': (SECOND, PLURAL, FEMININE),'3pf': (THIRD, PLURAL, FEMININE),
                     '1sn':(FIRST,SINGULAR,NEUTER),'2sn':(SECOND,SINGULAR,NEUTER),'3sn':(THIRD,SINGULAR,NEUTER),
                     '1pn': (FIRST, PLURAL, NEUTER), '2pn': (SECOND, PLURAL, NEUTER),'3pn': (THIRD, PLURAL, NEUTER),
                     '2fp': (SECOND, FEMININE, OBJECT), '1fp': (FIRST, FEMININE, OBJECT),
                     '3mp': (THIRD, PLURAL, MASCULINE),
                     '2mp': (SECOND, PLURAL, MASCULINE), '1mp': (FIRST, PLURAL, MASCULINE),
                     '3np': (THIRD, PLURAL, NEUTER),
                     '2np': (SECOND, PLURAL, NEUTER), '1np': (FIRST, PLURAL, NEUTER), '3fp': (THIRD, PLURAL, FEMININE)}

# KPH I moved these to pernum because fuse and exclusive are consisidered person features in the GM
perNumInclFeatures = {'1pe': (FIRST,PLURAL,EXCLUSIVE),'1pi':(FIRST,PLURAL,INCLUSIVE),
                      '1se': (FIRST, SINGULAR, EXCLUSIVE), '1si': (FIRST, SINGULAR, INCLUSIVE)}

inclFeatures = {'incl': INCLUSIVE, 'in': INCLUSIVE, 'inc': INCLUSIVE, 'excl': EXCLUSIVE, 'ex': EXCLUSIVE, 'exc': EXCLUSIVE}


perNumInclHeadFeatures = {'1peA': (FIRST,PLURAL,EXCLUSIVE,SUBJECT),'1piA':(FIRST,PLURAL,INCLUSIVE,SUBJECT),
                          '1seA': (FIRST, SINGULAR, EXCLUSIVE, SUBJECT), '1siA': (FIRST, SINGULAR, INCLUSIVE, SUBJECT)}
# What to do with s/p?
perHeadFeatures = {"1s": (FIRST, SUBJECT), "2s": (SECOND, SUBJECT), "3s": (THIRD, SUBJECT),
                           "1s/a": (FIRST, SUBJECT), "2s/a": (SECOND, SUBJECT), "3s/a": (THIRD, SUBJECT),
                           "1a": (FIRST, SUBJECT), "2a": (SECOND, SUBJECT), "3a": (THIRD, SUBJECT),
                           #"1p": (FIRST, OBJECT), "2p": (SECOND, OBJECT), "3p": (THIRD, OBJECT), #these are plural more often than patient
                           "1s/p": (FIRST, "s/p"), "2s/p": (SECOND, "s/p"), "3s/p": (THIRD, "s/p"),
                           "1o": (FIRST, OBJECT), "2o": (SECOND, OBJECT), "3o": (THIRD, OBJECT),
                           '3I': (THIRD, OBJECT), '3II':(THIRD,OBJECT), '1subj': (FIRST, SUBJECT),
                           '2subj': (SECOND, SUBJECT), '3subj': (THIRD, SUBJECT), '1sbj': (FIRST, SUBJECT),
                           '2sbj': (SECOND, SUBJECT), '3sbj': (THIRD, SUBJECT), '1obj': (FIRST, OBJECT),
                           '2obj': (SECOND, OBJECT), '3obj': (THIRD, OBJECT)}

# Note: ns is not included because it is more commonly "nonsingular number" than "neuter gender on subject"
perGenHeadFeatures = {"1ms":(FIRST, MASCULINE, SUBJECT), "2ms":(SECOND, MASCULINE, SUBJECT),
                      "3ms":(THIRD, MASCULINE, SUBJECT),
                              "1fs":(FIRST, FEMININE, SUBJECT),
                              "2fs":(SECOND, FEMININE, SUBJECT), "3fs":(THIRD, FEMININE, SUBJECT),
                      "1mo":(FIRST, MASCULINE, OBJECT),
                              "2mo":(SECOND, MASCULINE, OBJECT), "3mo":(THIRD, MASCULINE, OBJECT),
                              "1fo":(FIRST, FEMININE, OBJECT),
                              "2fo":(SECOND, FEMININE, OBJECT), "3fo":(THIRD, FEMININE, OBJECT),
                      "1no":(FIRST, NEUTER, OBJECT),
                              "2no":(SECOND, NEUTER, OBJECT),
                              "3no":(THIRD, NEUTER, OBJECT)}

perNumHeadFeatures = {"1nsp":(FIRST,NONSINGULAR,OBJECT),"2nsp":(SECOND,NONSINGULAR,OBJECT),
                      "3nsp":(THIRD,NONSINGULAR,OBJECT),"1nss/a":(FIRST,NONSINGULAR,SUBJECT),
                      "2nss/a":(SECOND,NONSINGULAR,SUBJECT),"3nss/a":(THIRD,NONSINGULAR,SUBJECT),
                      "1sp":(FIRST,SINGULAR,OBJECT),"2sp":(SECOND,SINGULAR,OBJECT),"3sp":(THIRD,SINGULAR,OBJECT),
                      "1ss/a":(FIRST,SINGULAR,SUBJECT),"2ss/a":(SECOND,SINGULAR,SUBJECT),
                      "3ss/a":(THIRD,SINGULAR,SUBJECT), '1sa':(FIRST,SINGULAR,SUBJECT),
                      '2sa':(SECOND,SINGULAR,SUBJECT),'3sa':(THIRD,SINGULAR,SUBJECT),
                      "1pA": (FIRST,PLURAL,SUBJECT),"2pA": (SECOND,PLURAL,SUBJECT),"3pA": (THIRD,PLURAL,SUBJECT),
                      '1sA':(FIRST,SINGULAR,SUBJECT),'2sA':(SECOND,SINGULAR,SUBJECT),'3sA':(THIRD,SINGULAR,SUBJECT),
                      "1nso": (FIRST, NONSINGULAR, OBJECT), "2nso": (SECOND, NONSINGULAR, OBJECT),
                      "3nso": (THIRD, NONSINGULAR, OBJECT),"1so":(FIRST,SINGULAR,OBJECT),"2so":(SECOND,SINGULAR,OBJECT),
                      "1ss":(THIRD,SINGULAR,OBJECT), '2ss':(SECOND,SINGULAR,SUBJECT),'3ss':(THIRD,SINGULAR,SUBJECT),
                      "1pS": (FIRST,PLURAL,SUBJECT),"2pS": (SECOND,PLURAL,SUBJECT),"3pS": (THIRD,PLURAL,SUBJECT),
                      '1sS':(FIRST,SINGULAR,SUBJECT),'2sS':(SECOND,SINGULAR,SUBJECT),'3sS':(THIRD,SINGULAR,SUBJECT)}

perNumCaseFeatures = {'1sgn':(FIRST,SINGULAR,NOMINATIVE),'2sgn':(SECOND,SINGULAR,NOMINATIVE),'3sgn':(THIRD,SINGULAR,NOMINATIVE),
                      '1sgd':(FIRST,SINGULAR,DATIVE),'2sgd':(SECOND,SINGULAR,DATIVE),'3sgd':(THIRD,SINGULAR,DATIVE),
                      '1sge':(FIRST,SINGULAR,ERGATIVE),'2sge':(SECOND,SINGULAR,ERGATIVE),'3sge':(THIRD,SINGULAR,ERGATIVE),
                      '1sn': (FIRST, SINGULAR, NOMINATIVE),'2sn': (SECOND, SINGULAR, NOMINATIVE),
                      '3sn': (THIRD, SINGULAR, NOMINATIVE),'1sd': (FIRST, SINGULAR, DATIVE), '2sd': (SECOND, SINGULAR, DATIVE),
                      '3sd': (THIRD, SINGULAR, DATIVE),'1se': (FIRST, SINGULAR, ERGATIVE), '2se': (SECOND, SINGULAR, ERGATIVE),
                      '3se': (THIRD, SINGULAR, ERGATIVE),
                      '1pln':(FIRST,PLURAL,NOMINATIVE),'2pln':(SECOND,PLURAL,NOMINATIVE),'3pln':(THIRD,PLURAL,NOMINATIVE),
                      '1pld':(FIRST,PLURAL,DATIVE),'2pld':(SECOND,PLURAL,DATIVE),'3pld':(THIRD,PLURAL,DATIVE),
                      '1ple':(FIRST,PLURAL,ERGATIVE),'2ple':(SECOND,PLURAL,ERGATIVE),'3ple':(THIRD,PLURAL,ERGATIVE),
                      '1pn': (FIRST, PLURAL, NOMINATIVE),'2pn': (SECOND, PLURAL, NOMINATIVE),
                      '3pn': (THIRD, PLURAL, NOMINATIVE),'1pd': (FIRST, PLURAL, DATIVE), '2pd': (SECOND, PLURAL, DATIVE),
                      '3pd': (THIRD, PLURAL, DATIVE),'1pe': (FIRST, PLURAL, ERGATIVE), '2pe': (SECOND, PLURAL, ERGATIVE),
                      '3pe': (THIRD, PLURAL, ERGATIVE)
                      }

caseFeatures = {'nom':NOMINATIVE,'noms':NOMINATIVE,'acc':ACCUSATIVE,'erg':ERGATIVE,
                'abs':ABSOLUTIVE,'loc':LOCATIVE,'gen':GENITIVE,'instr':INSTRUMENTAL,'inst':INSTRUMENTAL,'ins':INSTRUMENTAL,
                'dat':DATIVE,'obl':OBLIQUE,'abl':ABLATIVE,'com':COMITATIVE,#'poss':POSSESSIVE,'pos':POSSESSIVE,
                'voc':VOCATIVE,'ben':BENEFACTIVE,'benef':BENEFACTIVE,'prp':PURPOSIVE_CASE,'purp':PURPOSIVE_CASE,'rel':RELATIVE_CASE,
                'prt':PARTITIVE,'compv':COMPARATIVE,'eqtv':EQUATIVE,'eqt':EQUATIVE,'priv':PRIVATIVE,'propr':PROPRIETIVE,'avr':AVERSIVE,
                'frml':FORMAL,'fml':FORMAL,'trans':TRANSLATIVE,'byway':ESSIVE,'ess':ESSIVE,'inter':INTERSETCTIVE,
                'among':INTERSETCTIVE,'at':AT,'post':POSTERIOR,'behind':POSTERIOR,'in':IN,'near':NEAR,'circ':NEAR,
                'infront':ANTERIOR,'ante':ANTERIOR,'nextto':NEXTTO,'apud':NEXTTO,'on':ON,'onhr':ONHONRIZONTAL,
                'onvr':ONVERTICAL,'sub':UNDER,'under':UNDER,'rem':DISTAL,'dist':DISTAL,'prox':PROXIMATE,'all':ALLATIVE,
                'apprx':APPROXIMATIVE,'approx':APPROXIMATIVE,'term':TERMINATIVE,'prol':PROLATIVE,'vers':VERSATIVE}

animFeatures ={'anim':ANIMATE,'hum':HUMAN,'inan':INANIMATE,'nhum':NONHUMAN}

negFeatures = {"neg":YES, "not":YES}

tenseFeatures = {"past":PAST, "pst":PAST, "pres":PRESENT, "prs":PRESENT, "fut":FUTURE,
                              "npst":NONPAST, "nfut":NONFUTURE, "future":FUTURE, "present":PRESENT,
                 'nonpast':NONPAST, 'npast':NONPAST, 'npt':NONPAST, 'nonfuture':NONFUTURE,'nonfut':NONFUTURE,'nonpst':NONPAST,'dist':DISTANT,
                 'pret':PRETERITE, 'preterite':PRETERITE, 'rem': REMOTE, 'remote':REMOTE, 'rmt':REMOTE, '1day':ONEDAY, 'oneday':ONEDAY,
                 'hod':HODIERNAL, 'hodiernal':HODIERNAL, 'immed':IMMEDIATE, 'immediate':IMMEDIATE, 'rct':RECENT,
                 'recent':RECENT}

aspectFeatures = {"imp":IMPERFECTIVE,"prf":PERFECTIVE,"impfv": IMPERFECTIVE,'imperf':IMPERFECTIVE,'ipfv':IMPERFECTIVE,
                  'impf':IMPERFECTIVE,"imperfective": IMPERFECTIVE,'impfv':IMPERFECTIVE, "pfv": PERFECTIVE, "perfective":PERFECTIVE,
                  "prfv":PERFECTIVE,"perf":PERFECTIVE,"hab": HABITUAL,'habit':HABITUAL,'prog':PROGRESSIVE,'dur':DURATIVE,'aor':PERFECTIVE,
                  'prosp':PROSPECTIVE,'prsp':PROSPECTIVE,'rel':RELATIVE_ASPECT,'ri':RELATIVE_ASPECT+'_'+IMPERFECTIVE,
                  'rp':RELATIVE_ASPECT+'_'+PERFECTIVE,'rpf':RELATIVE_ASPECT+'_'+PERFECTIVE,'distr':DISTRIBUTIVE, 'contin':CONTINUATIVE,
                  'cont':CONTINUATIVE, 'continuative':CONTINUATIVE, 'con':CONTINUATIVE, 'compl':COMPLETIVE, 'cmpl':COMPLETIVE,
                  'completive':COMPLETIVE,'comp':COMPLETIVE,'usit':USITATIVE,'usitative':USITATIVE,'inc':INCEPTIVE,
                  'incep':INCEPTIVE, 'pot':POTENTIAL, 'potential':POTENTIAL, 'rep':REPETITIVE, 'repet':REPETITIVE, 'repetitive':REPETITIVE,
                  'intentive':INTENTIVE, 'intt':INTENTIVE, 'iter':ITERATIVE, 'res':RESULTATIVE, 'result':RESULTATIVE,
                  'grad':GRADUATIVE,'graduative':GRADUATIVE,'mo':MOMENTANEOUS,'mom':MOMENTANEOUS,'momentaneous':MOMENTANEOUS}
#KPH: AOR is a weird one-- don't know what it stands for- came from ODIN

tenseAspectFeatures = {}
for tense in tenseFeatures:
    for aspect in aspectFeatures:
        tenseAspectFeatures[tense+aspect] = (tenseFeatures[tense], aspectFeatures[aspect])

# subj often is used for subjunctive but clashes with subject. What is a good way to go about it?
# Probably only looking at mood versus subject features very separately somehow?..

moodFeatures = {"sbjv":SUBJUNCTIVE, "ind":INDICATIVE,"indic":INDICATIVE,'opt':OPTATIVE,'subjunctive':SUBJUNCTIVE,'indicative':INDICATIVE,
                'optative':OPTATIVE, 'irrealis':IRREALIS,'irr':IRREALIS,'irreal':IRREALIS,'irri':IRREALIS, 'realis':REALIS,
                'real':REALIS,'imp':IMPERATIVE,'imperative':IMPERATIVE,'impv':IMPERATIVE, 'rec':RECIPROCAL, 'recip':RECIPROCAL,'recp':RECIPROCAL,
                'reciprocal':RECIPROCAL,'rr':RECIPROCAL, 'nfact':NONFACTIVE, 'nonfactive':NONFACTIVE, 'adm':ADMIRATIVE,'prp':PURPOSIVE_MOOD,
                'purp':PURPOSIVE_MOOD,'nprp':NONPURPOSIVE,'npurp':NONPURPOSIVE,'nonpurp':NONPURPOSIVE,'nonprp':NONPURPOSIVE,
                'cond':CONDITIONAL,'deb':DEBITIVE,'ded':DEDUCTIVE,'int':INTENTIVE,'inten':INTENTIVE,'lkly':LIKELY,'likely':LIKELY,
                'oblig':OBLIGATIVE,'obl':OBLIGATIVE,'opt':OPTATIVE,'perm':PERMISSIVE,'sim':SIMULATIVE, 'proh':PROHIBITIVE, 'hyp':HYPOTHETICAL}

voiceFeatures = {"appl":APPLICATIVE,'caus':CAUSATIVE,'cause':CAUSATIVE,'pass':PASSIVE,'passive':PASSIVE,'refl':REFLEXIVE,'emph':EMPHATIC,
                 'antip':ANTIPASSIVE,'antipas':ANTIPASSIVE,'antipass':ANTIPASSIVE,'anti':ANTIPASSIVE,'act':ACTIVE,'active':ACTIVE,
                 'acfoc':ACCOMPANIERFOCUS,'agfoc':AGENTFOCUS,'bfoc':BENEFICIARYFOCUS,'cfoc':CONVEYEDFOCUS,'dir':DIRECT,
                 'ifoc':INSTRUMENTFOCUS,'inv':INVERSE,'lfoc':LOCATIONFOCUS,'mid':MIDDLE,'pfoc':PATIENTFOCUS}

formFeatures = {'fin':FINITE,'nf':NONFINITE,'nonfin':NONFINITE,'nfin':NONFINITE,'inf':INFINITIVE,'nmz':NOMINALIZED,
                'nmzr':NOMINALIZED,'nmlz':NOMINALIZED,'ptcp':PARTICIPLE,'part':PARTICIPLE}

aktionsartFeatures = {'accmp':ACCOMPLISHMENT,'ach':ACHEIVEMENT,'acty':ACTIVITY,'atel':ATELIC,'dur':DURATIVE,'dyn':DYNAMIC,
                      'pct':PUNCTUAL,'semel':SEMELFACTIVE,'stat':STATIVE,'tel':TELIC}

#KPH: the classifier cat comes from ODIN and overlaps with Gender
classifierFeatures = {'cl':CLASSIFIER,'clf':CLASSIFIER,'i':CLASSIFIER,'ii':CLASSIFIER,'iii':CLASSIFIER,'iv':CLASSIFIER,
                      'v':CLASSIFIER,'vi':CLASSIFIER,'vii':CLASSIFIER,'viii':CLASSIFIER,'ix':CLASSIFIER,'x':CLASSIFIER}

sizeFeatures = {'dim':DIMINUATIVE,'dimin':DIMINUATIVE,'aug':AUGMENTATIVE}

infoStrFeatures ={'top':TOPIC,'topic':TOPIC,'foc':FOCUS,'focus':FOCUS}

compFeatures = {'cmpr':COMPARATIVE,'comp':COMPARATIVE,'sprl':SUPERLATIVE,'sup':SUPERLATIVE,'ab':ABSOLUTE,'abs':ABSOLUTIVE,
                'rl':RELATIVE_CASE,'rel':RELATIVE_CASE,'eqt':EQUATIVE}

defFeatures = {'def':DEFINITE,'indf':INDEFINITE,'spec':SPECIFIC,'nspec':NONSPECIFIC}

deixisFeatures = {'abv':ABOVE,'bel':BELOW,'even':EVEN,'med':MEDIAL,'noref':NOREF,'dist':DISTAL,'nvis':INVISIBLE,
                  'invis':INVISIBLE,'phor':PHORIC,'prox':PROXIMATE,'ref1':FIRSTPERSONREFERENCE,'ref2':SECONDPERSONREFERENCE,
                  'remt':REMOTE,'rmt':REMOTE,'vis':VISIBLE}

evidFeatures = {'assum':ASSUMED,'aud':AUDITORY,'drct':DIRECT,'dir':DIRECT,'fh':FIRSTHAND,'hrsy':HEARSAY,'infer':INFERRED,
                'nfh':NONFIRSTHAND,'nvsen':NONVISUALSENSORY,'quot':QUOTATIVE,'rprt':REPORTED,'sen':SENSORY}

interFeatures = {'decl':DECLARATIVE, 'int':INTERROGATIVE, 'q':INTERROGATIVE}

politeFeatures = {'avoid':AVOIDANCE, 'col':COLLOQUIAL, 'elev':FORMAL, 'foreg':FORMAL, 'form':FORMAL, 'high':HIGHSTATUS,
                  'humb':HUMBLING, 'hum':HUMBLING, 'infm':INFORMAL, 'lit':LITERARY, 'low':LOWSTATUS, 'pol':POLITE,
                  'stelev':ELEVATEDSTATUS, 'stsupr':SUPREMESTATUS}

possFeatures = {}


#ECC: create lists of nouny/verby keys (used in XigtReader to check for words with affixes that are both nouny and verby
nouny_feat_dicts = [caseFeatures]
verby_feat_dicts = [tenseFeatures, aspectFeatures, moodFeatures, voiceFeatures, formFeatures]


def collect_nouny_keys():
    return set().union(*nouny_feat_dicts)


def collect_verby_keys():
    return set().union(*verby_feat_dicts)


class FeatureDictionary(IterMixin):

    def __init__(self):
        self.dictionaries = {'aktionsartFeatures':aktionsartFeatures,
                             'animFeatures':animFeatures,
                             'aspectFeatures': aspectFeatures,
                             'caseFeatures': caseFeatures,
                             'classifierFeatures': classifierFeatures,
                             'compFeatures': compFeatures,
                             'defFeatures': defFeatures,
                             'deixisFeatures': deixisFeatures,
                             'evidFeatures': evidFeatures,
                             'formFeatures': formFeatures,
                             'genFeatures': genFeatures,
                             'infoStrFeatures': infoStrFeatures,
                             'interFeatures': interFeatures,
                             'moodFeatures': moodFeatures,
                             'negFeatures': negFeatures,
                             'numFeatures': numFeatures,
                             'object_feature_vals': object_feature_vals,
                             'perFeatures': perFeatures,
                             'perGenFeatures': perGenFeatures,
                             'perHeadFeatures': perHeadFeatures,
                             'perGenHeadFeatures': perGenHeadFeatures,
                             'perNumFeatures': perNumFeatures,
                             'perNumCaseFeatures': perNumCaseFeatures,
                             'perNumGenFeatures': perNumGenFeatures,
                             'perNumHeadFeatures': perNumHeadFeatures,
                             'perNumInclFeatures': perNumInclFeatures,
                             'perNumInclHeadFeatures': perNumInclHeadFeatures,
                             'politeFeatures': politeFeatures,
                             'sizeFeatures': sizeFeatures,
                             'subject_feature_vals': subject_feature_vals,
                             'tenseFeatures': tenseFeatures,
                             'tenseAspectFeatures': tenseAspectFeatures,
                             'voiceFeatures': voiceFeatures
                             }
        self.all_keys = self.collect_all_keys()

        #ECC: nouny and verby key lists
        # self.nouny_keys = collect_nouny_keys()
        # self.verby_keys = collect_verby_keys()

        # Variable names used in the Grammar Matrix. Cannot use any of these since then the Grammar Matrix will
        # not be able to properly compile the grammar.

        self.internal_feature_name = ["p", "i", "a", "x", "e", "tense", "sf", "comp", "cat", "conj", "rel", "agr",
                                              "opt", "cont", "sign", "number", "adv", "topic", "complete", "det",
                                              "scratch", "word", "passive", "last", "mod", "head", "per",
                                              "activated", "altkey", "altkeyrel", "alts", "apparg", "arg",
                                              "args", "arg-st", "aspect", "body", "carg", "c-arg", "c-cont",
                                              "cform", "clause", "clause-key", "cog-st", "compkey", "comps",
                                              "conj-dtr", "coord", "coord-rel", "coord-strat", "ctxt", "dtr", "fc",
                                              "first", "gtop", "harg", "hc-light", "hcons", "head-dtr", "hook", "icons",
                                              "icons-key", "index", "inflected", "instloc", "key", "key-arg", "keycomp",
                                              "keyrel", "keys", "label-name", "larg", "lbl", "lcoord-dtr", "l-hndl", "light",
                                              "l-index", "list", "lkeys", "local", "l-periph", "ltop", "marker-dtr", "mc",
                                              "meta-prefix", "meta-suffix", "mkg", "modified", "mood", "needs-affix", "node",
                                              "nonconj-dtr", "non-head-dtr", "non-local", "non-marker-dtr", "ocompkey",
                                              "opt-cs", "periph", "png", "posthead", "pred", "presup", "que", "rcoord-dtr",
                                              "rels", "rest", "result", "r-hndl", "r-index", "r-periph", "rstr", "rule-name",
                                              "slash", "sort", "spec", "speci", "spr", "stem", "subj", "synsem", "target",
                                              "tp", "val", "wlink", "xarg"]

    def collect_all_keys(self):
        all_keys = set()
        for d in self.dictionaries:
            for k in self.dictionaries[d]:
                all_keys.add(k)
        return all_keys

    def validate_dictionary(self):
        for d in self.dictionaries:
            for key, val in self.dictionaries[d].items():
                if self.lowercase_error(key) or self.lowercase_error(val):
                    sys.exit(1)


    def lowercase_error(self,item):
        for ch in item:
            if not (ch.isdigit() or ch.islower()):
                print('Found a non-lowercase item in FeatDict.py; '
                      'please make sure everything there is lowercase: ' + item)
                return True
            else:
                return False
