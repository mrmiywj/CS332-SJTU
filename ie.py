# -*- coding: utf-8 -*-
from gensim import models
import pyltp
import unicodedata

MODEL_PATH = './cn.cbow.bin'
CORPUS_PATH = './IEtrainingCorpus/relationExtractionTrainingCorpus.txt'
SEGMENTOR_MODEL_PATH = './ltp_data/cws.model'
POSTAGGER_MODEL_PATH = './ltp_data/pos.model'
NER_MODEL_PATH = './ltp_data/ner.model'
segmentor = pyltp.Segmentor()
postagger = pyltp.Postagger()
ner = pyltp.NamedEntityRecognizer()
ner.load(NER_MODEL_PATH)
postagger.load(POSTAGGER_MODEL_PATH)
segmentor.load(SEGMENTOR_MODEL_PATH)
model = models.Word2Vec.load_word2vec_format(MODEL_PATH, binary=True, unicode_errors='ignore')

class Item:
    def __init__(self, setence, relations):
        self.setence = unicodedata.normalize('NFKC', setence).encode('utf-8')
        self.words = segmentor.segment(self.setence)
        self.postags = postagger.postag(self.words)
        self.netags = ner.recognize(self.words, self.postags)
        self.word_vecs = list()
        for word in self.words:
            try:
                self.word_vecs.append(model[word.decode('utf-8')])
            except:
                self.word_vecs.append(None)
        self.relations = list()
        for relation in relations:
            self.relations.append((relation[0].encode('utf-8'), relation[1].encode('utf-8'), relation[2].encode('utf-8')))

# Read corups as dict
# Input: opened file
# Output: [sentence -> List[relation]]
def read_corpus():
    f = open(CORPUS_PATH, 'r')
    lines = f.readlines()
    res = list()
    mode = 1 # 1 = read sentence, 0 = read relations,
    now = 0
    for l in lines:
        if mode == 1:
            sentence_now = l.decode('gbk')
            res.append((sentence_now, list()))
            mode = 0
        elif mode == 0:
            if l.decode('gbk') == u'|\r\n':
                mode = 1
                now = now + 1
            else:
                relation = l.decode('gbk').split(',')
                res[now][1].append((relation[0], relation[1], relation[2][0]))
    f.close()
    return res

sen2relations = read_corpus()
print "Read corpus done."
items = list()
for i in range(5):
    print sen2relations[i]

for (sen, relations) in sen2relations:
    items.append(Item(sen, relations))

for i in range(-1, -3, -1):
    print items[i].setence
    print items[i].word_vecs
    print items[i].relations
