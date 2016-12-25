# -*- coding: utf-8 -*-
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import unicodedata
from gensim import models
from random import choice

##将命名实体的类别转成数字
def neType(str):
    if str == 'S-Ni' or str == 'B-Ni':
        return 0
    if str == 'S-Nh' or str == 'B-Nh':
        return 1
    if str == 'S-Ns' or str == 'B-Ns':
        return 2
################################################

##将关系的类别转成数字
def relationType(c):
    if c[0] == 'E':
        return 0
    if c[0] == 'C':
        return 1
    if c[0] == 'L':
        return 2
    else:
	return 4
#########################################

def main():
    model = models.Word2Vec.load_word2vec_format('cn.cbow.bin', binary=True, unicode_errors = 'ignore')
    segmentor = Segmentor()
    postagger = Postagger()
    recognizer = NamedEntityRecognizer()
    segmentor.load("ltp_data/cws.model")
    postagger.load("ltp_data/pos.model")
    recognizer.load("ltp_data/ner.model")
    ifsen = 1 #表示当前是读入句子还是读入关系
    input = open("trelationExtractionTrainingCorpus.txt", "r")
    outputfv = open('feature_vector.txt', 'w')
    outputfr = open('feature_result.txt', 'w')
    line = input.readline()
    senNo = 0 #debug用，程序中无意义
    while line:
        if line[0] == '|': #表示读到了|，一个句子和关系都已存储，开始进行特征处理和标号
            ##因为一个句子中可能有大量命名实体，这些命名实体大多数都没有关系，所以会导致得到的样本大多数都是N，不平衡，所以采取的方法是从每个句子的N关系中随机抽取一个样本加入训练集，其余的抛弃，这个列表存储N关系的特征，其实frt列表没意义，因为结果都是N，这个写完才意识到。。
	    fvt = list()
	    frt = list()
	    ###############################
	    ##这一段存储句子中每个命名实体开始和结束的位置，以及命名实体的个数
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
	    ################################################
	    ##程序中所有的print输出都是为了debug，不用管它们
            for i in range(namedEntityCount):
                j = namedEntityBegin[i]
                while (j<=namedEntityEnd[i]):
                    print words[j],
		    j = j + 1
                print '\n'
	    #######################################
	    ##对句子中的每两个命名实体，抽取它们之间的特征
            for i in range(namedEntityCount):
                for j in range(namedEntityCount):
                    if j > i:
			print '%d, %d' % (i,j)
                        neType1 = neType(netags[namedEntityBegin[i]])
                        neType2 = neType(netags[namedEntityBegin[j]])
                        if neType1*neType2>0 or neType1+neType2==0: ##只有两个命名实体是人名+组织名或地名+组织名才有意义，其余跳过
                            continue
                        featureVector = list()
                        featureVector.append(neType1)
                        featureVector.append(neType2)
			## 取第一个命名实体左边的两个词作为特征，不足两个词的话补0
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
			## 取第二个命名实体右边的两个词作为特征，不足两个词的话补0
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
			## 取两个命名实体之间的10个词作为特征，不足的话补0
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
			############################################
			## 寻找两个命名实体的关系，如果不在关系列表，关系为N，加入fvt，并在得到所有的N关系后，随机选取一个；如果在关系列表中标记为相应关系，加入特征
                        neIndex = namedEntityBegin[i]
                        ne1 = words[neIndex]
                        while neIndex < namedEntityEnd[i]:
                            neIndex = neIndex + 1
                            ne1 = ne1 + words[neIndex]
                        neIndex = namedEntityBegin[j]
                        ne2 = words[neIndex]
                        while neIndex < namedEntityEnd[j]:
                            neIndex = neIndex + 1
                            ne2 = ne2 + words[neIndex]
                        ifRelation = 0
                        for k in range(relationCount):
                            if (ne1 == relations[k][0] or ne1 == relations[k][1]) and (ne2 == relations[k][0] or ne2 == relations[k][1]) and (ne1 != ne2):
                                ifRelation = 1
                                break
                        if ifRelation == 0:
                            featureResult = 3
                        else:
                            featureResult = relationType(relations[k][2])
			if featureResult < 3:
                            for k in featureVector:
                                outputfv.write('%f ' % k)
                            outputfv.write('\n')
                            outputfr.write(str(featureResult))
			    outputfr.write('\n')
			    print featureResult
			else:
			    fvt.append(featureVector)
			    frt.append(featureResult)
	    nonCount = len(frt)
	    if nonCount == 0:
		ifsen = 1
		line = input.readline()
		print 'senNo: %d' % senNo
		senNo = senNo + 1
		continue
	    choiceOne = choice(range(nonCount))
	    for k in fvt[choiceOne]:
		outputfv.write('%f ' % k)
	    outputfv.write('\n')
	    outputfr.write(str(frt[choiceOne]))
	    outputfr.write('\n')
	    ##########################################################	    
            ifsen = 1
            line = input.readline()
	    print 'senNo: %d' % senNo
	    senNo = senNo + 1
            continue
        if ifsen == 1: # 第一次遇到句子，进行分词，词性分析，命名实体标注
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
        else: # 遇到关系，加入关系列表
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

if __name__ == '__main__':
    main()
