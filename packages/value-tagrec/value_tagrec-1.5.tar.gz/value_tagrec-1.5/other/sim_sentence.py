#!/usr/bin/env python
# coding: utf-8

# 计算两个句子之间相似度
#from fuzzywuzzy import fuzz
#import jieba
#import numpy as np
#import difflib
import Levenshtein
import time

def calSimSentence(s1, s2, method, outStr=' '):
    ###调用该函数，选择方法计算相似度
    method = method.lower()#转换为小写
    if method == 'edit':
        return editSim(s1, s2)
    elif method == 'levenshtein':
        return levenshteinSim(s1, s2)
    elif method == 'jaro':
        return jaroSim(s1, s2)
    elif method == 'jaroWinkler':##返回None
        return jaroWinklerSim(s1, s2)
    # elif method == 'fuzz': #结果>1
    #     return fuzzSim(s1, s2)
    # elif method == 'cos':
    #     return cosSim(s1, s2)
    # elif method == 'difflib':
    #     return difflibSim(s1, s2)
    # elif method == 'difflib_out':
    #     return difflibSim_out(s1, s2, outStr)



def editSim(s1, s2):
    """
    编辑距离算法
    :param s1: 语句1
    :param s2: 语句2
    :return: 编辑距离
    """
    n = max(len(s1), len(s2))
    return 1 - Levenshtein.distance(s1, s2) / n

def levenshteinSim(s1, s2):
    """
    计算莱文斯坦比
    :param s1:
    :param s2:
    :return:
    """
    return Levenshtein.ratio(s1, s2)

def jaroSim(s1, s2):
    """
    计算jaro距离
    :param s1:
    :param s2:
    :return:
    """
    return Levenshtein.jaro(s1, s2)

def jaroWinklerSim(s1, s2):
    """
    Jaro–Winkler距离。。！！返回None
    :param s1:
    :param s2:
    :return:
    """
    return Levenshtein.jaro_winkler(s1, s2)

# def fuzzSim(s1, s2):
#     """
#     fuzz距离，>1
#     :param s1:
#     :param s2:
#     :return:
#     """
#     return fuzz.ratio(s1, s2)


# def cosSim(s1, s2):
#     """
#     计算两个句子的余弦相似度
#     :param s1: 语句1
#     :param s2:语句2
#     :return:
#     """
#     vec1, vec2 = get_01_wordvec(s1, s2)
#     dist = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
#     return dist

# def difflibSim(s1, s2):
#     """
#     python自带的difflib相似度比较
#     :param s1:
#     :param s2:
#     :return:
#     """
#     #None的位置是一个函数，用来去掉自己不想算在内的元素
#     return difflib.SequenceMatcher(None, s1, s2).ratio()
#
# def difflibSim_out(s1, s2, outStr):
#     """
#     difflib 去掉不需要比较的字符，比如空格
#     :param s1:
#     :param s2:
#     :param outStr: 不需要比较的字符
#     :return:
#     """
#     seq = difflib.SequenceMatcher(lambda x: x in outStr, s1, s2)
#     ratio = seq.ratio()
#     return ratio
#
# def get_01_wordvec(s1, s2):
#     """
#     获取两个句子的0，1向量
#     :param s1:
#     :param s2:
#     :return: wordvector1, wordvector2
#     """
#     # 分词
#     cut1 = jieba.cut(s1)
#     cut2 = jieba.cut(s2)
#     list_word1 = (','.join(cut1)).split(',')
#     list_word2 = (','.join(cut2)).split(',')
#     # 列出所有的词,取并集
#     key_word = list(set(list_word1 + list_word2))
#     # 给定形状和类型的用0填充的矩阵存储向量
#     word_vector1 = np.zeros(len(key_word))
#     word_vector2 = np.zeros(len(key_word))
#     # 计算词频
#     # 依次确定向量的每个位置的值
#     for i in range(len(key_word)):
#         # 遍历key_word中每个词在句子中的出现次数
#         for j in range(len(list_word1)):
#             if key_word[i] == list_word1[j]:
#                 word_vector1[i] += 1
#         for k in range(len(list_word2)):
#             if key_word[i] == list_word2[k]:
#                 word_vector2[i] += 1
#     # 输出向量
#     #print(word_vector1)
#     #print(word_vector2)
#     return word_vector1, word_vector2


if __name__ == '__main__':
    print("other/sim_sentence.py")
    ###时间用时上，levenshtein 比 difflib 快
    methods = ['edit', 'levenshtein', 'jaro', 'cos', 'difflib', 'difflib_out']
    s1 = "通过这么一来一回的交锋，沈威已经初步确认了，这真是个缺心眼的，除了横就没别的了，一时又有些羡慕，同样都是世子，怎么自己就混得这么惨呢。"
    s2 = "一来一回 羡慕 初步确认"
    s3 = "一来一回 初步确认 羡慕 "
    s4 = "羡慕 初步确认"
    print(methods[0]+": "+str(calSimSentence(s1, s2, methods[0]))+'\t'+str(calSimSentence(s1, s3, methods[0]))+'\t'+str(calSimSentence(s1, s4, methods[0])))
    print(methods[1]+": "+str(calSimSentence(s1, s2, methods[1])) + '\t' + str(calSimSentence(s1, s3, methods[1])) + '\t' + str(
        calSimSentence(s1, s4, methods[1])))
    print(methods[2]+": "+str(calSimSentence(s1, s2, methods[2])) + '\t' + str(calSimSentence(s1, s3, methods[2])) + '\t' + str(
        calSimSentence(s1, s4, methods[2])))
    print(methods[3]+": "+str(calSimSentence(s1, s2, methods[3])) + '\t' + str(calSimSentence(s1, s3, methods[3])) + '\t' + str(
        calSimSentence(s1, s4, methods[3])))
    print(methods[4]+": "+str(calSimSentence(s1, s2, methods[4])) + '\t' + str(calSimSentence(s1, s3, methods[4])) + '\t' + str(
        calSimSentence(s1, s4, methods[4])))
    print(methods[5]+": "+str(calSimSentence(s1, s2, methods[5])) + '\t' + str(calSimSentence(s1, s3, methods[5])) + '\t' + str(
        calSimSentence(s1, s4, methods[5])))


