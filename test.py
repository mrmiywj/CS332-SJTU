# -*- coding: utf-8 -*-
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import unicodedata
from gensim import models
from sklearn.svm import SVC
from sklearn.externals import joblib
import numpy as np

def neType(str):
    if str == 'S-Ni' or str == 'B-Ni':
        return 0
    if str == 'S-Nh' or str == 'B-Nh':
        return 1
    if str == 'S-Ns' or str == 'B-Ns':
        return 2

def relationType(c):
    if c[0] == 'E':
        return 0
    if c[0] == 'C':
        return 1
    if c[0] == 'L':
        return 2
    else:
	return 4

def main():
    clf = joblib.load('model.pkl')
    pf = list()
    ne1s = list()
    ne2s = list()
    model = models.Word2Vec.load_word2vec_format('cn.cbow.bin', binary=True, unicode_errors = 'ignore')
    segmentor = Segmentor()
    postagger = Postagger()
    recognizer = NamedEntityRecognizer()
    segmentor.load("ltp_data/cws.model")
    postagger.load("ltp_data/pos.model")
    recognizer.load("ltp_data/ner.model")
    ifsen = 1
    input = open("trelationExtractionTrainingCorpus.txt", "r")
    outputfv = open('feature_vector.txt', 'w')
    outputfr = open('feature_result.txt', 'w')
    outputp = open('predict_result.txt', 'w')
    line = input.readline()
    senNo = 0
    while line:
        if line[0] == '|':
	    namedEntityBegin = list()
	    namedEntityEnd = list()
	    namedEntityCount = 0
	    i = 0
            for netag in netags:
                if netag == 'O':
		    i = i + 1
                    continue
                if netag == 'S-Ni' or netag == 'S-Nh' or netag == 'S-Ns':
                    namedEntityBegin.append(i)
                    namedEntityEnd.append(i)
                    namedEntityCount = namedEntityCount + 1
		    i = i + 1
                    continue
                if netag == 'B-Ni' or netag == 'B-Nh' or netag == 'B-Ns':
                    namedEntityBegin.append(i)
                    namedEntityCount = namedEntityCount + 1
		    i = i + 1
                    continue
                if netag == 'E-Ni' or netag == 'E-Nh' or netag == 'E-Ns':
                    namedEntityEnd.append(i)
    		    i = i + 1
                    continue
                else:
 		    i = i + 1
                    continue
            for i in range(namedEntityCount):
                j = namedEntityBegin[i]
                while (j<=namedEntityEnd[i]):
                    print words[j],
		    j = j + 1
                print '\n'
            for i in range(namedEntityCount):
                for j in range(namedEntityCount):
                    if j > i:
			print '%d, %d' % (i,j)
                        neType1 = neType(netags[namedEntityBegin[i]])
                        neType2 = neType(netags[namedEntityBegin[j]])
                        if neType1*neType2>0 or neType1+neType2==0:
                            continue
                        featureVector = list()
                        featureVector.append(neType1)
                        featureVector.append(neType2)
                        if namedEntityBegin[i] < 3:
                            leftWindowScale = namedEntityBegin[i]
                        else:
                            leftWindowScale = 2
                        featureVector.append(leftWindowScale)
                        if leftWindowScale == 0:
                            for k in range(300):
                                featureVector.append(0)
                                featureVector.append(0)
                        elif leftWindowScale == 1:
                            try:
                                t = model[words[namedEntityBegin[i]-1].decode('utf-8')]
				for k in t:
				    featureVector.append(k)
                            except:
                                for k in range(300):
                                    featureVector.append(0)
                            for k in range(300):
                                featureVector.append(0)
                        else:
                            for k in range(2):
                                try:
                                    t = model[words[namedEntityBegin[i]-k-1].decode('utf-8')]
				    for ktemp in t:
					featureVector.append(ktemp)
                                except:
                                    for ktemp in range(300):
                                        featureVector.append(0)
                        wordsLen = len(words)
                        rightWindowScale = wordsLen - namedEntityEnd[j]
                        if rightWindowScale > 2:
                            rightWindowScale = 2
                        featureVector.append(rightWindowScale)
                        if rightWindowScale == 0:
                            for k in range(300):
                                featureVector.append(0)
                                featureVector.append(0)
                        elif rightWindowScale == 1:
                            try:
                                t = model[words[namedEntityEnd[j]+1].decode('utf-8')]
				for k in t:
				    featureVector.append(k)
                            except:
                                for k in range(300):
                                    featureVector.append(0)
                            for k in range(300):
                                featureVector.append(0)
                        else:
                            for k in range(2):
                                try:
                                    t = model[words[namedEntityEnd[j]+1+k].decode('utf-8')]
				    for ktemp in t:
					featureVector.append(ktemp)
                                except:
                                    for ktemp in range(300):
                                        featureVector.append(0)
                        wordBetweenCount = namedEntityBegin[j] - namedEntityEnd[i] - 1
                        featureVector.append(wordBetweenCount)
                        if wordBetweenCount == 0:
                            for k in range(10):
                                for ktemp in range(300):
                                    featureVector.append(0)
                        elif wordBetweenCount <= 10:
                            for k in range(wordBetweenCount):
                                try:
                                    t = model[words[namedEntityEnd[i]+k+1].decode('utf-8')]
				    for ktemp in t:
					featureVector.append(ktemp)
                                except:
                                    for ktemp in range(300):
                                        featureVector.append(0)
                            for k in range(10-wordBetweenCount):
                                for ktemp in range(300):
                                    featureVector.append(0)
                        else:
                            for k in range(5):
                                try:
                                    t = model[words[namedEntityEnd[i]+k+1].decode('utf-8')]
				    for ktemp in t:
					featureVector.append(ktemp)
                                except:
                                    for ktemp in range(300):
                                        featureVector.append(0)
                            for k in range(5):
                                try:
                                    t = model[words[namedEntityBegin[j]-5+k].decode('utf-8')]
				    for ktemp in t:
					featureVector.append(ktemp)
                                except:
                                    for ktemp in range(300):
                                        featureVector.append(0)
			pf.append(featureVector)
                        neIndex = namedEntityBegin[i]
                        ne1 = words[neIndex]
                        while neIndex < namedEntityEnd[i]:
                            neIndex = neIndex + 1
                            ne1 = ne1 + words[neIndex]
			ne1s.append(ne1)
                        neIndex = namedEntityBegin[j]
                        ne2 = words[neIndex]
                        while neIndex < namedEntityEnd[j]:
                            neIndex = neIndex + 1
                            ne2 = ne2 + words[neIndex]
			ne2s.append(ne2)
                        ifRelation = 0
                        for k in range(relationCount):
                            if (ne1 == relations[k][0] or ne1 == relations[k][1]) and (ne2 == relations[k][0] or ne2 == relations[k][1]) and (ne1 != ne2):
                                ifRelation = 1
                                break
                        if ifRelation == 0:
                            featureResult = 3
                        else:
                            featureResult = relationType(relations[k][2])
                        for k in featureVector:
                            outputfv.write('%f ' % k)
                        outputfv.write('\n')
                        outputfr.write(str(featureResult))
			outputfr.write('\n')
			print featureResult
            ifsen = 1
            line = input.readline()
	    print 'senNo: %d' % senNo
	    senNo = senNo + 1
            continue
        if ifsen == 1:
            print line
	    line = unicodedata.normalize('NFKC', line.decode('utf-8')).encode('utf-8')
            words = segmentor.segment(line)
            postags = postagger.postag(words)
            netags = recognizer.recognize(words, postags)
            print "|".join(words)
            print "|".join(postags)
            print "|".join(netags)
            ifsen = 0
            relationCount = 0
            relations = list()
        else:
            relation = line.split(',')
            relations.append(relation)
            relationCount = relationCount + 1
            print "|".join(relations[relationCount-1])
	    print relations[relationCount-1][2]
        line = input.readline()
    segmentor.release()
    postagger.release()
    recognizer.release()
    input.close()
    outputfv.close()
    outputfr.close()
    pred_res = clf.predict(pf)
    for i in pred_res:
	outputp.write(str(i))
	outputp.write('\n')

if __name__ == '__main__':
    main()
